from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.popup import ErrorPopup
from components.DataTarget import DataTarget
from components.TypeWindow import TypeWindow
from style import *

# The parameter frame is a part of the main window that shows each parameter and opens a TypeWindow when clicking the parameter
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
        styleAppend("color: hsl(200, 30%, 10%); font-size:16px;", title)
        rightLayout.addWidget(title)
        description = QLabel("Select a type to manipulate the fields of elements of that type")
        styleAppend(TEXT_SEMIHIGHLIGHT, description)
        description.setWordWrap(True)
        rightLayout.addWidget(description)
        for (index, typeName) in enumerate(self.data['networkobjects'].keys()):
            button = QPushButton(f"{index} {typeName} ({self.data['networkobjects'][typeName]['length']})")
            styleAppend("color: hsl(200, 30%, 20%); padding: 10px 2px;",button)
            button.clicked.connect(lambda checked, typeName=typeName: self.openTypeWindow(typeName))
            rightLayout.addWidget(button)
        
        scrollLeft.setWidget(container)
    
    def openTypeWindow(self, item):
        self.w = TypeWindow(item)
        self.w.setGeometry(0,0, 1200, 800)
        self.w.show()
