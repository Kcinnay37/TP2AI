from Game import Game
from PySide2.QtWidgets import QWidget, QPushButton, QSlider, QComboBox,QHBoxLayout, QLabel
from PySide2.QtCore import QTimer
from EventManager import EventManager

class Window(QWidget):
    game:Game
    timer:QTimer

    FPS:int

    def __init__(self, game:Game, FPS:int=60):
        super().__init__()

        EventManager.StartListening("initCombotBox", self.InitCombotBox)

        self.FPS = 1000 / FPS
        self.game = game
        self.InitUI()
        self.InitPygame(game)

    def InitUI(self):
        self.setWindowTitle("Labo5")
        self.setGeometry(10, 10, 300, 200)

        # text pour la vie
        self.life = QLabel()
        self.life.setText("Life: ")

        self.layout = QHBoxLayout()

        # combotBox des state
        self.combotBox = QComboBox()

        self.combotBox.currentIndexChanged.connect(self.ChangeStateAgent)

        self.layout.addWidget(self.combotBox)
        self.layout.addWidget(self.life)
        self.setLayout(self.layout)

        self.show()

    # met le combotBox avec les state de l'agent et le text a la bonne vie
    def InitCombotBox(self, param):
        self.combotBox.clear()
        self.combotBox.currentIndexChanged.disconnect(self.ChangeStateAgent)

        match(param["agent"].type):
            case "civil":
                self.combotBox.addItem("wander")
                self.combotBox.addItem("objectif")
                self.combotBox.addItem("flee")
                self.combotBox.addItem("dead")
            case "garde":
                self.combotBox.addItem("defend")
                self.combotBox.addItem("wander")
                self.combotBox.addItem("search")
                self.combotBox.addItem("flee")
                self.combotBox.addItem("attack")
                self.combotBox.addItem("warn")
                self.combotBox.addItem("dead")
                self.combotBox.addItem("alarm")

        self.combotBox.setCurrentText(param["agent"].currentState)
        self.combotBox.currentIndexChanged.connect(self.ChangeStateAgent)

        self.life.setText("Life: " + str(param["agent"].life))

    # initialise pygame et le timer pour les frame
    def InitPygame(self, game:Game):
        self.game = game

        self.timer = QTimer()
        self.timer.timeout.connect(self.IsRun)
        self.timer.start(self.FPS)

    # change l'etat de lagent avec l'interface
    def ChangeStateAgent(self):
        agent = EventManager.TriggerEvent("getAgentConnect", None)
        combotBox = self.sender()
        state = combotBox.itemText(combotBox.currentIndex())

        if state != "":
            agent.changeManually = True
            agent.PlayTransition(state)

    # tant que la game run
    def IsRun(self):
        if not self.game.GameLoop():
            self.close()

    def ChangeMode(self):
        pass
        #combotBox = self.sender()
        #self.game.ChangeMode(combotBox.itemText(combotBox.currentIndex()))
