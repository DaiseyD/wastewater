from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget
from components.SubmitWindow import SubmitWindow
import json

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
        self.sw = SubmitWindow(self.target)
        self.sw.show()
        print("testing purpose: returning from submit method")
        return
        canRun = True
        if(self.target['rainfallevents']==[]):
            canRun = False
            ErrorPopup("please select a rainfallevent")
        if("RunName" not in self.target.keys()):
            canRun = False
            ErrorPopup("please set a RunName")
        if(canRun):
            sw = SubmitWindow()
            sw.show()
            self.writejsonresult(self.target)
            self.mainwindow.close()
            exit(0)

    def writejsonresult(self, result):
        try:
            with(open("communication/uiresults.json", "w")) as f:
                f.write(json.dumps(result))

        except Exception as e:
            print(f"Error writing to JSON file: {e}")
            exit(1)
