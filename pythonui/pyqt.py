import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import json



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
        leftContainer = QWidget()
        rightLayout= QVBoxLayout(leftContainer)
        for (index,item) in enumerate(self.data["networkobjects"]):
            button = QPushButton(f"{index} {item['name']}")
            button.clicked.connect(lambda checked, item=item: self.openTypeWindow(item))
            rightLayout.addWidget(button)
            
        scrollLeft.setWidget(leftContainer)

    def setRightFrame(self):
        rightFrame = QFrame()
        self.hbox.addWidget(rightFrame)
        vboxr = QVBoxLayout(rightFrame)
        scrollRight = QScrollArea()
        vboxr.addWidget(scrollRight)
        rightContainer = QWidget()
        rightLayout = QVBoxLayout(rightContainer)

        for (index, rainfallevent) in enumerate(self.data['rainfallevents']):
            rainholder = QWidget()
            rightLayout.addWidget(rainholder)
            rainhbox = QHBoxLayout(rainholder)
            rainhbox.addWidget(QLabel(f"{index} {rainfallevent['name']}"))
            rainhbox.addWidget(QCheckBox())
            # rightLayout.addWidget(QLabel(f"{index} {rainfallevent['name']}"))

        scrollRight.setWidget(rightContainer)
    
    def openTypeWindow(self, item):
        self.w = TypeWindow(item, self.datatarget)
        self.w.show()

class TypeWindow(QWidget):

    def __init__(self, dataobject, datatarget):
        super().__init__()
        self.data = dataobject
        self.target = datatarget        
        vboxbase = QVBoxLayout(self)
        scrollArea = QScrollArea()
        vboxbase.addWidget(scrollArea)
        container = QWidget()
        vboxscroll = QVBoxLayout(container)
        title = QLabel(dataobject['name'])
        title.setStyleSheet("font-size:14pt;")
        vboxscroll.addWidget(title)
        for (index,item) in enumerate(dataobject["fields"]):
            self.addline(vboxscroll, index)
        scrollArea.setWidget(container)


    def addline(self, vbox, index):
        f = QFrame()
        vbox.addWidget(f)
        fieldobject = self.data['fields'][index]

        hbox = QHBoxLayout(f)
        label = QLabel(f"{fieldobject}")
        hbox.addWidget(label)

        if(fieldobject['type'] in ["Double","Long", "Short", "Single"]):   
            checkbox = QCheckBox()
            inputarea = QLineEdit()
            checkbox.clicked.connect(lambda x, fieldobject=fieldobject, values=inputarea : self.handlecheckbox(x, fieldobject, values))
            hbox.addWidget(checkbox)
            hbox.addWidget(inputarea)

    def handlecheckbox(self, state, object, inputarea):
        print(inputarea.text())
        values = inputarea.text().split(',')
        numvalues = list(map(lambda x : float(x), values))
        print(numvalues)
        if (state==True):
            self.addToTarget(object, numvalues)
        else:
            self.removeFromTarget(object)
        print(self.target)

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
result = {}
mainwindow = Wastewindow(getjsondata(), result)
# Create a button, connect it and show it

mainwindow.show()
# Run the main Qt loop
app.exec()

writejsonresult(result)

