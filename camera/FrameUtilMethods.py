import numpy as np


class FrameUtilMethods:
    """Util methods to get desired lines from image frame

        NOTE: it needs to have frame in GBR format to work properly
        5
    """
    def __init__(self, frame=None, mainLine=100, lineFrom=100, lineTo=100):
        self.frame = frame
        self.mainLine = mainLine
        self.lineFrom = lineFrom
        self.lineTo = lineTo
        self.referenceData = None

    def avgLines(self, lineFrom, lineTo, color):
        """  :return Single avreged line from frame of given color and lines range  """

        if lineFrom == lineTo:
            return self.frame[self.mainLine, :, color]

        selectedLines = self.frame[lineFrom:lineTo, :, color]
        return np.mean(selectedLines, axis=0)

    def getRedLine(self):
        """ :return avarged line of red values from frame"""

        return self.avgLines(self.lineFrom, self.lineTo, 2)

    def getGreenLine(self):
        """ :return avarged line of green values from frame"""

        return self.avgLines(self.lineFrom, self.lineTo, 1)

    def getBlueLine(self):
        """ :return avarged line of blue values from frame"""

        return self.avgLines(self.lineFrom, self.lineTo, 0)

    def getMaxLine(self):
        """ :return avarged line of max(GBR) values from frame"""

        redLine = self.getRedLine()
        greenLine = self.getGreenLine()
        blueLine = self.getBlueLine()
        return np.maximum.reduce([redLine, greenLine, blueLine])

    def setFrame(self, frame):
        """Sets actual frame to work with"""
        self.frame = frame

    def setLinesFromTo(self, lineFrom, lineTo):
        """Sets desired range of lines to work With"""
        self.lineFrom = lineFrom
        self.lineTo = lineTo

    def setMainLine(self, mainLine):
        """Sets actual mainLine"""
        self.mainLine = mainLine

    def setReferenceData(self, referenceData):
        self.referenceData = referenceData

    def subtractLines(self, actualLine):
        """ :returns subtracted reference data from actual line"""
        if self.referenceData is not None:
            return np.subtract(actualLine, self.referenceData).astype(np.int8)
        else:
            raise ValueError("Empty reference data")

    def divdeLines(self, actualLine):
        """ :return divideded actual data by reference data"""

        if self.referenceData is not None:
            dividedLine = np.divide(actualLine, self.referenceData)
            np.place(dividedLine, np.isinf(dividedLine) | np.isnan(dividedLine), 1)
            return dividedLine
        else:
            raise ValueError("Empty reference data")

    def getCollumn(self, collumn):
        return self.frame[100:110, collumn, :]