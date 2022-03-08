from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QCheckBox, QWidget


states = [False, False, False, False, False, False, False]  # A, B, C, D, E, F, G
option_move_mouse = 0


def checkBoxChangedActionA(state):
    if QtCore.Qt.Checked == state:
        states[0] = True
    else:
        states[0] = False


def checkBoxChangedActionB(state):
    if QtCore.Qt.Checked == state:
        states[1] = True
    else:
        states[1] = False


def checkBoxChangedActionC(state):
    if QtCore.Qt.Checked == state:
        states[2] = True
    else:
        states[2] = False


def checkBoxChangedActionD(state):
    if QtCore.Qt.Checked == state:
        states[3] = True
    else:
        states[3] = False


def checkBoxChangedActionE(state):
    if QtCore.Qt.Checked == state:
        states[4] = True
    else:
        states[4] = False


def checkBoxChangedActionF(state):
    if QtCore.Qt.Checked == state:
        states[5] = True
    else:
        states[5] = False


def checkBoxChangedActionG(state):
    if QtCore.Qt.Checked == state:
        states[6] = True
    else:
        states[6] = False


def index_changed(i):
    global option_move_mouse
    option_move_mouse = i


class ToolBar(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu")
        self.resize(380, 350)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label2 = QLabel("Alertas são exibidos aqui!", self)
        self.label2.setStyleSheet("color: red;")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setWordWrap(True)

        self.layout.addWidget(self.label2)

        self.checkBoxA = QCheckBox("Abrir teclado com os dois olhos fechados")
        self.checkBoxB = QCheckBox("Clicar com o olho esquerdo")
        self.checkBoxC = QCheckBox("Clicar com o olho direito")
        self.checkBoxD = QCheckBox("Rolar com o dedinho")
        self.checkBoxE = QCheckBox("Dois dedos (duplo clique), Três dedos (arrastar)")
        self.checkBoxF = QCheckBox("Cliques com a orientação da palma da mão")
        self.checkBoxG = QCheckBox("Movimentar o mouse")

        self.checkBoxA.stateChanged.connect(checkBoxChangedActionA)
        self.checkBoxB.stateChanged.connect(checkBoxChangedActionB)
        self.checkBoxC.stateChanged.connect(checkBoxChangedActionC)
        self.checkBoxD.stateChanged.connect(checkBoxChangedActionD)
        self.checkBoxE.stateChanged.connect(checkBoxChangedActionE)
        self.checkBoxF.stateChanged.connect(checkBoxChangedActionF)
        self.checkBoxG.stateChanged.connect(checkBoxChangedActionG)

        self.checkBoxA.setChecked(True)
        self.checkBoxE.setChecked(True)
        self.checkBoxG.setChecked(True)

        self.layout.addWidget(self.checkBoxA)
        self.layout.addWidget(self.checkBoxB)
        self.layout.addWidget(self.checkBoxC)
        self.layout.addWidget(self.checkBoxD)
        self.layout.addWidget(self.checkBoxE)
        self.layout.addWidget(self.checkBoxF)
        self.layout.addWidget(self.checkBoxG)

        self.widget = QComboBox()
        self.widget.addItems(["Palma da mão", "Rosto", "Dedo indicador", "Dedo polegar", "Dedo médio", "Dedo anelar",
                              "Dedinho", "Movimentar o mouse com a direção do olhar", "Movimentar o mouse com a direção do olhar e dedo"])
        self.widget.currentIndexChanged.connect(index_changed)

        self.layout.addWidget(self.widget)

        self.button = QPushButton('Fechar', self)
        self.button.setToolTip('This is an example button')
        self.button.setBaseSize(60, 20)
        self.layout.addWidget(self.button)

        self.show()

    def statea(self):
        return states[0]

    def stateb(self):
        return states[1]

    def statec(self):
        return states[2]

    def stated(self):
        return states[3]

    def statee(self):
        return states[4]

    def statef(self):
        return states[5]

    def stateg(self):
        return states[6]

    def option_select(self):
        return option_move_mouse

    def update(self):
        if not states[6]:
            self.widget.setDisabled(True)
        else:
            self.widget.setDisabled(False)

    def printf_msg(self, msg):
        self.label2.setText(msg)


