from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget

class SimParameterFrame(QFrame):
    """
    This frame contains textfields for setting parameters for the simulation itself, such as duration and name. Additionally,
    this frame contains a submit button which, when clicked, writes the saved parameters to a file and closes the UI so the ruby code can continue
    """
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
        vbox.addWidget(self.setupExecuteCheckbox())
        self.getCurrentState()

    def setupWasteOutput(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        wasteComboBox = QComboBox()
        self.wasteComboBox = wasteComboBox
        wasteComboBox.addItem("None")
        for item in self.data['wasteOutput']:
            wasteComboBox.addItem(item['name'])
        wasteComboBox.activated.connect(lambda x: self.updateWasteOutput(x))
        hbox.addWidget(QLabel("Waste water output"))
        hbox.addWidget(wasteComboBox)
        return frame

    def setupDuration(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("Duration (in minutes):"))
        durationField = QLineEdit()
        self.durationField = durationField
        durationField.editingFinished.connect(lambda widget=durationField: self.updateSimParameters(widget, "Duration"))
        hbox.addWidget(durationField)
        return frame

    def setupTimeStep(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("Timestep (in seconds):"))
        timestepField = QLineEdit()
        self.timestepField = timestepField
        timestepField.editingFinished.connect(lambda widget=timestepField: self.updateSimParameters(widget, "TimeStep"))
        hbox.addWidget(timestepField)
        return frame

    def setupRunName(self):
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("RunName"))
        runNameField = QLineEdit()
        self.runNameField = runNameField
        runNameField.editingFinished.connect(lambda widget=runNameField: self.updateString(widget, "RunName"))
        hbox.addWidget(runNameField)
        return frame
    
    def setupExecuteCheckbox(self):
        if "ExecuteRun" not in self.datatarget:
            self.datatarget["ExecuteRun"] = False
        frame = QFrame()
        hbox = QHBoxLayout(frame)
        hbox.addWidget(QLabel("Execute run"))
        executeRunCheck = QCheckBox()
        self.executeRunCheck = executeRunCheck
        executeRunCheck.checkStateChanged.connect(lambda x: self.updateBool(x, "ExecuteRun"))
        hbox.addWidget(executeRunCheck)
        return frame

    #updates a simparameter
    def updateSimParameters(self, widget, field):
        try:
            val = int(widget.text())
            self.datatarget['simparameters'][field]= val
        except Exception as e:
            ErrorPopup(str(e))

    # updates wastewater parameter
    def updateWasteOutput(self, index):
        if(index==0):
            self.datatarget['simparameters'].pop('Waste Water', None)
            return
        id = self.data['wasteOutput'][index - 1]['id']
        self.datatarget['simparameters']["Waste Water"] = id

    # updates a string value of a key in the datatarget
    def updateString(self, widget, key):
        self.datatarget[key] = widget.text()

    def updateBool(self, state, key):
        self.datatarget[key] = True if state==Qt.CheckState.Checked else False

    def getCurrentState(self):
        try:
            duration = self.datatarget['simparameters']['Duration']
            self.durationField.setText( str(duration) )
        except Exception as e:
            pass
        try:
            timestep = self.datatarget['simparameters']['TimeStep']
            self.timestepField.setText(str(timestep) )
        except:
            pass
        try:
            runname = self.datatarget['RunName']
            self.runNameField.setText(runname)
        except: 
            pass
        try:
            executeRun = self.datatarget['ExecuteRun']
            self.executeRunCheck.setCheckState(Qt.CheckState.Checked if executeRun else Qt.CheckState.Unchecked)
        except:
            pass
