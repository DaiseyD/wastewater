from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget
from style import *
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
    searchBar = None
    typeFilter = None
    def __init__(self, typeName):
        super().__init__()
        self.name = typeName
        self.data = DataTarget().data['networkobjects'][typeName]
        self.datatarget = DataTarget().target['parameters']
        vboxBase = QVBoxLayout(self)
        frameTop = QFrame()
        vboxBase.addWidget(frameTop)
        vboxTop = QVBoxLayout(frameTop)
        filterLayout = QHBoxLayout()
        self.initTitle(vboxTop)
        vboxTop.addLayout(filterLayout)
        self.initFilters(filterLayout)
        frameBottom = QFrame()
        vboxBase.addWidget(frameBottom)
        boxCard = QVBoxLayout(frameBottom)
        scrollArea = QScrollArea()
        boxCard.addWidget(scrollArea)
        container = QFrame()
        gridbox = QVBoxLayout(container)
        self.typeWidgets = []

        for (index,item) in enumerate(self.data['fields']):
            fieldFrame = self.addlinegrid(typeName, item)
            gridbox.addWidget(fieldFrame, 0)
            self.addToTypeFilter(item['type'])
        scrollArea.setWidget(container)
        scrollArea.setWidgetResizable(True)

    def initTitle(self, layout):
        title = QLabel(self.name)
        styleAppend("font-size:16pt;", title)
        layout.addWidget(title)

    def initFilters(self, layout):
        self.searchBar = QLineEdit()
        self.searchBar.textChanged.connect(self.applyFilters)
        layout.addWidget(self.searchBar,1)
        self.typeFilter = QComboBox()
        self.typeFilter.addItem("all")
        self.typeFilter.activated.connect(self.applyFilters)
        layout.addWidget(self.typeFilter,1)
    

    def applyFilters(self):
        searchText = self.searchBar.text()
        typeText = self.typeFilter.currentText()
        for w in self.typeWidgets:
            if searchText.lower() in w.name.lower() and (typeText == w.fieldObject['type'] or typeText.lower()=="all"):
                w.show()
            else:
                w.hide()

    def addToTypeFilter(self, value):
        if value not in [self.typeFilter.itemText(i) for i in range(self.typeFilter.count())]:
            self.typeFilter.addItem(value)

    def addlinegrid(self, typeName, fieldObject):
        labFrame = self.LabelFrame(typeName, fieldObject)
        self.typeWidgets.append(labFrame)
        return labFrame

    # the labelframe contains a single field of a parameter, it can be used to modify said field for the simulations
    class LabelFrame(QFrame):
        def __init__(self, typeName, fieldObject):
            super().__init__() 
            self.name = fieldObject['name']
            self.typeName = typeName
            self.fieldObject = fieldObject
            self.data = DataTarget().data
            self.datatarget = DataTarget.target['parameters']
            self.baseStyle = """
                *[selected="true"]{background-color: hsl(80, 100%, 60%);}
                LabelFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}
                """
            baselayout = QHBoxLayout(self)
            infoframe = QFrame()
            infolayout = QVBoxLayout(infoframe)
            inputframe = QFrame()
            inputlayout = QVBoxLayout(inputframe)
            baselayout.addWidget(infoframe,1)
            baselayout.addWidget(inputframe,1)
            self.setupLabels(infolayout)
            self.setupDataWidgets(inputlayout)         
            self.setStyleSheet(self.baseStyle)
        
        def setupDataWidgets(self, layout):
            checkbox = QCheckBox()
            self.checkbox = checkbox
            infobox = QLabel()
            self.infobox = infobox
            strategybox = QComboBox()
            self.strategybox = strategybox
            styleAppend("* { font-size: 16px; }", self.strategybox)
            strategies = DataTarget().data['strategies']
            for i in strategies:
                strategybox.addItem(i)
            inputarea = QLineEdit()
            self.updateInfo(self.checkbox, self.infobox, self.fieldObject)

            datahandlefunction = lambda fo=self.fieldObject, ia=inputarea, checkbox=checkbox, infobox=infobox, strategybox=strategybox : self.dataHandle(fo, ia, checkbox, strategybox, infobox)          
            inputarea.editingFinished.connect(datahandlefunction)
            checkbox.checkStateChanged.connect(lambda x: datahandlefunction())
            strategybox.activated.connect(lambda index: datahandlefunction())
    
            layout.addWidget(checkbox)
            layout.addWidget(infobox)
            layout.addWidget(inputarea)
            layout.addWidget(QLabel("Strategy:"))
            layout.addWidget(strategybox)

        def setupLabels(self, layout):
            nameLabel0 = QLabel("name:")
            styleAppend(TEXT_SEMIHIDDEN, nameLabel0)
            nameLabel1 = QLabel(f"{self.fieldObject["name"]}")
            styleAppend(TEXT_SEMIHIGHLIGHT, nameLabel1)
            typeLabel0 = QLabel("type:")
            styleAppend(TEXT_SEMIHIDDEN, typeLabel0)
            typeLabel1 = QLabel(f"{self.fieldObject["type"]}")
            styleAppend(TEXT_SEMIHIGHLIGHT, typeLabel1)
            valueLabel0 = QLabel("value ex.:")
            styleAppend(TEXT_SEMIHIDDEN, valueLabel0)
            valueLabel1 = QLabel(f"{self.fieldObject["value"]}")
            styleAppend(TEXT_SEMIHIGHLIGHT, valueLabel1)
            layout.addWidget(packFrame([nameLabel0, nameLabel1], direction="H"))
            layout.addWidget(packFrame([typeLabel0, typeLabel1], direction="H"))
            layout.addWidget(packFrame([valueLabel0, valueLabel1], direction="H"))
            

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
                self.setProperty("selected", True)
            else:
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                infobox.setText("")
                self.setProperty("selected", False)
            self.setStyleSheet(self.styleSheet()) # this seems to be the only way to make dynamic styling properties work
                    

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
                    else:
                        values = basevalues
                    strategy = strategybox.currentText()
                    if typeName not in self.datatarget:
                        self.datatarget[typeName] = {}
                    DataTarget().updateParameterField(typeName, fieldObject['name'], values, strategy)
                    self.setProperty("selected", True)
                except Exception as e:
                    checkbox.setCheckState(Qt.CheckState.Unchecked)
                    self.setProperty("selected", False)
                    ErrorPopup(f"Error parsing input into values:\n{str(e)}")
                    return
            else: 
                DataTarget().removeFromParameterField(typeName, fieldObject['name'])
                self.setProperty("selected", False)
            self.updateInfo(checkbox, infobox, fieldObject)

    