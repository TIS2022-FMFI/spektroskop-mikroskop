import datetime
import os
import time
from threading import Thread

import serial
from serial.tools import list_ports
from gui_widgets.ImporExportModule import *
import cv2 as cv


class MotorController:
    def __init__(self, plot=None):
        self.X = 0
        self.dataContainer = []
        self.plot = plot

        self.t = None

        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            motinfo = str(port).split(" - ")
            if ("USB-SERIAL" in port.description):
                com = motinfo[0]
        try:
            self.ser = serial.Serial(com, 115200)
        except:
            a = 1
        time.sleep(3)

    def _doMoveX(self,direction,numberOfSteps):
        # Setting relative mode (G90 absolute)
        # self.ser.write(str.encode('G91\r\n'))

        # Setting step "direction"
        if direction == "l":
            stepUnit = "-0.01"
        else:
            stepUnit = "0.01"
        for _ in range(numberOfSteps):
            print("ZZZZZZZZZZZZZZZZZZZ")
            # DO SOMETHING HERE

            self.dataContainer.append(self.plot.camera.get_frame().__next__())
            # self.dataContainer = self.plot.camera.get_frame().__next__()
            # print(self.dataContainer)
            if direction == "l":
                self.X -= 1
            else:
                self.X += 1
            # self.ser.write(str.encode('G0X' + stepUnit + 'F01\r\n'))
            time.sleep(2)
        # self.ser.close()

    def moveX(self, direction, numberOfSteps):
        self.t = Thread(target=self._doMoveX, args=(direction, numberOfSteps))
        self.t.start()

    def saveData(self):
        path = askdirectory()
        dateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        path += "/" + dateTime
        os.mkdir(path)
        frameCounter = 0
        for frame in self.dataContainer:
            name = path + "/{:03d}".format(frameCounter) + ".png"
            frameCounter += 1
            cv.imwrite(name, frame)

    def releaseThread(self):
        self.t.join()
