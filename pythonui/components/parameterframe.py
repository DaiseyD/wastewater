from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup

def packFrame(widgets, direction):
    frame = QFrame()
    if(direction=='V'):
        layout = QVBoxLayout(frame)
    elif (direction=="H"):
        layout = QHBoxLayout(frame)
    else: 
        raise Exception("wrong argument to pack frame")
    for w in widgets:
        layout.addWidget(w)
    return frame


class ParameterFrame(QFrame):

    def __init__(self, objectdata, datatarget, strategies):
        super().__init__()
        if 'parameters' not in datatarget.keys():
            datatarget['parameters'] = {}
        self.datatarget = datatarget['parameters']
        self.objectdata = objectdata
        vbox = QVBoxLayout(self)
        scrollLeft = QScrollArea()
        vbox.addWidget(scrollLeft)
        container = QFrame()
        rightLayout= QVBoxLayout(container)
        title = QLabel("Parameters")
        title.setStyleSheet("color: hsl(200, 30%, 10%); font-size:16px;")
        rightLayout.addWidget(title)
        for (index,item) in enumerate(self.objectdata):
            button = QPushButton(f"{index} {item['name']}")
            button.setStyleSheet("color: hsl(200, 30%, 20%); padding: 10px 2px;")
            button.clicked.connect(lambda checked, item=item: self.openTypeWindow(item, strategies))
            rightLayout.addWidget(button)
            
        scrollLeft.setWidget(container)
    
    def openTypeWindow(self, item, strategies):
        self.w = TypeWindow(item, self.datatarget, strategies)
        self.w.show()

