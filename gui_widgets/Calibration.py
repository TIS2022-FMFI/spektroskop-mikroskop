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

    def pushArrays(self, file):
        self.pixels = [float(line.split()[0]) for line in file]
        self.nm = [float(line.split()[1]) for line in file]

    def loadFile(self):
        if self.filepath is None:
            raise Exception("Please choose file")
        with open(self.filepath, mode='r') as file:
            # self.calibrationChart = [[float(column) for column in line.split()] for line in file.readlines()]
            fileCopy = file.readlines()
            self.pushArrays(fileCopy)

    def loadFileFromApp(self, file):
        self.pixels = []
        self.nm = []
        for line in file.split('\n'):
            elem = line.split()
            if len(elem) != 2 or not elem[0].isnumeric() or not elem[1].isnumeric():
                return False
            self.pixels.append(float(elem[0]))
            self.nm.append(float(elem[1]))
        return True

    def calculateModel(self, polynomDegree=3):
        self.model = np.poly1d(np.polyfit(self.pixels, self.nm, polynomDegree))


class CalibrationRender:
    def __init__(self):
        self.maxx = None
        self.minx = None
        self.offset = None

    def render(self, calibration):
        fig = plt.figure("  Kalibračný súbor spektrometra ",
                         figsize=(10, 6),
                         facecolor='xkcd:mint green',
                         edgecolor='r',
                         linewidth=4)
        if calibration.model is None:
            raise Exception("No Calibration!")
        legendPos = calibration.nm - calibration.model(calibration.pixels)
        ax1 = plt.subplot(211)
        ax3 = plt.subplot(212)

        self.offset = np.max(calibration.pixels) / len(calibration.pixels)
        self.minx = np.min(calibration.pixels) - self.offset
        self.maxx = np.max(calibration.pixels) + self.offset
        polyline = self._createScatterplot(ax1, ax3, legendPos, calibration)
        ax1.plot(polyline, calibration.model(polyline), color='green')

        plt.xlim([self.minx, self.maxx])

        self._setax1(ax1)
        self._setax3(ax3)

        fig.show()

    def _createScatterplot(self, ax1, ax3, legendPos, calibration):
        # create scatterplot
        ax1.scatter(calibration.pixels, calibration.nm, label="Kalibračný bod", color="red", marker="o", s=150)
        ax3.plot([0, 1300], [0, 0], color="green")
        ax3.plot(calibration.pixels, legendPos, label="Kalibračná krivka", color="blue")
        ax3.scatter(calibration.pixels, legendPos, label="Kalibračný bod", color="red", marker="o", s=150)
        return np.linspace(self.minx, self.maxx, 800)

    @staticmethod
    def _setax1(ax1):
        ax1.set_xlabel('x - px')
        ax1.set_ylabel('y - nm')
        ax1.set_title('Calibration chart')
        ax1.grid(color='w')
        ax1.set_facecolor((0.9, 0.9, 0.9))
        ax1.legend()

    @staticmethod
    def _setax3(ax3):
        ax3.set_xlabel('x - px')
        ax3.set_ylabel('y - nm')
        ax3.grid(color='w')
        ax3.set_facecolor((0.9, 0.9, 0.9))
        ax3.legend()


class CalibrationHandler:
    def __init__(self):
        pass

    @staticmethod
    def calibrateFromFile(calibration, polynomeDegree=3):
        """args=calibration object,  polynomial degree"""
        calibration.chooseFile()
        if calibration.filepath == "":
            return
        calibration.loadFile()
        calibration.calculateModel(polynomeDegree)

    @staticmethod
    def calibrateFromApp(calibration, file, polynomeDegree=3):
        if calibration.loadFileFromApp(file):
            calibration.calculateModel(polynomeDegree)
