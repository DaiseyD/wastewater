from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.DataTarget import DataTarget
from components.SubmitWindow import SubmitWindow

# This class is responsible for checking if all mandatory parameters are set, opens error popup if theyre not, otherwise, closes the window and return exit code 0
class SubmitFrame(QFrame):
    def __init__(self, mainwindow):
        super().__init__()
        self.target = DataTarget().target
        self.mainwindow = mainwindow
        vbox = QVBoxLayout(self)
        button = QPushButton("Submit")
        vbox.addWidget(button)
        button.clicked.connect(self.submit)

    def submit(self):
        self.sw = SubmitWindow(self.target, self.mainwindow)
        self.sw.setGeometry(0,0, 1200, 800)
        self.sw.show()
    
    
