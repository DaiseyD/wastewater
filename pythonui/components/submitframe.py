from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
import json

class SubmitFrame(QFrame):
    def __init__(self, target, mainwindow):
        super().__init__()
        self.target = target
        self.mainwindow = mainwindow
        vbox = QVBoxLayout(self)
        button = QPushButton("Submit")
        vbox.addWidget(button)
        button.clicked.connect(self.submit)



    def submit(self):
        canRun = True
        if(self.target['rainfallevents']==[]):
            canRun = False
            ErrorPopup("please select a rainfallevent")
        if("RunName" not in self.target.keys()):
            canRun = False
            ErrorPopup("please set a RunName")
        if("SceneName" not in self.target.keys()):
            canRun = False
            ErrorPopup("please set a scenename")
        if(canRun):
            self.writejsonresult(self.target)
            self.mainwindow.close()

    def writejsonresult(self, result):
        try:
            with(open("communication/uiresults.json", "w")) as f:
                f.write(json.dumps(result))

        except Exception as e:
            print(f"Error writing to JSON file: {e}")
            exit(1)
