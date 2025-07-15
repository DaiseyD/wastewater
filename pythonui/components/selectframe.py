from PySide6.QtWidgets import *
from PySide6.QtCore import *

class SelectFrame(QFrame):
    
    def __init__(self, data, datatarget):
        super().__init__()
        self.datatarget = datatarget
        self.data = data
        scrollArea = QScrollArea()
        vboxscroll = QVBoxLayout(self)
        vboxscroll.addWidget(scrollArea)
        container = QFrame()
        vbox = QVBoxLayout(container)
        for (index, item) in enumerate(self.data['selectionobjects']):
            l = QLabel(item)
            vbox.addWidget(l)
        scrollArea.setWidget(container)
    