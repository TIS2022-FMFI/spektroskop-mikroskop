import tkinter

from camera.FrameUtilMethods import FrameUtilMethods


class Render3DGraph:
    def __init__(self, newHeightMap=None, width=1300, height=900, cellSize=1, margin=5):
        self.chosenPX = None
        self.paintMap = None
        self.heightMap = newHeightMap
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.margin = margin
        self.canvas = None
        self.dimensions2D = True
        self.frameUtil = FrameUtilMethods()

    def setCellSize(self, newCellSize):
        """sets cell size within the allowed limits"""
        if newCellSize < 3 or newCellSize > 20:
            return
        self.cellSize = newCellSize

    def setHeightMap(self, newHeightMap):
        """assign new Height map"""
        self.heightMap = newHeightMap

    @staticmethod
    def getColor(value):
        """returns the color for given pixel"""
        return f'#{value[2]:02X}{value[1]:02X}{value[0]:02X}'

    def switch3Dto2D(self):
        """switch to change view from 2D onto 3D and vice versa"""
        if self.dimensions2D:
            self.render3D()
        else:
            self.render2D()
        self.dimensions2D = not self.dimensions2D

    def render3D(self):
        """renders 2D array into seemingly 3 dimensional space"""
        self.canvas.delete('all')
        y = self.margin + 260
        for j, line in enumerate(self.paintMap):
            x = 150 - j * (150 / len(self.paintMap))
            self.canvas.create_text(x + 750, y - 3, text="+" + str((len(self.paintMap)-j-1)*0.01) + "mm", fill="black",
                                    font='Helvetica 7 bold')
            for k, val in enumerate(line):
                if k == 0:
                    self.block(x, y, max(val), self.getColor(val), s2=max(line[k + 1]))
                elif k == len(line) - 1:
                    self.block(x, y, max(val), self.getColor(val), s1=max(line[k - 1]))
                else:
                    self.block(x, y, max(val), self.getColor(val), s1=max(line[k - 1]), s2=max(line[k + 1]))
                x += self.cellSize
            y += 150 / len(self.paintMap)
        self.canvas.create_text(930, 320, text="F\nR\nA\nM\nE\nS", fill="black", font='Helvetica 15 bold')
        self.canvas.create_text(400, 410, text="P I X E L S", fill="black", font='Helvetica 15 bold')  # ;) programur

    def block(self, x, y, size, color, s1=None, s2=None):
        """block is the smallest unit used in 3D render"""
        if size == 0:
            size = 1
        self.canvas.create_rectangle(x, y - size, x + self.cellSize, y, fill=color, outline=color)
        self.canvas.create_line(x, y - size - 1, x + self.cellSize + 1, y - size - 1, fill="Black")
        if s1 is not None and size > s1:
            self.canvas.create_line(x - 1, y - s1, x - 1, y - size - 1, fill="Black")
        if s2 is not None and size > s2:
            self.canvas.create_line(x + self.cellSize, y - s2, x + self.cellSize, y - size - 1, fill="Black")

    def render2D(self):
        """renders given height map as 2D"""
        self.canvas.delete('all')
        y = self.margin
        for line in self.paintMap:
            x = self.margin
            for val in line:
                self.canvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize,
                                             fill=self.getColor(val), outline=self.getColor(val))
                x += self.cellSize
            y += self.cellSize

    def setRenderMap(self):
        pom = []
        for frame in reversed(self.heightMap):
            self.frameUtil.setFrame(frame)
            pom.append(self.frameUtil.getCollumn(self.chosenPX))
        return pom

    def renderHeightMap(self, waveLength, newHeightMap=None):
        """main window creation, checks whether the new map fill fit into given window size,
         if it is possible then handles rendering of graphs"""
        if newHeightMap is not None:
            self.heightMap = newHeightMap
        if self.heightMap is None:
            pass
            # raise Exception("nothing to render")
        if len(self.heightMap) > 15:
            raise Exception("to much data to render")
        self.chosenPX = waveLength
        self.paintMap = self.setRenderMap()
        master = tkinter.Tk()
        master.resizable(False, False)
        master.title(str(self.chosenPX) + " nm")
        self.canvas = tkinter.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()

        def changePxValue():
            """changes px for slider value"""
            self.chosenPX = slider.get()
            print(self.chosenPX)
            self.paintMap = self.setRenderMap()
            if self.dimensions2D:
                self.render2D()
            else:
                self.render3D()

        slider = tkinter.Scale(master, from_=0, to=1280, orient=tkinter.HORIZONTAL, length=300, tickinterval=128)
        slider.set(self.chosenPX)
        slider.place(x=910, y=53)
        buttonSetWL = tkinter.Button(master, text="Set", command=changePxValue)
        buttonSetWL.place(x=880, y=70)
        button3D = tkinter.Button(master, text="3D/2D graph", command=self.switch3Dto2D)
        button3D.place(x=880, y=30)
        self.render2D()
        master.mainloop()