class TypeWindow(QWidget):
    def __init__(self, dataobject, datatarget, strategies):
        super().__init__()
        self.data = dataobject
        self.datatarget = datatarget
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
        for (index,item) in enumerate(dataobject["fields"]):
            self.addlinegrid(gridbox, index, strategies)
        scrollArea.setWidget(container)


    def initTitleAndSearch(self, layout):
        title = QLabel(self.data['name'])
        title.setStyleSheet("font-size:14pt;")
        layout.addWidget(title)
        self.setupSearch(layout)

    def setupSearch(self, box):
        searchBar = QLineEdit()
        searchBar.textChanged.connect(self.updateDisplay)
        box.addWidget(searchBar)

    def updateDisplay(self, text):
        for w in self.typeWidgets:
            if text.lower() in w.name.lower():
                w.show()
            else:
                w.hide()

    def addlinegrid(self, vbox, index, strategies):
        fieldobject = self.data['fields'][index]
        labFrame = self.LabelFrame(fieldobject, self, strategies)
        vbox.addWidget(labFrame, index)
        labFrame.name = fieldobject['name']
        self.typeWidgets.append(labFrame)

    
    class LabelFrame(QFrame):
        def __init__(self, fieldobject, parent, strategies):
            self.parent = parent
            super().__init__() 
            labelframelayout = QGridLayout(self)
            styleForField = "color: hsl(200, 30%, 70%);"
            styleForValue = "color:hsl(200, 30%, 40%);"
            nameLabel0 = QLabel("name:")
            nameLabel0.setStyleSheet(styleForField)
            nameLabel1 = QLabel(f"{fieldobject["name"]}")
            nameLabel1.setStyleSheet(styleForValue)
            typeLabel0 = QLabel("type:")
            typeLabel0.setStyleSheet(styleForField)
            typeLabel1 = QLabel(f"{fieldobject["type"]}")
            typeLabel1.setStyleSheet(styleForValue)
            valueLabel0 = QLabel("value ex.:")
            valueLabel0.setStyleSheet(styleForField)
            valueLabel1 = QLabel(f"{fieldobject["value"]}")
            valueLabel1.setStyleSheet(styleForValue)
            labelframelayout.addWidget(packFrame([nameLabel0, nameLabel1], direction="H"), 0, 0, 1, 4)
            labelframelayout.addWidget(packFrame([typeLabel0, typeLabel1], direction="H"), 1, 0, 1, 4)
            labelframelayout.addWidget(packFrame([valueLabel0, valueLabel1], direction="H"), 2, 0, 1, 4)
            checkbox = QCheckBox()
            infobox = QLabel()
            strategybox = QComboBox()
            for i in strategies:
                strategybox.addItem(i)

            if(fieldobject["type"] == "Boolean"):
                inputarea=QComboBox()
                inputarea.addItem("True")
                inputarea.addItem("False")
            else: 
                inputarea = QLineEdit()

            datahandlefunction = lambda fieldobject=fieldobject, inputarea=inputarea, checkbox=checkbox, infobox=infobox, strategybox=strategybox : self.parent.dataHandle(fieldobject, inputarea, checkbox, strategybox, infobox)
            if(fieldobject["type"] == "Boolean"):
                inputarea.activated.connect(lambda index: datahandlefunction())
            else: 
                inputarea.editingFinished.connect(datahandlefunction)

            labelframelayout.addWidget(checkbox, 0, 4, 1, -1, Qt.AlignmentFlag.AlignRight)
            labelframelayout.addWidget(infobox, 1, 4, 1, -1)
            labelframelayout.addWidget(inputarea, 2, 4, 1, -1)
            labelframelayout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)
            
            labelframelayout.addWidget(strategybox, 3, 2, 1, -1)
            checkbox.checkStateChanged.connect(lambda x: datahandlefunction())
            strategybox.activated.connect(lambda index: datahandlefunction())
    

            labelframelayout.addWidget(checkbox, 0, 4, 1, -1, Qt.AlignmentFlag.AlignRight)
            labelframelayout.addWidget(infobox, 1, 4, 1, -1)
            labelframelayout.addWidget(inputarea, 2, 4, 1, -1)
            labelframelayout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)
            self.setStyleSheet("LabelFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
            self.parent.updateInfo(checkbox, infobox, fieldobject)
            

    def updateInfo(self, checkbox, infobox, fieldobject):
        #below line is a hard to read line which tests if data on the field has been written to the target for data passing
        if(self.data['name'] in self.datatarget and fieldobject['name'] in self.datatarget[self.data['name']] and self.datatarget[self.data['name']][fieldobject['name']]!=[]):
            uiresults = self.datatarget[self.data['name']][fieldobject['name']]
            infostring = ""
            for i in uiresults['values']:
                infostring = infostring + f"{i}, "
            infostring = infostring + f"\n{uiresults["strategy"]}"
            infobox.setText(infostring)
            checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            infobox.setText("")
                    

    def addToTarget(self, fieldobject, values):
        typeName = self.data['name']
        if typeName in self.datatarget:
            self.datatarget[typeName][fieldobject['name']] = values
        else:
            self.datatarget[typeName] = {}
            self.datatarget[typeName][fieldobject['name']] = values

    def dataHandle(self, fieldobject, inputarea, checkbox, strategybox, infobox):
        if(fieldobject['type'] in ["Single", "Double", "Short", "Long"]): 
            self.dataHandleNum(fieldobject, inputarea, checkbox, strategybox, infobox)
        elif fieldobject['type'] == "Boolean":
            self.datahandleBool(fieldobject, inputarea, checkbox, strategybox, infobox)
            
        else:
            ErrorPopup("Unsupported type found")


    def datahandleBool(self, fieldobject, inputarea, checkbox, strategybox, infobox):
        typeName = self.data['name']
        if(checkbox.isChecked()):
            try:
                value = inputarea.currentText()=="True"
                strategy = strategybox.currentText()
                if typeName not in self.datatarget:
                    self.datatarget[typeName] = {}
                self.datatarget[typeName][fieldobject['name']] = {}
                self.datatarget[typeName][fieldobject['name']]['values'] = [value]
                self.datatarget[typeName][fieldobject['name']]['strategy'] = strategy
            except Exception as e:
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                ErrorPopup(str(e))
                return
        else: 
            if(typeName not in self.datatarget.keys()):
                pass
            else: 
                try:
                    self.datatarget[typeName].pop(fieldobject['name'])
                except KeyError as ke:
                    pass
                if(self.datatarget[typeName] == None):
                    self.datatarget.pop(typeName)
        self.updateInfo(checkbox, infobox, fieldobject)
        print(self.datatarget)


    def dataHandleNum(self, fieldobject, inputarea, checkbox, strategybox, infobox):
        typeName = self.data['name']
        if(checkbox.isChecked()):
            try:
                values = inputarea.text().split(',')
                numvalues = list(map(lambda x : float(x), values))
                strategy = strategybox.currentText()
                if typeName not in self.datatarget:
                    self.datatarget[typeName] = {}
                self.datatarget[typeName][fieldobject['name']] = {}
                self.datatarget[typeName][fieldobject['name']]['values'] = numvalues
                self.datatarget[typeName][fieldobject['name']]['strategy'] = strategy
            except Exception as e:
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                ErrorPopup(str(e))
                return
        else: 
            if(typeName not in self.datatarget.keys()):
                pass
            else: 
                try:
                    self.datatarget[typeName].pop(fieldobject['name'])
                except KeyError as ke:
                    pass
                if(self.datatarget[typeName] == None):
                    self.datatarget.pop(typeName)
        self.updateInfo(checkbox, infobox, fieldobject)
        print(self.datatarget)

