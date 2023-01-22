import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class Camera:
    def __init__(self, cameraId=0):
        self.camera = cv2.VideoCapture(cameraId)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.zoom = 1.0
        self.angle = 0.0
        self.chanel = 'r'
        self.isCapturing = True

    def get_frame(self):
        while self.isCapturing:
            _, frame = self.camera.read()
            yield frame

    def pause(self):
        self.isCapturing = False

    def start(self):
        self.isCapturing = True

    def release(self):
        self.camera.release()

    def setExposureTime(self, exposureTime):
        self.camera.set(cv2.CAP_PROP_EXPOSURE, exposureTime)

    def setColorChanel(self, chanel):
        self.chanel = chanel

    def showImage(self):
        while True:
            frame = self.get_frame().__next__()
            cv2.imshow("frame", frame)

# def update_plot(frame, line):
#     # get the red color values of the first line of the frame
#     if camera.chanell == 'r':
#         # red_line = frame[250,:,2]
#         red_line = avgLines(frame, 0, 640, 2)
#         line.set_data(range(len(red_line)), red_line)
#         line.set_color("red")
#     if camera.chanell == 'g':
#         green_line = frame[250,:,0]
#         line.set_data(range(len(green_line)), green_line)
#         line.set_color("green")
#     if camera.chanell == 'b':
#         blue_line = frame[250,:,1]
#         line.set_data(range(len(blue_line)), blue_line)
#         line.set_color("blue")
#     if camera.chanell == 'a':
#         # a for all (max of r, g, b)
#         max_value = np.maximum(np.maximum(frame[250,:,0], frame[250,:,1]), frame[250,:,2])
#         line.set_data(range(len(max_value)), max_value)
#         line.set_color("black")
#
# def avgLines(frame, lineFrom, lineTo, color=2):
#     line = []
#     selectedLines = []
#     for i in range(lineFrom, lineTo):
#         selectedLines.append(frame[i,:,color])
#     for i in range(1280):
#         line.append(np.mean([li[i] for li in selectedLines]))
#     return line
#
# def show_plot(camera):
#     frame = camera.get_frame().__next__()
#     red = frame[0,:,2]
#     fig, ax = plt.subplots()
#     ax.set_xlim([0, 1280])
#     ax.set_ylim([0, 256])
#     # ax.autoscale(enable=True, axis='both', tight=None)
#     line, = ax.plot(red)
#     ani = FuncAnimation(fig, update_plot, fargs=(line,), frames=camera.get_frame(), interval=10)
#     plt.show()

# camera = Camera()
# show_plot(camera)
# camera.release()
# cv2.destroyAllWindows()
