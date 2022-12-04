import tkinter

def xd() -> object:
    pass

class Render3DGraph:
    colors = ("#000000", "#6C006C", "#8100A2", "#6F00F8", "#2800FF",
              "#00ADFF", "#00FFC6", "#1FFF01", "#A9FF01", "#F4FF00",
              "#FFD000", "#FF8B00", "#FF1F00", "#C90000")

    def __init__(self, newHeightMap=None, width=500, height=500, cellSize=4, margin=5):
        self.maxIntensity = None
        self.heightMap = newHeightMap
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.margin = margin
        self.canvas = None
        self.dimensions2D = True

    def setCellSize(self, newCellSize):
        self.cellSize = newCellSize

    def setHeightMap(self, newHeightMap):
        self.heightMap = newHeightMap

    def getColor(self, value):
        if self.maxIntensity < len(self.colors):
            return self.colors[value]
        i = int(value / (self.maxIntensity // (len(self.colors) - 1)))
        if i >= len(self.colors):
            return self.colors[-1]
        return self.colors[i]

    def renderLegend(self):
        step = a.maxIntensity // (len(a.colors) - 1)
        if step == 0:
            step += 1
        for i, color in enumerate(self.colors):
            self.canvas.create_rectangle(self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3),
                                    self.margin + 10 * i,
                                    self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3) + 10,
                                    self.margin + 10 * i + 10,
                                    fill=color, outline=color)
            self.canvas.create_text(self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3) + 12,
                               self.margin - 2 + 10 * i,
                               text='>' + str(step * i), anchor='nw')
        self.canvas.create_text(self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3) + 12,
                           self.margin - 2 + 10 * (len(self.colors)),
                           text="<= " + str(self.maxIntensity), anchor='nw')

    def switch3Dto2D(self):
        if self.dimensions2D:
            self.render3D()
        else:
            self.render2D()
        self.dimensions2D = not self.dimensions2D

    def render3D(self):
        self.canvas.delete('all')
        self.canvas.create_text(100, 100, text="to be implemented")

    def render2D(self):
        self.canvas.delete('all')
        y = self.margin
        for lne in self.heightMap:
            x = self.margin
            for val in lne:
                self.canvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize,
                                             fill=self.getColor(val), outline=self.getColor(val))
                x += self.cellSize
            y += self.cellSize
        self.renderLegend()

    def renderHeightMap(self, waveLength, newHeightMap=None):
        if newHeightMap is not None:
            self.heightMap = newHeightMap
        if self.heightMap is None:
            print("nothing to render")
            return
        master = tkinter.Tk()
        master.title(str(waveLength) + " nm")

        if self.cellSize * len(self.heightMap) > self.height or self.cellSize * len(self.heightMap) > self.width:
            print("resize your window to fit all contents")
            return
        self.maxIntensity = max(map(max, self.heightMap))
        self.canvas = tkinter.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()

        button3D = tkinter.Button(master, text="3D/2D graph", command=self.switch3Dto2D)
        button3D.place(x=self.margin * 2 + self.cellSize * (len(self.heightMap[0]) + 3),
                       y=self.margin - 2 + 10 * (len(self.colors) + 2))
        self.render2D()
        master.mainloop()


if __name__ == "__main__":
    a = Render3DGraph(width=1800, height=1000, cellSize=14)
    lst = []
    with open("test.txt", "r") as f:
        for line in f:
            temp = []
            for e in line.split():
                temp.append(int(e))
            lst.append(temp)
    a.setHeightMap(lst)
    print(len(a.colors))
    a.renderHeightMap(200)
