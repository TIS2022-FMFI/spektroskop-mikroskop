from tkinter import *

from camera.Camera import Camera
from camera.Plot import Plot
from gui_widgets.CalibrationFrame import CalibrationFrame
from gui_widgets.CameraSettingsFrame import CameraSettingsFrame
from gui_widgets.D32Frame import D32Frame
from gui_widgets.D3Frame import D3Frame
from gui_widgets.GraphFunctionFrame import GraphFunctionFrame
from gui_widgets.GraphImageFrame import GraphImageFrame
from gui_widgets.ImportExportFrame import ImportExportFrame
from gui_widgets.MotorControlFrame import MotorControlFrame
from gui_widgets.NavbarFrame import NavbarFrame
from gui_widgets.SpectroImageFrame import SpectroImageFrame


class GUI(Tk):
    def __init__(self):
        super().__init__()
        # Initializing constants
        self.MASTER_WIDTH = 1500
        self.MASTER_HEIGHT = 750

        self.camera = Camera(0)
        # Setting master window size
        self.geometry(f"{self.MASTER_WIDTH}x{self.MASTER_HEIGHT}")

        # Initializing window for camera feed
        self.cameraFeedTopLevel = Toplevel()

        # Initializing frame objects
        self.spectroImageFrame = SpectroImageFrame()

        '''frame for live graph'''
        self.graphImageFrame = GraphImageFrame()
        self.plot = Plot(self.graphImageFrame)
        self.graphImageFrame.initPlot(self.plot)
        self.graphImageFrame.placeWidgets()



        self.motorControlsFrame = MotorControlFrame()

        self.cameraSettingsFrame = CameraSettingsFrame()
        self.calibrationFrame = CalibrationFrame(self.plot)
        self.d32Frame = D32Frame()
        self.graphFunctionFrame = GraphFunctionFrame()
        self.d3Frame = D3Frame()
        self.importExportFrame = ImportExportFrame()

        self.navbarFrame = NavbarFrame(self.cameraSettingsFrame, self.calibrationFrame, self.d32Frame,
                                       self.graphFunctionFrame, self.d3Frame, self.importExportFrame,
                                       self.cameraFeedTopLevel)
        self.navbarFrame.initPlot(self.plot)
        # Placing frame objects into the window
        self.navbarFrame.pack(side=LEFT, fill=Y)
        self.spectroImageFrame.pack(pady=(30, 0))
        self.graphImageFrame.pack(pady=(20, 0))
        self.motorControlsFrame.pack(side=BOTTOM)


        self.mainloop()