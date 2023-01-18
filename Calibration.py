from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt


class Calibration:
    def __init__(self, defaultPath=None):
        self.model = None
        self.nm = []
        self.pixels = []
        self.filepath = defaultPath
        # self.calibrationChart = None

    def chooseFile(self):
        self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if self.filepath == "":
            self.filepath = None

    def loadFile(self):
        if self.filepath is None:
            raise Exception("Please choose file")
        with open(self.filepath, mode='r') as file:
            # self.calibrationChart = [[float(column) for column in line.split()] for line in file.readlines()]
            fileCopy = file.readlines()
            self.pixels = [float(line.split()[0]) for line in fileCopy]
            self.nm = [float(line.split()[1]) for line in fileCopy]

    def calculateModel(self, polynomDegree=3):
        self.model = np.poly1d(np.polyfit(self.pixels, self.nm, polynomDegree))


class CalibrationRender:
    def __init__(self):
        pass

    def render(self, calibration):
        if calibration.model is None:
            raise Exception("No Calibration!")
        legendPos = calibration.nm - calibration.model(calibration.pixels)
        ax1 = plt.subplot(211)
        ax3 = plt.subplot(212)
        polyline = self.createScatterplot(ax1, ax3, legendPos, calibration)
        ax1.plot(polyline, calibration.model(polyline), color='green')

        plt.xlim([-65, 1365])

        self.setax1(ax1)
        self.setax3(ax3)

        # function to show the plot
        plt.show()

    # todo: spytat sa vojteka co by tam mohlo byt miesto HgAr--ortut

    @staticmethod
    def createScatterplot(ax1, ax3, legendPos, calibration):
        # create scatterplot
        ax1.scatter(calibration.pixels, calibration.nm, label="HgAr", color="red", marker="o", s=150)
        ax3.plot([0, 1300], [0, 0], color="green")
        ax3.plot(calibration.pixels, legendPos, label="HgAr", color="blue")
        ax3.scatter(calibration.pixels, legendPos, label="HgAr", color="red", marker="o", s=150)
        return np.linspace(0, 1300, 500)

    @staticmethod
    def setax1(ax1):
        ax1.set_xlabel('x - px')
        ax1.set_ylabel('y - nm')
        ax1.set_title('Calibration chart')
        ax1.grid(color='w')
        ax1.set_facecolor((0.9, 0.9, 0.9))
        ax1.legend()

    @staticmethod
    def setax3(ax3):
        ax3.set_xlabel('x - px')
        ax3.set_ylabel('y - nm')
        ax3.grid(color='w')
        ax3.set_facecolor((0.9, 0.9, 0.9))
        ax3.legend()


if __name__ == "__main__":
    c = Calibration()
    c.chooseFile()
    print(c.filepath)
    c.loadFile()
    c.calculateModel(3)
    r = CalibrationRender()
    r.render(c)

    # kalib(1)
