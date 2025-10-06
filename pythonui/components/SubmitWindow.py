from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup



class SubmitWindow(QWidget):
    def __init__(self, target):
        self.target = target
        super().__init__()
        vboxBase = QVBoxLayout(self)
        vboxBase.addWidget(QLabel("Submission Window"), 1)
        mainarea = QScrollArea()
        vboxBase.addWidget(mainarea, 7)
        mainvbox = QVBoxLayout(mainarea)
        self.setupMain(mainvbox)
        


    def setupMain(self, layout):
        self.setupTypeFrame(layout)
        rainfallFrame = QFrame()
        layout.addWidget(rainfallFrame)

    def setupTypeFrame(self, layout):
        typeFrame = QFrame()
        layout.addWidget(typeFrame)
        vbox = QVBoxLayout(typeFrame)
        vbox.addWidget(QLabel("typeParameters"))
        toggleBox = QCheckBox()
        contentFrame = QLabel("BRRRRRRRRRRRRR")
        toggleBox.checkStateChanged.connect(lambda state, w = contentFrame: self.toggleWidget(state, w))
        vbox.addWidget(toggleBox)
        vbox.addWidget(contentFrame)
        contentFrame.hide()
    
    def toggleWidget(self, state, widget):
        if(state==Qt.CheckState.Checked):
            widget.show()
        elif state==Qt.CheckState.Unchecked :
            widget.hide()
        else:
            ErrorPopup("unknown state of checkbox")
        
        
        
        
