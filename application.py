from gui_widgets.Gui import GUI
from camera.Plot import Plot


class Application:
    def __init__(self):
        self.gui = GUI()
        # self.plot = Plot(self.gui.graphImageFrame)
        # self.gui.graphImageFrame.initPlot(self.plot)
        # self.gui.graphImageFrame.placeGraph()



app = Application()
# app.gui.plot.release()
# app.gui.destroy()
# app.gui.graphImageFrame.placeGraph()