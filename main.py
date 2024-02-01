from ultralytics import YOLO
import cv2
import time
import video_generator
from datetime import datetime
import threading
import multi_data_form

def thread_handler(recorder, accidents, time, lock):
    recorder.generateVideo()
    multi_data_form.make_request(accidents,time)
    lock.release()
    
def main():
    # camera set up
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # the resolution of external camera is 640x640, it also matches to the yolo model
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640) 

    # model set up
    model = YOLO("custom.pt")
    names = model.names # get the class name dictionary (search by int(classId))

    # The text parameters of current time
    coordinate = (10,30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    textColor = (255,255,255) # white
    borderColor = (0,0,0) # black
    thickness = 1
    lineType = cv2.LINE_AA

    ### 
    lock = threading.Lock()
    
    accidentRecord = video_generator.VideoGenerator()
    while(cap.isOpened()):
        ret, frame = cap.read()
        detectedAccidents = set()
        if ret == True:
            results = model.predict(frame)
            cv2.imshow("img",frame)
            # add the frame to videogenerator
            frame = cv2.resize(frame, (640, 480)) # the frame size should match with the size of videowriter, otherwise, the video capture cannot be open and not frame store in it
            currentTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            cv2.putText(frame, currentTime, coordinate, font, fontScale, borderColor, thickness+1, lineType) # border of current time
            cv2.putText(frame, currentTime, coordinate, font, fontScale, textColor, thickness, lineType)
            accidentRecord.addFrame(frame)
            for result in results[0]: # each of result only contains one class
                if names[int(result.boxes.cls)] == 'fall':
                    detectedAccidents.add(names[int(result.boxes.cls)])
                elif names[int(result.boxes.cls)] == "chest-pain": # chest pain
                    detectedAccidents.add(names[int(result.boxes.cls)])
                elif names[int(result.boxes.cls)] == "accidentC": # raise for help
                    detectedAccidents.add(names[int(result.boxes.cls)])
            if detectedAccidents: # the video generation start in here
                # a lock required in this block
                if lock.acquire(False):
                    p = threading.Thread(target=thread_handler, args=[accidentRecord, detectedAccidents, currentTime, lock])
                    p.start()
                    print("video generation started, please wait a seconds...............")
                ### the lock need to be release after generation and may be send out the video
            print(len(accidentRecord.frames))
            cv2.waitKey(1)
            
if __name__ == "__main__":
    main()            