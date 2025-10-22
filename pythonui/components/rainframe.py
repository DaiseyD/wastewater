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
        self.target = DataTarget()
        vbox = QVBoxLayout(self)
        scrollRight = QScrollArea()
        vbox.addWidget(scrollRight)
        rightContainer = QFrame()
        hbox = QHBoxLayout(rightContainer)
        rainContainer = QFrame()
        hbox.addWidget(rainContainer)
        rainLayout = QVBoxLayout(rainContainer)
        self.setTitleDesc(rainLayout)
        self.setupRain(rainLayout)
        rainLayout.addStretch() # align elements to top
        scrollRight.setWidget(rightContainer)

    def setupRain(self, rainLayout):

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

    def setTitleDesc(self, layout):
        title = QLabel("Rainfall events")
        styleAppend(TEXT_HIGHLIGHT, title)
        layout.addWidget(title)
        description = QLabel("Select the rainfall events you wish to include in the simulation")
        styleAppend(TEXT_SEMIHIGHLIGHT, description)
        description.setWordWrap(True)
        layout.addWidget(description)

    def selectRainEvent(self,state, id):
        if state == True:
            self.target.addToRain(id)
        else:
            self.target.removeFromRain(id)


