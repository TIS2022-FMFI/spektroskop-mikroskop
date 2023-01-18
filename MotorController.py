import time

import serial
from serial.tools import list_ports


class MotorController:
    def __init__(self):
        self.X = 0

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

    def moveX(self,direction,numberOfSteps):
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

            if direction == "l":
                self.X -= 1
            else:
                self.X += 1
            # self.ser.write(str.encode('G0X' + stepUnit + 'F01\r\n'))
            time.sleep(2)
        # self.ser.close()