from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget\


class SimParameterFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.datatarget = DataTarget().target
        self.data = DataTarget().data
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Mandatory fields:"))
        vbox.addWidget(self.setupWasteOutput())
        vbox.addWidget(self.setupDuration())
        vbox.addWidget(self.setupTimeStep())
        vbox.addWidget(self.setupRunName())
        vbox.addWidget(self.setupSceneName())

    def setupWasteOutput(self):
        comboBox = QComboBox()
        for item in self.data['wasteOutput']:
            comboBox.addItem(item['name'])
        comboBox.activated.connect(lambda x, id=item['id']: self.updateWasteOutput(id))
        return comboBox

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

    def setupSceneName(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("SceneName"))
        edit = QLineEdit()
        edit.editingFinished.connect(lambda widget=edit: self.updateString(widget, "SceneName"))
        hbox.addWidget(edit)
        return frame
    
    def updateSimParameters(self, widget, field):
        try:
            val = int(widget.text())
            self.datatarget['simparameters'][field]= val
        except Exception as e:
            ErrorPopup(str(e))
        print(self.datatarget)

    def updateWasteOutput(self, id):
        self.datatarget['simparameters']["WasteOutput"] = id
        print(self.datatarget)

    def updateString(self, widget, field):
        self.datatarget[field] = widget.text()
        print(self.datatarget)