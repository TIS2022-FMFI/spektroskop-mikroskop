from tkinter.filedialog import askopenfilename, asksaveasfile
import numpy as np
import matplotlib.pyplot as plt


class Calibration:
    def __init__(self, defaultPath="calibration_files/kalib.txt", plot=None):
        self.filepath = defaultPath
        self.nm = []
        self.pixels = []
        self.model = None
        self.plot = None
        self.loadFile()
        self.initPlot(plot)
        self.calculateModel()

    def initPlot(self, plot):
        """initializes plot for calib class to access"""
        self.plot = plot

    def __str__(self):
        """returns string format, formatted to multiple lines"""
        return "".join([str(self.pixels[i]) + "    " + str(self.nm[i]) + '\n' for i in range(len(self.pixels))])

    def chooseFile(self):
        """chooses calibration file"""
        self.filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.filepath == "":
            self.filepath = None

    def saveFile(self):
        """saves calibration file"""
        file = asksaveasfile(mode='w', defaultextension=".txt")
        if file is None:
            return
        file.write(self.__str__())
        file.close()

    def pushArrays(self, file):
        """"sets vvalues to arrays"""
        self.pixels = [float(line.split()[0]) for line in file]
        self.nm = [float(line.split()[1]) for line in file]

    def loadFile(self):
        """reads file from given path"""
        if self.filepath is None:
            raise Exception("Please choose file")
        with open(self.filepath, mode='r') as file:
            # self.calibrationChart = [[float(column) for column in line.split()] for line in file.readlines()]
            fileCopy = file.readlines()
            self.pushArrays(fileCopy)

    def loadFileFromApp(self, file):
        """loads calibration chart from app"""
        self.pixels = []
        self.nm = []
        for line in file.split('\n'):
            elem = line.split()
            if len(elem) != 2:
                continue
            if not elem[0].replace('.', '').isnumeric() or not elem[1].replace('.', '').isnumeric():
                return False
            self.pixels.append(float(elem[0]))
            self.nm.append(float(elem[1]))
        return True

    def calculateModel(self, polynomDegree=3):
        """calculates calibration chart"""
        self.model = np.poly1d(np.polyfit(self.pixels, self.nm, polynomDegree))
        self.plot.initModel(self.model)

    def getModel(self):
        """returns model"""
        return self.model


class CalibrationRender:
    def __init__(self):
        self.maxx = None
        self.minx = None
        self.offset = None

    def render(self, calibration):
        """renders calibration, based on data from calib.px, calib.nm, calib.model"""
        fig = plt.figure("  Spectrometer calibration chart ",
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
        """args=calibration object,  polynomial degree
           handles calibration from file, chosen from OS system"""
        calibration.chooseFile()
        if calibration.filepath == "":
            return
        calibration.loadFile()
        calibration.calculateModel(polynomeDegree)

    @staticmethod
    def calibrateFromApp(calibration, file, polynomeDegree=3):
        """handles calibration from app, values are given in text window"""
        if calibration.loadFileFromApp(file):
            calibration.calculateModel(polynomeDegree)
            