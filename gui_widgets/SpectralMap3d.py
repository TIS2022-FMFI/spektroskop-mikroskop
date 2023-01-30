import tkinter
from tkinter import filedialog

import numpy as np

from camera.FrameUtilMethods import FrameUtilMethods

from PIL import ImageGrab


class Render3DGraph:
    def __init__(self, newHeightMap=None, width=1300, height=900, cellSize=3, margin=5):
        self.heightMap = newHeightMap
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.margin = margin
        self.canvas = None
        self.dimensions2D = True

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
        print(value)
        return f'#{value[2]:02X}{value[0]:02X}{value[1]:02X}'

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
        for j, line in enumerate(self.heightMap):
            x = self.margin + j * self.cellSize / 1.5 + self.cellSize * len(line)
            line = reversed(line)
            for k, val in enumerate(line):
                self.block(x, y, max(val), self.getColor(val))
                x -= self.cellSize * 1.3
            y += self.cellSize

    def block(self, x, y, size, color):
        """block is the smallest unit used in 3D render"""
        if size == 0:
            size = 1
        self.canvas.create_rectangle(x, y - size, x + self.cellSize, y, fill=color, outline="Black")
        self.canvas.create_polygon(x - self.cellSize / 3, y - self.cellSize / 3, x, y, x, y - size,
                                   x - self.cellSize / 3,
                                   y - size - self.cellSize / 3, fill=color, outline="Black")
        self.canvas.create_polygon(x, y - size, x + self.cellSize, y - size, x + self.cellSize * 2 / 3,
                                   y - size - self.cellSize / 3,
                                   x - self.cellSize / 3, y - size - self.cellSize / 3, fill=color, outline="Black")

    def render2D(self):
        """renders given height map as 2D"""
        self.canvas.delete('all')
        y = self.margin
        for line in self.heightMap:
            x = self.margin
            for val in line:
                self.canvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize,
                                             fill=self.getColor(val), outline=self.getColor(val))
                x += self.cellSize
            y += self.cellSize



    def renderHeightMap(self, waveLength, newHeightMap=None):
        """main window creation, checks whether the new map fill fit into given window size,
         if it is possible then handles rendering of graphs"""
        if newHeightMap is not None:
            self.heightMap = newHeightMap
        if self.heightMap is None:
            raise Exception("nothing to render")

        frameUtil = FrameUtilMethods()
        pom = []
        for frame in self.heightMap:
            frameUtil.setFrame(frame)
            pom.append(frameUtil.getCollumn(waveLength))

        self.heightMap = np.invert(pom)
        print(self.heightMap)
        master = tkinter.Tk()
        master.title(str(waveLength) + " nm")
        # if self.cellSize * len(self.heightMap) > self.height or self.cellSize * len(self.heightMap[0]) \
        #         + self.cellSize / 3 * len(self.heightMap) > self.width:
        #     raise Exception("resize your window to fit all contents")
        self.canvas = tkinter.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()

        def saveGraph():
            """saves graph image"""
            file = filedialog.asksaveasfilename(filetypes=(('PNG File', '.PNG'), ('PNG File', '.png')))
            file += ".png"
            ImageGrab.grab().crop((master.winfo_x()+10, master.winfo_y()+32, master.winfo_x()+self.width,
                                   master.winfo_y()+self.height)).save(file)
        button3D = tkinter.Button(master, text="3D/2D graph", command=self.switch3Dto2D)
        # print(self.heightMap)
        button3D.place(x=self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3) + self.cellSize / 3
                         * len(self.heightMap),
                       y=self.margin - 2 + 10 * (len(self.heightMap) + 2))
        buttonSave = tkinter.Button(master, text="Save", command=saveGraph)
        buttonSave.place(x=self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3) + self.cellSize / 3
                         * len(self.heightMap),
                       y=self.margin + 3 * (len(self.heightMap) + 2))
        self.render2D()
        master.mainloop()


if __name__ == "__main__":
    a = Render3DGraph(width=300, height=500, cellSize=14)
    lst = [[[220, 1, 255], [200, 200, 200], [100, 100, 100]], [[220, 0, 0], [0, 10, 0], [150, 0, 240]],
           [[0, 122, 0], [200, 200, 200], [230, 230, 230]], [[220, 0, 0], [0, 1, 0], [100, 100, 190]]]
    # with open(askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])) as f:
    #     a.setHeightMap([[int(float(column)) for column in line.split()] for line in f.readlines()])
    a.setHeightMap(lst)
    a.renderHeightMap(550)
    # print(a.maxIntensity, "max, min:", a.minIntensity)
