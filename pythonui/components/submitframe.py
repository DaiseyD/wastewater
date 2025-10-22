from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.DataTarget import DataTarget
from components.SubmitWindow import SubmitWindow

# This class is responsible for providing info on the parameters that have been set currently
class SubmitFrame(QFrame):
    def __init__(self, mainwindow):
        super().__init__()
        self.target = DataTarget().target
        self.data = DataTarget().data
        DataTarget().observers.append(self)
        self.mainwindow = mainwindow
        vbox = QVBoxLayout(self)
        self.infoBox = QLabel("")
        vbox.addWidget(self.infoBox)
        button = QPushButton("Submit")
        vbox.addWidget(button)
        button.clicked.connect(self.submit)
        self.update()

    def update(self):
        nParams = 0
        nSims = 1
        fieldsChanged = 0
        for itemKey in self.target['parameters']:
            item = self.target['parameters'][itemKey]
            paramICMLength = self.data['networkobjects'][itemKey]['length']
            for fieldKey in item:
                field = self.target['parameters'][itemKey][fieldKey]
                if field["strategy"] == "changeAll":
                    nSims = nSims * len(field["values"])
                    fieldsChanged += paramICMLength*nSims
                else:
                    fieldsChanged += paramICMLength*nSims
        nRainEvents = len(self.target['rainfallevents'])
        self.infoBox.setText(
            f"rainfallevents: {nRainEvents}\n"+
            f"nSims: {nSims}\n"+
            f"fields to Change: {fieldsChanged}\n"
            )
        self.target['FieldsChanged'] = fieldsChanged

    def getTotalFields(self, typeName):
        fieldsChanged = self.data['networkobjects'][typeName]['length']
        return fieldsChanged


    def submit(self):
        self.sw = SubmitWindow(self.target, self.mainwindow)
        self.sw.setGeometry(0,0, 1200, 800)
        self.sw.show()
    
    
    
