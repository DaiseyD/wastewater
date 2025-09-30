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

# the TypeWindow is a window which shows all fields of a parameter and allows for the modifying of said field for simulations
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
        gridbox = QGridLayout(container)
        # gridbox = QVBoxLayout(container)
        gridbox.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.typeWidgets = []
        i = 0
        for (index,item) in enumerate(self.data['fields']):
            fieldFrame = self.addlinegrid(typeName, item)
            horizIndex = index % 3
            vertIndex = index // 3
            gridbox.addWidget(fieldFrame, vertIndex, horizIndex)
        scrollArea.setWidget(container)


    def initTitleAndSearch(self, layout):
        title = QLabel(self.name)
        title.setStyleSheet("font-size:16pt;")
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

    def addlinegrid(self, typeName, fieldObject):
        labFrame = self.LabelFrame(typeName, fieldObject)
        self.typeWidgets.append(labFrame)
        return labFrame

    # the labelframe contains a single field of a parameter, it can be used to modify said field for the simulations
    class LabelFrame(QFrame):
        def __init__(self, typeName, fieldObject):
            self.name = fieldObject['name']
            self.typeName = typeName
            self.fieldObject = fieldObject
            self.data = DataTarget().data
            self.datatarget = DataTarget.target['parameters']
            self.baseStyle = "LabelFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}"
            super().__init__() 
            labelframelayout = QGridLayout(self)
            self.fieldStyle = "color: hsl(200, 30%, 70%);"
            self.valueStyle = "color: hsl(200, 30%, 40%);"
            self.setupLabels(labelframelayout)
            self.setupDataWidgets(labelframelayout)      
           
            self.setStyleSheet(self.baseStyle)
        
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
            
            layout.addWidget(checkbox, 0, 4, 1, -1, Qt.AlignmentFlag.AlignRight)
            layout.addWidget(infobox, 1, 4, 1, -1)
            layout.addWidget(inputarea, 2, 4, 1, -1)
            layout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)
            layout.addWidget(strategybox, 3, 2, 1, -1)
            self.updateInfo(self.checkbox, self.infobox, self.fieldObject)

            inputarea.editingFinished.connect(datahandlefunction)
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
            

        def setInfoString(self, checkbox, infobox, fieldObject):
            if(self.typeName in self.datatarget and fieldObject['name'] in self.datatarget[self.typeName] and self.datatarget[self.typeName][fieldObject['name']]!=[]):
                uiresults = self.datatarget[self.typeName][fieldObject['name']]
                infostring = ""
                for i in uiresults['values']:
                    infostring = infostring + f"{i}, "
                infostring = infostring + f"\n{uiresults["strategy"]}"
                infobox.setText(infostring)
            else:
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                infobox.setText("")

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
                    basevalues = inputarea.text().split(',')
                    if fieldObject['type'] in ["Single", "Double", "Short", "Long"]:
                       values = list(map(lambda x : float(x), basevalues))
                    elif fieldObject['type'] == "Boolean":
                        aux = []
                        for val in basevalues:
                            if val.lower() == "true":
                                aux.append(True)
                            elif val.lower() == "false":
                                aux.append(False)
                            else:
                                raise(Exception("value must be true or false"))
                        values = aux
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
    