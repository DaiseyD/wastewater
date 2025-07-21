from PySide6.QtWidgets import *
from PySide6.QtCore import *

# creating this class will open a popup window with an error message as specified in init
class ErrorPopup(QDialog):
    def __init__(self, errormessage):
        super().__init__()
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel(errormessage))
        self.exec_()