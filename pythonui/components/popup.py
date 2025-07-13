from PySide6.QtWidgets import *
from PySide6.QtCore import *


class ErrorPopup(QDialog):
    def __init__(self, errormessage):
        super().__init__()
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel(errormessage))
        self.exec_()