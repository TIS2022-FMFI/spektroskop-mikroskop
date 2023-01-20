import cv2

class CameraUtils:

    def __init__(self, cameraId = 0):
        self.frame = None
        self.videoCapture = cv2.VideoCapture(cameraId)

    def start(self):
        while(True):
            self.frame = self.videoCapture.read()
            cv2.imshow("frame", self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def getFrame(self):
        return self.frame
