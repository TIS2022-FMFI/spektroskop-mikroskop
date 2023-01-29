from tkinter import *
from PIL import Image,ImageTk
import cv2

class LiveCameraWindow(Frame):
    def __init__(self,camera,parent):
        self.camera = camera
        self.window = Toplevel(parent)
        self.lmain = Label(self.window)
        self.lmain.pack()

        self.test_frame = None
        frame = Frame.__init__(self, parent)

        self.update_frame()
        # self.show_frame()

    def show_frame(self):
        print('showframe')
        imgtk = ImageTk.PhotoImage(image=self.img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

    def update_frame(self):
        # Capture frame-by-frame
        print("updateframe")
        ret, frame = self.camera.camera.read()
        # Convert the frame to a format suitable for Tkinter
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img = Image.fromarray(frame)
            self.show_frame()
            self.lmain.after(10, self.update_frame)
