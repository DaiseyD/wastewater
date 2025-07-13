from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup

class SimParameterFrame(QFrame):

    def __init__(self, datatarget):
        super().__init__()
        self.datatarget = datatarget
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.setupDuration())
        vbox.addWidget(self.setupTimeStep())

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


    def updateSimParameters(self, widget, field):
        print(widget.text())
        try:
            val = int(widget.text())
            if 'simparameters' not in self.datatarget.keys():
                self.datatarget['simparameters'] = {}
            self.datatarget['simparameters'][field]= val
        
        except Exception as e:
            ErrorPopup(str(e))
        print(self.datatarget)
