import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.rainframe import RainFrame
from components.parameterframe import ParameterFrame
# from components.selectframe import SelectFrame
from components.simparameterframe import SimParameterFrame
from components.submitframe import SubmitFrame
from components.DataTarget import DataTarget
import style
import json

def getjsondata():
    try:
        with(open("communication/ICMInfo.json", "r")) as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)


class Wastewindow(QMainWindow):
    
    def __init__(self):
        self.data = DataTarget().data
        self.datatarget = DataTarget().target
        super().__init__()
        self.setWindowTitle("DG_Infoworks")
        self.frame = QFrame()
        self.hbox = QHBoxLayout(self.frame)        
        self.setCentralWidget(self.frame)
        self.setLeftFrame()
        self.setRightFrame()

    def setLeftFrame(self):  
        leftFrame = QFrame()
        leftLayout = QGridLayout(leftFrame)
        self.hbox.addWidget(leftFrame)
        paraframe = ParameterFrame()
        leftLayout.addWidget(paraframe, 0, 0, 1, -1)
        submitFrame = SubmitFrame(self)
        leftLayout.addWidget(submitFrame, 1, 0, 1, -1)
        leftLayout.setRowStretch(0, 3)
        leftLayout.setRowStretch(1, 2)

    def setRightFrame(self):
        rightFrame = QFrame()
        self.hbox.addWidget(rightFrame)
        vbox = QVBoxLayout(rightFrame)
        rainFrame = RainFrame()
        vbox.addWidget(rainFrame)
        simParameterFrame = SimParameterFrame()
        vbox.addWidget(simParameterFrame)
        vbox.setStretch(0, 2)
        vbox.setStretch(1, 1)


# Create the Qt Application
data = DataTarget()
data.setData(getjsondata())
app = QApplication(sys.argv)
app.setStyleSheet(style.STYLEGLOBAL)

mainwindow = Wastewindow()
# Create a button, connect it and show it

mainwindow.show()
# Run the main Qt loop
app.exec()
exit(1)


