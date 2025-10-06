from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup

# utility function for toggling a widget's visibility
def toggleWidget(self, state, widget):
    if(state==Qt.CheckState.Checked):
        widget.show()
    elif state==Qt.CheckState.Unchecked :
        widget.hide()
    else:
        ErrorPopup("unknown state of checkbox")

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
        contentFrame = self.TypeFrame(self.target['parameters'])
        toggleBox.checkStateChanged.connect(lambda state, w = contentFrame: toggleWidget(state, w))
        vbox.addWidget(toggleBox)
        vbox.addWidget(contentFrame)
        contentFrame.hide()
    
    class TypeFrame(QFrame):
        def init(self, data):
            super().init()
            self.data = data
            for item in self.data:
                QLabel(item)


    

        
    
        
        
        
