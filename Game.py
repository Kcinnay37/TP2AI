import pygame
from Engine import Engine
from Civil import Civil
from Garde import Garde
from Timer import Timer
from Player import Player
from Map import Map
from EventManager import EventManager
from ColliderManager import ColliderManager
from PathFinding import PathFinding

class Game:
    isRun:bool

    width:int = 1920
    height:int = 1080
    size:float = []

    screen:pygame.display.set_mode

    BGColor:int = [2, 0, 102]

    engine:Engine

    timer:Timer
    player:Player

    map:Map

    colliderManager:ColliderManager

    pathFinding:PathFinding

    def __init__(self):
        EventManager.StartListening("getScreenSize", self.GetScreenSize)

        self.isRun = True

        self.colliderManager = ColliderManager()
        self.engine = Engine()
        self.timer = Timer()

        pygame.init()

        self.GameInit()

    def GetScreenSize(self, param):
        return [self.width, self.height]

    def GameInit(self):
        self.size = [self.width, self.height]
        self.screen = pygame.display.set_mode(self.size)

        # init tout les acteur de la map et les mets dans l'engine -----------------------------------------------------------------
        self.map = Map("map", "map", "Image\\MapTP2.tmx")
        EventManager.TriggerEvent("addActor", {"actor": self.map})

        self.pathFinding = PathFinding()

        self.player = Player("player", "player", "Image\\Player.png", "Image\\PlayerArm.png", [(64 * 7) + 32, (64 * 7) + 32], 3)
        EventManager.TriggerEvent("addActor", {"actor": self.player})

        self.civil1 = Civil("civil1", "civil", "Image\\Civil1_1.png", "Image\\Civil1_2.png", [2 * 64 + 32, 3 * 64 + 32], 1)
        EventManager.TriggerEvent("addActor", {"actor": self.civil1})

        self.civil2 = Civil("civil2", "civil", "Image\\Civil2_1.png", "Image\\Civil2_2.png", [2 * 64 + 32, 13 * 64 + 32], 1)
        EventManager.TriggerEvent("addActor", {"actor": self.civil2})

        self.civil3 = Civil("civil3", "civil", "Image\\Civil3_1.png", "Image\\Civil3_2.png", [25 * 64 + 32, 2 * 64 + 32], 1)
        EventManager.TriggerEvent("addActor", {"actor": self.civil3})

        self.garde1 = Garde("garde1", "garde", "Image\\Garde1.png", "Image\\Garde2.png", [15 * 64 + 32, 9 * 64 + 32], 4)
        EventManager.TriggerEvent("addActor", {"actor": self.garde1})

        self.garde2 = Garde("garde2", "garde", "Image\\Garde1.png", "Image\\Garde2.png", [20 * 64 + 32, 9 * 64 + 32], 4)
        EventManager.TriggerEvent("addActor", {"actor": self.garde2})

        # ----------------------------------------------------------------------------------------------------------------------

        self.engine.Start()

    def GameLoop(self):
        self.timer.Update()

        self.ProcessInput()

        self.engine.FixedUpdate()
        self.engine.Update()

        self.Render()

        return self.isRun

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    dir = EventManager.TriggerEvent("checkColliderWithAgents", {"pos": pygame.mouse.get_pos(), "size": [1, 1]})
                    if dir[2] != None and dir[2].type != "player":
                        oldAgent = EventManager.TriggerEvent("getAgentConnect", None)
                        if oldAgent != None:
                            oldAgent.DisconnectToInterface()
                        
                        dir[2].ConnectToInterface()

                        EventManager.TriggerEvent("initCombotBox", {"agent": dir[2]})
                if pygame.mouse.get_pressed()[2]:
                    pass

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.player.ChangeArm()



    def Render(self):
        self.screen.fill(self.BGColor)

        self.engine.Render(self.screen)

        pygame.display.flip()

    def ChangeMode(self, mode:str):
        self.AI.SetState(mode)
