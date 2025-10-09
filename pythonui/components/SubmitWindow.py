from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget
from components.simparameterframe import SimParameterFrame
import json

# utility function for toggling a widget's visibility
def toggleWidget(state, widget):
    if(state==Qt.CheckState.Checked):
        widget.show()
    elif state==Qt.CheckState.Unchecked :
        widget.hide()
    else:
        ErrorPopup("unknown state of checkbox")

class SubmitWindow(QWidget):
    def __init__(self, target, mainwindow):
        self.target = target
        super().__init__()
        vboxBase = QVBoxLayout(self)
        vboxBase.addWidget(QLabel("Submission Window"), 1)
        mainarea = QScrollArea()
        vboxBase.addWidget(mainarea, 6)
        mainframe = QFrame()
        mainvbox = QVBoxLayout(mainframe)
        self.setupMain(mainvbox)
        mainarea.setWidget(mainframe)
        mainarea.setWidgetResizable(True)
        vboxBase.addWidget(SimParameterFrame())
        vboxBase.addWidget(self.SubmitArea(mainwindow))
        
    def setupMain(self, layout):
        self.setupParamFrame(layout)
        rainfallFrame = self.RainSubmitFrame(self.target['rainfallevents'])
        layout.addWidget(rainfallFrame)

    def setupParamFrame(self, layout):
        parametersBaseFrame = QFrame()
        layout.addWidget(parametersBaseFrame)
        vbox = QVBoxLayout(parametersBaseFrame)
        paramTitleLayout = QHBoxLayout()
        vbox.addLayout(paramTitleLayout)
        paramTitleLayout.addWidget(QLabel("typeParameters"))
        toggleBox = QCheckBox()
        contentFrame = self.ParamFrame(data=self.target['parameters'])
        toggleBox.checkStateChanged.connect(lambda state, w = contentFrame: toggleWidget(state, w))
        paramTitleLayout.addWidget(toggleBox)
        vbox.addWidget(contentFrame)
        contentFrame.hide()
    
    class ParamFrame(QFrame):
        def __init__(self, data):
            super().__init__()
            self.setStyleSheet("ParamFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
            self.data = data
            layout = QVBoxLayout(self)
            self.data = data
            for item in self.data:
                layout.addWidget(self.FieldFrame(item, self.data[item]))
    
        class FieldFrame(QFrame):
            def __init__(self, typeName, data):
                super().__init__()
                self.setStyleSheet("FieldFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
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
            self.setStyleSheet("RainSubmitFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
            self.data = data
            self.raindata = DataTarget().data['rainfallevents']
            layout = QVBoxLayout(self)
            title = QLabel("RainfallEvents")
            title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            layout.addWidget(title, 1,Qt.AlignmentFlag.AlignTop)
            dataframe = QFrame()
            layout.addWidget(dataframe,7)
            datalayout = QVBoxLayout(dataframe)
            dataframe.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            for i in self.data:
                raineventlayout = QHBoxLayout()
                raineventlayout.addWidget(QLabel(f"{i}"))
                rainname = list(filter((lambda item: item['id'] == i), self.raindata))[0]['name']
                raineventlayout.addWidget(QLabel(rainname))
                datalayout.addLayout(raineventlayout)
    
    class SubmitArea(QFrame):
        def __init__(self, mainwindow):
            super().__init__()
            self.target = DataTarget().target
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
            if(canRun):
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





    

        
    
        
        
        
