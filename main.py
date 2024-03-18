from ultralytics import YOLO
import cv2
import time
import video_generator
from datetime import datetime
import threading
import multi_data_form
from ultralytics.utils.plotting import Annotator
import second_validation
import stream

    
def main():
    # camera set up
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # the resolution of external camera is 640x640, it also matches to the yolo model
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640) 

    # model set up
    model = YOLO("newmodel100epoch.pt")
    names = model.names # get the class name dictionary (search by int(classId))

    # The text parameters of current time
    coordinate = (10,30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    textColor = (255,255,255) # white
    borderColor = (0,0,0) # black
    thickness = 1
    lineType = cv2.LINE_AA

    
    accidentRecord = video_generator.VideoGenerator()
    secondValidation = second_validation.SecondValidation()
    VotingStart = False
    votingResult = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        detectedAccidents = set()
        if ret == True:
            results = model.predict(frame, conf=0.5)
            # add the frame to videogenerator
            frame = cv2.resize(frame, (640, 480)) # the frame size should match with the size of videowriter, otherwise, the video capture cannot be open and not frame store in it
            currentTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            cv2.putText(frame, currentTime, coordinate, font, fontScale, borderColor, thickness+1, lineType) # border of current time
            cv2.putText(frame, currentTime, coordinate, font, fontScale, textColor, thickness, lineType)
            stream.stream(frame)
            accidentRecord.addFrame(frame)
            for result in results[0]: # each of result only contains one class
                if names[int(result.boxes.cls)] == 'Fall':
                    detectedAccidents.add(names[int(result.boxes.cls)])
                elif names[int(result.boxes.cls)] == "Holdingchest": # chest pain
                    detectedAccidents.add(names[int(result.boxes.cls)])
                elif names[int(result.boxes.cls)] == "Hand Up": # raise for help
                    detectedAccidents.add(names[int(result.boxes.cls)])
            if detectedAccidents: # the video generation start in here
                VotingStart = True
            if VotingStart:
                secondValidation.voting(detectedAccidents)
                print(len(secondValidation.votes))
                print(secondValidation.votes)
                if len(secondValidation.votes) == secondValidation.maxVote:
                    VotingStart = False
                    votingResult = secondValidation.majorityCounting()
                print(votingResult)
                if len(votingResult) != 0:
                    accidentRecord.generateVideo()
                    multi_data_form.make_request(votingResult, currentTime)
                    print("")
                    votingResult = []    
            for r in results: 
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c=box.cls
                    annotator.box_label(b, model.names[int(c)])
            frame = annotator.result()        
            print(len(accidentRecord.frames))
            cv2.imshow("img",frame)
            cv2.waitKey(1)
            
if __name__ == "__main__":
    main()            