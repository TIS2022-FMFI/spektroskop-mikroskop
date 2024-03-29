from tkinter import *

class FrameBaseClass(Frame):
    def __init__(self):
        super().__init__()

        # Initializing constants, colors, fonts and images
        self.FONT = "Arial 10 bold"
        self.FONT_H = "Arial 15 bold"

        self.NAVBAR_FRAME_COLOR = "#3E4149"
        self.FRAME_COLOR = "#b3b3b3"
        self.BUTTON_COLOR = "#9648fb"
        self.BUTTON_COLOR_CLICKED = "#e4ccfd"

        self.NAVBAR_BUTTON_SIZE = 70

        self.BUTTON_SIZE_HEIGHT = 20
        self.BUTTON_SIZE_WIDTH = 80

        self.SPECTROMETER_FRAME_WIDTH = self.winfo_screenwidth() * 0.7
        self.SPECTROMETER_FRAME_HEIGHT = 200

        self.GRAPH_FRAME_WIDTH = self.winfo_screenwidth() * 0.7
        """ 300 is for spectrometer frame height plus motor control frame plus some padding"""
        self.GRAPH_FRAME_HEIGHT = (self.winfo_screenheight() * 0.4)

        self.IMAGE_TRICK = PhotoImage(width=1, height=1)  # Used for a trick that lets you enable button sizes by px

        self.PLAY_IMAGE = PhotoImage(file='GUI_Images\playImage.png')
        self.STOP_IMAGE = PhotoImage(file='GUI_Images\stopImage.png')
        self.CAMERA_IMAGE = PhotoImage(file="GUI_Images\\video-camera.png")
        self.ON_IMAGE = PhotoImage(file="GUI_Images\circleGreen.png")
        self.OFF_IMAGE = PhotoImage(file="GUI_Images\circleRed.png")

    def initializeButton(self, h, w, text):
        return Button(self, text=text, bg=self.BUTTON_COLOR, fg="white", font=self.FONT, borderwidth=0,
                      height=h, width=w, image=self.IMAGE_TRICK,
                      compound=CENTER)

    def initializeLabel(self, text, isHeading):
        font = self.FONT if isHeading == 0 else self.FONT_H
        return Label(self, text=text, font=font, bg=self.FRAME_COLOR)

    def initializeEntry(self, w):
        return Entry(self, width=w)

    def initializeScale(self, w):
        return Scale(self, width=w, orient=HORIZONTAL, name="exposure time", from_=0, to=-13)


    def removeWidgetsFromFrame(self):
        for widgets in self.winfo_children():
            widgets.grid_forget()

    def FUNCTION_TODO(self, argument):
        print(argument)
