from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from idlelib.tooltip import Hovertip

class D32Frame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame
        self.configure(bg=self.FRAME_COLOR)

        # Initializing widgets in frame

        # Labels
        self.spectralMapLabel = self.initializeLabel("Spectral\n map", 1)
        self.windowDimensionsLabel = self.initializeLabel("Window\n dimensions:", 0)
        self.xLabel = self.initializeLabel("X:", 0)
        self.yLabel = self.initializeLabel("Y:", 0)
        self.cellSizeLabel = self.initializeLabel("Cell size:", 0)

        # Buttons
        self.spectralMapSetButton = self.initializeButton(self.BUTTON_SIZE_HEIGHT, self.BUTTON_SIZE_WIDTH, "Set")
        self.spectralMapSetButton.configure(command=lambda: self.FUNCTION_TODO("ARGUMENT"))

        # Entries
        self.xEntry = self.initializeEntry(10)
        self.yEntry = self.initializeEntry(10)
        self.cellSizeEntry = self.initializeEntry(10)

        # Entry values
        self.xValue = self.xEntry.get()
        self.yValue = self.xEntry.get()
        self.cellSizeValue = self.xEntry.get()


        # Tooltips
        self.windowDimensionsTooltipMSG = "calibfile choose"
        self.windowDimensionsTooltip = Hovertip(self.windowDimensionsLabel, self.windowDimensionsTooltipMSG)

        self.xTooltipMSG = " create calibfile"
        self.xTooltip = Hovertip(self.xLabel, self.xTooltipMSG)

        self.yTooltipMSG = " create calibfile"
        self.yTooltip = Hovertip(self.yLabel, self.yTooltipMSG)

        self.cellSizeTooltipMSG = "cell size"
        self.cellSizeTooltip = Hovertip(self.cellSizeLabel, self.cellSizeTooltipMSG)


        self.placeWidgets()

    def placeWidgets(self):
        self.spectralMapLabel.pack()

        self.windowDimensionsLabel.pack()

        self.xLabel.pack()
        self.xEntry.pack()

        self.yLabel.pack()
        self.yEntry.pack()

        self.cellSizeLabel.pack()
        self.cellSizeEntry.pack()

        self.spectralMapSetButton.pack(pady=(5,5))

        # self.spectralMapLabel.grid(sticky=W, row=0, column=0, pady=(10, 0))
        #
        # self.windowDimensionsLabel.grid(sticky=W, row=1, column=0, pady=(10, 0))
        #
        # self.xLabel.grid(sticky=W, row=2, column=0, pady=(10, 0))
        # self.xEntry.grid(sticky=W, row=2, column=1, pady=(10, 0), padx=(10, 10))
        #
        # self.yLabel.grid(sticky=W, row=3, column=0, pady=(10, 0))
        # self.yEntry.grid(sticky=W, row=3, column=1, pady=(10, 0), padx=(10, 10))
        #
        # self.cellSizeLabel.grid(sticky=W, row=4, column=0, pady=(10, 0))
        # self.cellSizeEntry.grid(sticky=W, row=4, column=1, pady=(10, 0), padx=(10, 10))
        #
        # self.spectralMapSetButton.grid(row=5, column=0, pady=(10, 10), columnspan=2)
