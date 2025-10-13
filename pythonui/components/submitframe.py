from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.DataTarget import DataTarget
from components.SubmitWindow import SubmitWindow

# This class is responsible for checking if all mandatory parameters are set, opens error popup if theyre not, otherwise, closes the window and return exit code 0
class SubmitFrame(QFrame):
    def __init__(self, mainwindow):
        super().__init__()
        self.target = DataTarget().target
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
        for item in self.target['parameters']:
            nParams += len(self.target['parameters'][item])
        nRainEvents = len(self.target['rainfallevents'])
        self.infoBox.setText(f"fields changed: {nParams}\nrainfallevents: {nRainEvents}")

    def submit(self):
        self.sw = SubmitWindow(self.target, self.mainwindow)
        self.sw.setGeometry(0,0, 1200, 800)
        self.sw.show()
    
    
    
