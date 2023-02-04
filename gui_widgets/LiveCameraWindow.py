import time
from threading import Thread
from tkinter import *
from PIL import Image,ImageTk
import cv2

class LiveCameraWindow(Frame):
    def __init__(self, camera, parent):
        self.lmain = None
        self.window = None
        self.parent = parent
        self.camera = camera

        self.test_frame = None
        frame = Frame.__init__(self, parent)

        # self.update_frame()
        # self.show_frame()

        self.t = None

    def show_frame(self):
        imgtk = ImageTk.PhotoImage(image=self.img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

    def update_frame(self):
        # Capture frame-by-frame
        ret = True
        frame = self.camera.get_frame().__next__()
        # Convert the frame to a format suitable for Tkinter
        if ret and frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img = Image.fromarray(frame)
            self.show_frame()
            # time.sleep(0.1)
            self.lmain.after(100, self.update_frame)

    def initCamera(self, camera):
        self.camera = camera

    def wof(self):
        self.camera.start()
        self.window = Toplevel(self.parent)
        self.lmain = Label(self.window)
        self.lmain.pack()
        self.update_frame()
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    def start(self):
        self.t = Thread(target=self.wof)
        self.t.start()
        # self.update_frame()

        #

    def release(self):
        self.t.join()
        # ...

    def onClose(self):
        self.camera.release()
        self.window.destroy()
        self.t.join()
