from gui_widgets.FrameBaseClass import FrameBaseClass


class SpectroImageFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame and size
        self.configure(bg="red", width=self.SPECTROMETER_FRAME_WIDTH, height=self.SPECTROMETER_FRAME_HEIGHT)
        # Setting that disables frame shrinkage to fit widgets
        self.propagate(False)
        self.camera = None

    def placeWidgets(self):
        pass

    def initCamera(self, camera):
        self.camera = camera
