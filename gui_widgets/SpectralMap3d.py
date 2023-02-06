import tkinter
from tkinter import filedialog

import cv2

from camera.FrameUtilMethods import FrameUtilMethods

from PIL import ImageGrab


class Render3DGraph:
    def __init__(self, newHeightMap=None, width=1300, height=900, cellSize=1, margin=5):
        self.paintMap = None
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
            for k, val in enumerate(line):
                if k == 0:
                    self.block(x, y, max(val), self.getColor(val), s2=max(line[k + 1]))
                elif k == len(line) - 1:
                    self.block(x, y, max(val), self.getColor(val), s1=max(line[k - 1]))
                else:
                    self.block(x, y, max(val), self.getColor(val), s1=max(line[k - 1]), s2=max(line[k + 1]))
                x += self.cellSize
            y += 150 / len(self.paintMap)
        self.canvas.create_text(890, 320, text="F\nR\nA\nM\nE\nS", fill="black", font='Helvetica 15 bold')
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

    def renderHeightMap(self, waveLength, newHeightMap=None):
        """main window creation, checks whether the new map fill fit into given window size,
         if it is possible then handles rendering of graphs"""
        if newHeightMap is not None:
            self.heightMap = newHeightMap
        if self.heightMap is None:
            raise Exception("nothing to render")
        if len(self.heightMap) > 22:
            raise Exception("to much data to render")
        frameUtil = FrameUtilMethods()
        pom = []
        for frame in reversed(self.heightMap):
            frameUtil.setFrame(frame)
            pom.append(frameUtil.getCollumn(waveLength))
        self.paintMap = pom
        master = tkinter.Tk()
        master.resizable(False, False)
        master.title(str(waveLength) + " nm")
        self.canvas = tkinter.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()

        def saveGraph():
            """saves graph image"""
            file = filedialog.asksaveasfilename(filetypes=(('PNG File', '.PNG'), ('PNG File', '.png')))
            if file is not None and file != '':
                file += ".png"
                ImageGrab.grab().crop((master.winfo_x() + 10, master.winfo_y() + 32, master.winfo_x() + self.width,
                                       master.winfo_y() + self.height)).save(file)

        button3D = tkinter.Button(master, text="3D/2D graph", command=self.switch3Dto2D)
        button3D.place(x=880, y=10)
        buttonSave = tkinter.Button(master, text="Save", command=saveGraph)
        buttonSave.place(x=880, y=40)
        self.render2D()
        master.mainloop()
