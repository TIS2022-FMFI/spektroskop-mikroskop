from tkinter import *
from gui_widgets.FrameBaseClass import FrameBaseClass
from gui_widgets.MotorController import MotorController


# TODO SCROLLBAR ABY UPDATEOVAL LABEL
class MotorControlFrame(FrameBaseClass):

    def __init__(self, plot=None):
        super().__init__()
        self.plot = plot
        self.motorController = MotorController(self.plot)

        # Initializing widgets

        # Scrollbar
        # Radiobutton values/state
        self.scrollBarVal = DoubleVar()
        # Pouzivam DoubleVar lebo automaticky sa updatuje # Na ziskania value pouzi self.scrollBarVal.get()
        self.scrollBar = Scale(self, from_=0, to=0.3, orient=HORIZONTAL, length=500, command=self.test, resolution=0.01,
                               font=self.FONT, variable=self.scrollBarVal)

        # Labels
        self.mmLabel = Label(self, text="mm", font=self.FONT)
        self.valueLabel = Label(self, text="Value: 0.00mm", font=self.FONT)

        # Buttons
        self.backToStartButton = self.initializeButton(30, 50, "|<")

        self.backToStartButton.configure(command=lambda: self.motorController.moveX("l", self.motorController.X))

        self.stepBackButton = self.initializeButton(30, 50, "-")
        self.stepBackButton.configure(command=lambda: self.motorController.moveX("l", 1))

        self.stepForwardButton = self.initializeButton(30, 50, "+")
        self.stepForwardButton.configure(command=lambda: self.motorController.moveX("r", 1))

        self.forwardStepsButton = self.initializeButton(30, 50, ">|")
        self.forwardStepsButton.configure(
            command=lambda: self.motorController.moveX("r", int(self.scrollBarVal.get() * 100)))

        self.doStep = self.initializeButton(30, 50, "Start")
        self.doStep.configure(command=lambda: self.motorController.moveX("r", int(self.stepEntry.get())))

        # Entry
        self.stepEntry = self.initializeEntry(15)

        # Entry values
        self.stepValue = self.stepEntry.get()

        self.placeWidgets()

    # z nejako dovodu pri commandoch pri scale widgeti musi byt aj to "v" premenna, inak to pada idk why
    def test(self, v):
        print(self.scrollBarVal.get())

    def placeWidgets(self):
        self.backToStartButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.stepBackButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.mmLabel.pack(side=LEFT, padx=(10, 0), pady=(10, 10))
        self.scrollBar.pack(side=LEFT, padx=(10, 10), pady=(10, 25))
        self.stepForwardButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.forwardStepsButton.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.doStep.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
        self.stepEntry.pack(side=LEFT, padx=(10, 10), pady=(10, 10))
