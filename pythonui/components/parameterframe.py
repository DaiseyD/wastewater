from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget

def packFrame(widgets, direction): # this function puts widgets into a frame and into a vbox if direction = 'V' or an hbox if direction = 'H'
    frame = QFrame()
    if(direction=='V'):
        layout = QVBoxLayout(frame)
    elif (direction=="H"):
        layout = QHBoxLayout(frame)
    else: 
        raise Exception("wrong direction argument to pack frame")
    for w in widgets:
        layout.addWidget(w)
    return frame

class ParameterFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.datatarget = DataTarget().target
        self.data = DataTarget().data
        vbox = QVBoxLayout(self)
        scrollLeft = QScrollArea()
        vbox.addWidget(scrollLeft)
        container = QFrame()
        rightLayout= QVBoxLayout(container)
        title = QLabel("Parameters")
        title.setStyleSheet("color: hsl(200, 30%, 10%); font-size:16px;")
        rightLayout.addWidget(title)
        for (index, typeName) in enumerate(self.data['networkobjects'].keys()):
            button = QPushButton(f"{index} {typeName}")
            button.setStyleSheet("color: hsl(200, 30%, 20%); padding: 10px 2px;")
            button.clicked.connect(lambda checked, typeName=typeName: self.openTypeWindow(typeName))
            rightLayout.addWidget(button)
        
        scrollLeft.setWidget(container)
    
    def openTypeWindow(self, item):
        self.w = TypeWindow(item)
        self.w.show()

