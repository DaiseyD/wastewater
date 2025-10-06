from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget
# utility function for toggling a widget's visibility
def toggleWidget(state, widget):
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
        self.setupParamFrame(layout)
        rainfallFrame = self.RainSubmitFrame(self.target['rainfallevents'])
        layout.addWidget(rainfallFrame)

    def setupParamFrame(self, layout):
        parametersBaseFrame = QFrame()
        layout.addWidget(parametersBaseFrame)
        vbox = QVBoxLayout(parametersBaseFrame)
        vbox.addWidget(QLabel("typeParameters"))
        toggleBox = QCheckBox()
        contentFrame = self.ParamFrame(data=self.target['parameters'])
        toggleBox.checkStateChanged.connect(lambda state, w = contentFrame: toggleWidget(state, w))
        vbox.addWidget(toggleBox)
        vbox.addWidget(contentFrame)
        contentFrame.hide()
    
    class ParamFrame(QFrame):
        def __init__(self, data):
            super().__init__()
            layout = QVBoxLayout(self)
            self.data = data
            for item in self.data:
                layout.addWidget(self.FieldFrame(item, self.data[item]))
    
        class FieldFrame(QFrame):
            def __init__(self, typeName, data):
                super().__init__()
                self.typeName = typeName
                self.data = data
                baseLayout = QVBoxLayout(self)
                titleLayout = QHBoxLayout()
                baseLayout.addLayout(titleLayout)
                titleLayout.addWidget(QLabel(typeName),7)

                toggleBox = QCheckBox()
                frame = self.setupFieldFrames(baseLayout)
                toggleBox.checkStateChanged.connect(lambda x, frame=frame : toggleWidget(x, frame))
                frame.hide()
                titleLayout.addWidget(toggleBox)
                baseLayout.addWidget(frame)
            
            def setupFieldFrames(self, layout):
                frame = QFrame()
                layout.addWidget(frame)
                frameLayout = QVBoxLayout(frame)    
                for i in self.data:
                    frameLayout.addWidget(QLabel(f"Strategy:{self.data[i]['strategy']}"))
                    frameLayout.addWidget(QLabel(i))
                return frame
            
    class RainSubmitFrame(QFrame):
        def __init__(self, data):
            super().__init__()
            self.data = data
            self.raindata = DataTarget().data['rainfallevents']
            layout = QVBoxLayout(self)
            for i in self.data:
                raineventlayout = QHBoxLayout()
                raineventlayout.addWidget(QLabel(f"{i}"))
                rainname = list(filter((lambda item: item['id'] == i), self.raindata))[0]['name']
                raineventlayout.addWidget(QLabel(rainname))
                layout.addLayout(raineventlayout)



    

        
    
        
        
        
