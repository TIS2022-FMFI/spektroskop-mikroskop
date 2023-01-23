from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass

# # TODO LOGIKA PRI ZMENE CONNECTION OBRAZKA

class D3Frame(FrameBaseClass):
    def __init__(self):
        super().__init__()

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # #Initalizing widgets in frame

        # Labels
        self.d3Label = self.initializeLabel("3D", 1)
        self.wavelengthLabel = self.initializeLabel("Wavelength:", 0)
        self.scanLabel = self.initializeLabel("Scan:", 0)

        # Buttons
        self.showButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.showButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Images
        self.scanImage = Label(self, image=self.OFF_IMAGE, bg=self.FRAME_COLOR)

        # Entries
        self.wavelengthEntry = self.initializeEntry(15)

        # Entry values
        self.wavelengthValue = self.wavelengthEntry.get()

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.d3Label.grid(sticky=W, row=0, column=0, pady=(10, 0))
        self.wavelengthLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        self.wavelengthEntry.grid(sticky=W, row=1, column=1, padx=(0, 10), pady=(10, 0))
        self.showButton.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))
        self.scanLabel.grid(sticky=W, row=3, column=0, padx=(0, 10), pady=(10, 10))
        self.scanImage.grid(row=3, column=0, padx=(30, 10), pady=(10, 10))