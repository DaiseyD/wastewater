from PySide6.QtWidgets import *
from PySide6.QtCore import *
import json


class RainFrame(QFrame):
    def __init__(self, raindata, targetdata):
        super().__init__()
        self.raindata = raindata
        self.targetdata = targetdata
        vbox = QVBoxLayout(self)
        title = QLabel("Rainfall events")
        vbox.addWidget(title)
        scrollRight = QScrollArea()
        vbox.addWidget(scrollRight)
        rightContainer = QFrame()
        rightLayout = QVBoxLayout(rightContainer)

        for (index, rainfallevent) in enumerate(raindata):
            rainholder = QFrame()
            rightLayout.addWidget(rainholder)
            rainhbox = QHBoxLayout(rainholder)
            rainhbox.addWidget(QLabel(f"{rainfallevent['id']}: {rainfallevent['name']}"))
            checkbox = QCheckBox()
            rainhbox.addWidget(checkbox)
            checkbox.clicked.connect(lambda state, id=rainfallevent['id']: self.selectRainEvent(state,id))
            # rightLayout.addWidget(QLabel(f"{index} {rainfallevent['name']}"))
        scrollRight.setWidget(rightContainer)

    def selectRainEvent(self,state, id):
        if "rainfallevents" not in self.targetdata.keys():
            self.targetdata['rainfallevents'] = []  
        if state == True:
            self.targetdata['rainfallevents'].append(id)
        else:
            self.targetdata['rainfallevents'].remove(id)
        print(self.targetdata)


