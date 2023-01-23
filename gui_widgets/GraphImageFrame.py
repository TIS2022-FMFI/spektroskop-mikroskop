from gui_widgets.FrameBaseClass import FrameBaseClass


class GraphImageFrame(FrameBaseClass):
    def __init__(self):
        super().__init__()
        # Setting color of frame and size
        self.configure(bg="green", width=self.GRAPH_FRAME_WIDTH, height=self.GRAPH_FRAME_HEIGHT)
        # Setting that disables frame shrinkage to fit widgets
        self.propagate(False)
        # Initializing widgets
        self.plot = None
        # self.placeWidgets()

    def placeWidgets(self):
        self.plot.show_plot()

    def initPlot(self, plot):
        self.plot = plot