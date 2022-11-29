import pygame
from Engine import Engine
from Civil import Civil
from Timer import Timer
from Player import Player
from Map import Map
from EventManager import EventManager
from ColliderManager import ColliderManager

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

        self.map = Map("map", "map", "Image\\MapTP2.tmx")
        EventManager.TriggerEnter("addActor", {"actor": self.map})

        self.player = Player("player", "player", "Image\\Player.png", "Image\\PlayerArm.png")
        EventManager.TriggerEnter("addActor", {"actor": self.player})

        self.civil = Civil("civil", "ai", "Image\\Civil1_1.png", "Image\\Civil1_2.png")
        EventManager.TriggerEnter("addActor", {"actor": self.civil})

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
                    pass
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
