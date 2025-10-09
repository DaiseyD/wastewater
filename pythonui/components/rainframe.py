from PySide6.QtWidgets import *
from PySide6.QtCore import *
from components.DataTarget import DataTarget
from style import *
import json

# A frame which contains all the rainfallevents and allows to select them to enable them in the simulation
class RainFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.raindata = DataTarget().data['rainfallevents']
        self.targetdata = DataTarget.target
        vbox = QVBoxLayout(self)
        scrollRight = QScrollArea()
        vbox.addWidget(scrollRight)
        rightContainer = QFrame()
        hbox = QHBoxLayout(rightContainer)
        rainContainer = QFrame()
        hbox.addWidget(rainContainer)
        rainLayout = QVBoxLayout(rainContainer)
        self.setupRain(rainLayout)
        rainLayout.addStretch() # align elements to top
        scrollRight.setWidget(rightContainer)

    def setupRain(self, rainLayout):
        title = QLabel("<b>Rainfall events</b>")
        rainLayout.addWidget(title)
        for (index, rainfallevent) in enumerate(self.raindata):
            rainholder = QFrame()
            rainLayout.addWidget(rainholder)
            rainhbox = QHBoxLayout(rainholder)
            # rainhbox.addWidget(QLabel(f"{rainfallevent['id']}: {rainfallevent['name']}"))
            idLabel = QLabel(f"{rainfallevent['id']}:")
            idLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            styleAppend(TEXT_SEMIHIDDEN, idLabel)
            rainhbox.addWidget(idLabel, 0, Qt.AlignmentFlag.AlignLeft)
            rainnameLabel = QLabel(f"{rainfallevent['name']}")
            styleAppend(TEXT_PLAIN, rainnameLabel)
            rainhbox.addWidget(rainnameLabel, 0, Qt.AlignmentFlag.AlignCenter)
            checkbox = QCheckBox()
            rainhbox.addWidget(checkbox, 0, Qt.AlignmentFlag.AlignRight)
            checkbox.clicked.connect(lambda state, id=rainfallevent['id']: self.selectRainEvent(state,id))

    def selectRainEvent(self,state, id):
        if state == True:
            self.targetdata['rainfallevents'].append(id)
        else:
            self.targetdata['rainfallevents'].remove(id)
        print(self.targetdata)