class TypeWindow(QWidget):
    def __init__(self, typeName):
        super().__init__()
        self.name = typeName
        self.data = DataTarget().data['networkobjects'][typeName]
        self.datatarget = DataTarget().target['parameters']
        vboxBase = QVBoxLayout(self)
        frameTop = QFrame()
        vboxBase.addWidget(frameTop)
        hboxTop = QHBoxLayout(frameTop)
        self.initTitleAndSearch(hboxTop)
        frameBottom = QFrame()
        vboxBase.addWidget(frameBottom)
        boxCard = QVBoxLayout(frameBottom)
        scrollArea = QScrollArea()
        boxCard.addWidget(scrollArea)
        container = QFrame()
        gridbox = QVBoxLayout(container)
        gridbox.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.typeWidgets = []
        i = 0
        for (index,item) in enumerate(self.data['fields']):
            self.addlinegrid(gridbox, typeName, item)
            i = i + 1 
        scrollArea.setWidget(container)


    def initTitleAndSearch(self, layout):
        title = QLabel(self.name)
        title.setStyleSheet("font-size:14pt;")
        layout.addWidget(title)
        self.setupSearch(layout)

    def setupSearch(self, box):
        searchBar = QLineEdit()
        searchBar.textChanged.connect(self.filterLines)
        box.addWidget(searchBar)

    def filterLines(self, text):
        for w in self.typeWidgets:
            if text.lower() in w.name.lower():
                w.show()
            else:
                w.hide()

    def addlinegrid(self, vbox, typeName, fieldObject):
        labFrame = self.LabelFrame(typeName, fieldObject)
        vbox.addWidget(labFrame)
        self.typeWidgets.append(labFrame)
    
    class LabelFrame(QFrame):
        def __init__(self, typeName, fieldObject):
            self.name = fieldObject['name']
            self.typeName = typeName
            self.fieldObject = fieldObject
            self.data = DataTarget().data
            self.datatarget = DataTarget.target['parameters']
            super().__init__() 
            labelframelayout = QGridLayout(self)
            self.fieldStyle = "color: hsl(200, 30%, 70%);"
            self.valueStyle = "color:hsl(200, 30%, 40%);"
            self.setupLabels(labelframelayout)
            self.setupDataWidgets(labelframelayout)      
           
            self.setStyleSheet("LabelFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
            self.updateInfo(self.checkbox, self.infobox, fieldObject)
        
        def setupDataWidgets(self, layout):
            checkbox = QCheckBox()
            self.checkbox = checkbox
            infobox = QLabel()
            self.infobox = infobox
            strategybox = QComboBox()
            self.strategybox = strategybox
            strategies = DataTarget().data['strategies']
            for i in strategies:
                strategybox.addItem(i)
            inputarea = QLineEdit()
            datahandlefunction = lambda fo=self.fieldObject, ia=inputarea, checkbox=checkbox, infobox=infobox, strategybox=strategybox : self.dataHandle(fo, ia, checkbox, strategybox, infobox)
            inputarea.editingFinished.connect(datahandlefunction)

            layout.addWidget(checkbox, 0, 4, 1, -1, Qt.AlignmentFlag.AlignRight)
            layout.addWidget(infobox, 1, 4, 1, -1)
            layout.addWidget(inputarea, 2, 4, 1, -1)
            layout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)
            
            layout.addWidget(strategybox, 3, 2, 1, -1)
            checkbox.checkStateChanged.connect(lambda x: datahandlefunction())
            strategybox.activated.connect(lambda index: datahandlefunction())
    
            layout.addWidget(checkbox, 0, 4, 1, -1, Qt.AlignmentFlag.AlignRight)
            layout.addWidget(infobox, 1, 4, 1, -1)
            layout.addWidget(inputarea, 2, 4, 1, -1)
            layout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)

        def setupLabels(self, layout):
            nameLabel0 = QLabel("name:")
            nameLabel0.setStyleSheet(self.fieldStyle)
            nameLabel1 = QLabel(f"{self.fieldObject["name"]}")
            nameLabel1.setStyleSheet(self.valueStyle)
            typeLabel0 = QLabel("type:")
            typeLabel0.setStyleSheet(self.fieldStyle)
            typeLabel1 = QLabel(f"{self.fieldObject["type"]}")
            typeLabel1.setStyleSheet(self.valueStyle)
            valueLabel0 = QLabel("value ex.:")
            valueLabel0.setStyleSheet(self.fieldStyle)
            valueLabel1 = QLabel(f"{self.fieldObject["value"]}")
            valueLabel1.setStyleSheet(self.valueStyle)
            layout.addWidget(packFrame([nameLabel0, nameLabel1], direction="H"), 0, 0, 1, 4)
            layout.addWidget(packFrame([typeLabel0, typeLabel1], direction="H"), 1, 0, 1, 4)
            layout.addWidget(packFrame([valueLabel0, valueLabel1], direction="H"), 2, 0, 1, 4)
            
        def updateInfo(self, checkbox, infobox, fieldObject):
            #below line is a hard to read line which tests if data on the field has been written to the target for data passing
            if(self.typeName in self.datatarget and fieldObject['name'] in self.datatarget[self.typeName] and self.datatarget[self.typeName][fieldObject['name']]!=[]):
                uiresults = self.datatarget[self.typeName][fieldObject['name']]
                infostring = ""
                for i in uiresults['values']:
                    infostring = infostring + f"{i}, "
                infostring = infostring + f"\n{uiresults["strategy"]}"
                infobox.setText(infostring)
                checkbox.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                infobox.setText("")
                    

        def addToTarget(self, fieldObject, values):
            typeName = self.typeName
            if typeName in self.datatarget:
                self.datatarget[typeName][fieldObject['name']] = values
            else:
                self.datatarget[typeName] = {}
                self.datatarget[typeName][fieldObject['name']] = values

        def dataHandle(self, fieldObject, inputarea, checkbox, strategybox, infobox):
            typeName = self.typeName
            if(checkbox.isChecked()):
                try:
                    values = inputarea.text().split(',')
                    if fieldObject['type'] in ["Single", "Double", "Short", "Long"]:
                       values = list(map(lambda x : float(x), values))
                    
                    strategy = strategybox.currentText()
                    if typeName not in self.datatarget:
                        self.datatarget[typeName] = {}
                    DataTarget().updateParameterField(typeName, fieldObject['name'], values, strategy)
                except Exception as e:
                    checkbox.setCheckState(Qt.CheckState.Unchecked)
                    ErrorPopup(str(e))
                    return
            else: 
                DataTarget().removeFromParameterField(typeName, fieldObject['name'])
            self.updateInfo(checkbox, infobox, fieldObject)

