from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget

# This frame contains the other simparameters which have to be set in order to run the simulation
class SimParameterFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.datatarget = DataTarget().target
        self.data = DataTarget().data
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Mandatory simulation parameters:"))
        vbox.addWidget(self.setupWasteOutput())
        vbox.addWidget(self.setupDuration())
        vbox.addWidget(self.setupTimeStep())
        vbox.addWidget(self.setupRunName())

    def setupWasteOutput(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)

        comboBox = QComboBox()
        comboBox.addItem("None")
        for item in self.data['wasteOutput']:
            comboBox.addItem(item['name'])
        comboBox.activated.connect(lambda x: self.updateWasteOutput(x))
        hbox.addWidget(QLabel("Waste water output"))
        hbox.addWidget(comboBox)
        return frame

    def setupDuration(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("Duration (in minutes):"))
        edit = QLineEdit()
        edit.editingFinished.connect(lambda widget=edit: self.updateSimParameters(widget, "Duration"))
        hbox.addWidget(edit)
        return frame

    def setupTimeStep(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("Timestep (in seconds):"))
        edit = QLineEdit()
        edit.editingFinished.connect(lambda widget=edit: self.updateSimParameters(widget, "TimeStep"))
        hbox.addWidget(edit)
        return frame

    def setupRunName(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("RunName"))
        edit = QLineEdit()
        edit.editingFinished.connect(lambda widget=edit: self.updateString(widget, "RunName"))
        hbox.addWidget(edit)
        return frame
    
    #updates a simparameter
    def updateSimParameters(self, widget, field):
        try:
            val = int(widget.text())
            self.datatarget['simparameters'][field]= val
        except Exception as e:
            ErrorPopup(str(e))
        print(self.datatarget)

    # updates wastewater parameter
    def updateWasteOutput(self, index):
        if(index==0):
            self.datatarget['simparameters'].pop('Waste Water', None)
            print(self.datatarget)
            return
        id = self.data['wasteOutput'][index - 1]['id']
        self.datatarget['simparameters']["Waste Water"] = id
        print(self.datatarget)

    # updates a string value of a key in the datatarget
    def updateString(self, widget, key):
        self.datatarget[key] = widget.text()
        print(self.datatarget)