from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from gui_widgets.SpectralMap3d import Render3DGraph
from idlelib.tooltip import Hovertip


class D3Frame(FrameBaseClass):
    def __init__(self, motorFrame):
        super().__init__()

        self.motorFrame = motorFrame

        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # #Initalizing widgets in frame

        # Labels
        self.d3Label = self.initializeLabel("3D", 1)
        self.wavelengthLabel = self.initializeLabel("px:", 0)
        self.scanLabel = self.initializeLabel("Scan:", 0)

        # Buttons
        self.showButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Show")
        self.showButton.configure(command=lambda: self.show3Dgraph())

        # Images
        self.scanImage = Label(self, image=self.OFF_IMAGE, bg=self.FRAME_COLOR)

        # Entries
        self.wavelengthEntry = self.initializeEntry(13)

        # Entry values
        self.wavelengthValue = self.wavelengthEntry.get()

        #Tooltips
        self.wavelengthLabelTooltipMSG = "Image collum for image sequence analysis."
        self.calibrationChartTooltip = Hovertip(self.wavelengthLabel,
                                                       self.wavelengthLabelTooltipMSG)

        # Placing widgets into frame
        self.placeWidgets()

    def placeWidgets(self):
        self.d3Label.pack()
        self.wavelengthLabel.pack()
        self.wavelengthEntry.pack()
        self.showButton.pack(pady=(5,5))
        self.scanLabel.pack()
        self.scanImage.pack()



        # self.d3Label.grid(sticky=W, row=0, column=0, pady=(10, 0))
        # self.wavelengthLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        # self.wavelengthEntry.grid(sticky=W, row=1, column=1, padx=(0, 10), pady=(10, 0))
        # self.showButton.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))
        # self.scanLabel.grid(sticky=W, row=3, column=0, padx=(0, 10), pady=(10, 10))
        # self.scanImage.grid(row=3, column=0, padx=(30, 10), pady=(10, 10))
        
    def show3Dgraph(self):
        dataFor3D = self.motorFrame.motorController.dataContainer
        render = Render3DGraph(dataFor3D)
        value = self.wavelengthEntry.get()
        if not value.isnumeric():
            value = 0
        render.renderHeightMap(int(value))
