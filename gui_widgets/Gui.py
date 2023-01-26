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

        self.model = None

        # Setting master window size
        self.geometry(f"{self.MASTER_WIDTH}x{self.MASTER_HEIGHT}")

        # Initializing window for camera feed
        self.cameraFeedTopLevel = Toplevel()

        '''frame for camera image'''
        self.spectroImageFrame = SpectroImageFrame()
        self.camera = Camera(0)
        self.camera.initCanvas(self.spectroImageFrame)
        self.spectroImageFrame.initCamera(self.camera)
        self.spectroImageFrame.placeWidgets()

        '''frame for live graph'''
        self.graphImageFrame = GraphImageFrame()
        self.plot = Plot(self.graphImageFrame, self.camera)



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
        # Placing frame objects into the window
        self.navbarFrame.pack(side=LEFT, fill=Y)
        self.spectroImageFrame.pack(pady=(30, 0))
        self.graphImageFrame.pack(pady=(20, 0))
        self.motorControlsFrame.pack(side=BOTTOM)

        '''init plot for frames that has dependancy on it'''
        self.initPlots()
        self.placeWidets()

        self.mainloop()
        self.plot.release()
        self.quit()

        self.release()

    def release(self):
        self.plot.release()
        self.destroy()

    def initPlots(self):
        self.graphImageFrame.initPlot(self.plot)
        self.navbarFrame.initPlot(self.plot)
        self.cameraSettingsFrame.initPlot(self.plot)

    def placeWidets(self):
        self.graphImageFrame.placeWidgets()


