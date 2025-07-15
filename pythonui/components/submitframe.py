from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup

class SubmitFrame(QFrame):
    def __init__(self, target):
        super().__init__()
        self.target = target
        vbox = QVBoxLayout(self)
        button = QPushButton("Submit")
        vbox.addWidget(button)
        button.clicked.connect(self.submit)



    def submit(self):
        if(self.target['rainfallevents']==[]):
            ErrorPopup("please select a rainfallevent")
        if("RunName" not in self.target.keys()):
            ErrorPopup("please set a RunName")
        if("SceneName" not in self.target.keys()):
            ErrorPopup("please set a scenename")