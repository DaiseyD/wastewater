import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import style
import json

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

def getjsondata():
    try:
        with(open("testcopy.json", "r")) as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)

def writejsonresult(result):
    try:
        with(open("uiresults.json", "w")) as f:
            f.write(json.dumps(result))

    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        exit(1)

class Wastewindow(QMainWindow):
    
    def __init__(self, data, datatarget):
        self.data = data
        self.datatarget = datatarget
        super().__init__()
        self.setWindowTitle("My App")
        self.frame = QFrame()
        self.hbox = QHBoxLayout(self.frame)        
        self.setCentralWidget(self.frame)
        self.setLeftFrame()
        self.setRightFrame()


    def setLeftFrame(self):  
        leftFrame = QFrame()
        self.hbox.addWidget(leftFrame)
        vboxl = QVBoxLayout(leftFrame)
        scrollLeft = QScrollArea()
        vboxl.addWidget(scrollLeft)
        leftContainer = QFrame()
        rightLayout= QVBoxLayout(leftContainer)
        nodeTypeTitle = QLabel("Node types")
        nodeTypeTitle.setStyleSheet("color: hsl(200, 30%, 10%); font-size:16px;")
        rightLayout.addWidget(nodeTypeTitle)
        for (index,item) in enumerate(self.data["networkobjects"]):
            button = QPushButton(f"{index} {item['name']}")
            button.setStyleSheet("color: hsl(200, 30%, 20%); padding: 10px 2px;")
            button.clicked.connect(lambda checked, item=item: self.openTypeWindow(item))
            rightLayout.addWidget(button)
            
        scrollLeft.setWidget(leftContainer)

    def setRightFrame(self):
        rightFrame = QFrame()
        self.hbox.addWidget(rightFrame)
        vboxr = QVBoxLayout(rightFrame)
        scrollRight = QScrollArea()
        vboxr.addWidget(scrollRight)
        rightContainer = QFrame()
        rightLayout = QVBoxLayout(rightContainer)

        for (index, rainfallevent) in enumerate(self.data['rainfallevents']):
            rainholder = QFrame()
            rightLayout.addWidget(rainholder)
            rainhbox = QHBoxLayout(rainholder)
            rainhbox.addWidget(QLabel(f"{index} {rainfallevent['name']}"))
            rainhbox.addWidget(QCheckBox())
            # rightLayout.addWidget(QLabel(f"{index} {rainfallevent['name']}"))

        scrollRight.setWidget(rightContainer)
    
    def openTypeWindow(self, item):
        self.w = TypeWindow(item, self.datatarget)
        self.w.show()

class RandomWindow(QWidget):
    pass


class TypeWindow(QWidget):

    def __init__(self, dataobject, datatarget):
        super().__init__()
        self.data = dataobject
        self.target = datatarget       
        vboxbase = QVBoxLayout(self)
        scrollArea = QScrollArea()
        vboxbase.addWidget(scrollArea)
        container = QFrame()
        gridbox = QVBoxLayout(container)
        title = QLabel(dataobject['name'])
        title.setStyleSheet("font-size:14pt;")
        gridbox.addWidget(title)
        for (index,item) in enumerate(dataobject["fields"]):
            self.addlinegrid(gridbox, index)
        scrollArea.setWidget(container)


    def addlinegrid(self, vbox, index):
        fieldobject = self.data['fields'][index]
        labFrame = self.LabelFrame(fieldobject, self)
        vbox.addWidget(labFrame, index)

    
    class LabelFrame(QFrame):
        def __init__(self, fieldobject, parent):
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
            inputarea = QLineEdit()
            infobox = QLabel()
            checkbox.clicked.connect(lambda x, fieldobject=fieldobject, values=inputarea, checkbox=checkbox, infobox=infobox : self.parent.handlecheckbox(x, fieldobject, values, checkbox, infobox))
            labelframelayout.addWidget(checkbox, 0, 4, 1, -1)
            labelframelayout.addWidget(infobox, 1, 4, 1, -1)
            labelframelayout.addWidget(inputarea, 2, 4, 1, -1)
            labelframelayout.addWidget(QLabel("Strategy:"), 3, 0, 1, 2)
            dropdown = QComboBox()
            dropdown.addItem("randomselect")
            dropdown.addItem("randomrange")
            dropdown.addItem("changeall")
            labelframelayout.addWidget(dropdown, 3, 2, 1, -1)

            
            self.setStyleSheet("LabelFrame{border-color: hsl(200, 30%, 20%); border-width: 1; border-style: solid; border-radius: 5;}")
            self.parent.updateInfo(checkbox, infobox, fieldobject)

    def updateInfo(self, checkbox, infobox, fieldobject):
        # aux = self.target[self.data['name']]
        #below line is a hard to read line which tests if data on the field has been written to the target for data passing
        if(self.data['name'] in self.target and fieldobject['name'] in self.target[self.data['name']] and self.target[self.data['name']][fieldobject['name']]!=[]):
            values =  self.target[self.data['name']][fieldobject['name']]
            infostring = ""
            for i in values:
                infostring = infostring + f"{i},"
                infobox.setText(infostring)
                checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            infobox.setText("")
                    
    def handlecheckbox(self, state, object, inputarea, checkbox, infobox):
        values = inputarea.text().split(',')
        numvalues = list(map(lambda x : float(x), values))
        print(numvalues)
        if (state==True):
            self.addToTarget(object, numvalues)
        else:
            self.removeFromTarget(object)
        self.updateInfo(checkbox, infobox, object)

    def addToTarget(self, fieldobject, values):
        propname = self.data['name']
        if propname in self.target:
            self.target[propname][fieldobject['name']] = values
        else:
            self.target[propname] = {}
            self.target[propname][fieldobject['name']] = values


    def removeFromTarget(self, fieldobject):
        propname = self.data['name']
        self.target[propname].pop(fieldobject['name'])
        if(self.target[propname] == None):
            self.target.pop(propname)





# Create the Qt Application
app = QApplication(sys.argv)
app.setStyleSheet(style.STYLEGLOBAL)
result = {}
mainwindow = Wastewindow(getjsondata(), result)
# Create a button, connect it and show it

mainwindow.show()
# Run the main Qt loop
app.exec()

writejsonresult(result)

