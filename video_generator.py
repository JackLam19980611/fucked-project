import time
import cv2
class VideoGenerator:
    def __init__(self):
        self.frames = []
        self.FPS = 12
        self.maxFrameSize = self.FPS*20
        self.videoFileName = "accident_recording.avi"

    def generateVideo(self):
        time.sleep(5) # wait few seconds to get more frame not only the accident frame
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        videoHighet = 640
        videoWidth = 480
        out = cv2.VideoWriter(self.videoFileName, fourcc, self.FPS, (videoHighet, videoWidth))
        startFrame = len(self.frames) - self.maxFrameSize//2 if len(self.frames) - self.maxFrameSize//2 >0 else 0    
        for frame in self.frames[startFrame:]:
            out.write(frame)
        out.release()
            
    def addFrame(self, frame):
        if len(self.frames) == self.maxFrameSize:
            self.frames = self.frames[self.maxFrameSize//2:] # remove the half of the frames in the array
        self.frames.append(frame)
        