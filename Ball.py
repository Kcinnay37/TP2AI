import pygame
from Actor import Actor
import copy
from EventManager import EventManager

class Ball(Actor):
    defaultImg:pygame.image.load

    pos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    forward:pygame.math.Vector2
    angle:float

    currTime:int

    ignoreType:str

    def __init__(self, tag:str, type:str, ignoreType:str, pathImage:str, initialPos:pygame.math.Vector2, forward:pygame.math.Vector2, angle:float):
        super().__init__(tag, type)

        EventManager.StartListening("getCollidersBalls", self.GetColliderBall)

        self.pos = copy.copy(initialPos)
        self.forward = copy.copy(forward)
        self.size = pygame.math.Vector2(32, 32)
        self.midPos = self.pos + (self.size / 2)
        self.angle = copy.copy(angle)

        self.defaultImg = pygame.image.load(pathImage)
        self.defaultImg = pygame.transform.scale(self.defaultImg, self.size)

        self.currTime = 0

        self.type = type
        self.ignoreType = ignoreType

    # retourn les information relier a le collider de la ball
    def GetColliderBall(self, param):
        return [self.pos.x - (self.size.x / 2), self.pos.y - (self.size.y / 2), self.size.x, self.size.y, self]

    # bouge vert l'avant
    def Move(self):
        dt = EventManager.TriggerEvent("getDT", None)
        self.pos += self.forward * 1000 * dt
        self.midPos = self.pos + (self.size / 2)

    # regarde si la ball doit etre detruite
    def CheckDestroy(self):
        dir1 = EventManager.TriggerEvent("checkOutOfMap", {"pos": self.pos - self.size / 2, "size": self.size})
        dir2 = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - self.size / 2, "size": self.size, "layer": "Obstacle"})
        dir3 = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - self.size / 2, "size": self.size, "layer": "SafeZone"})
        dir4 = EventManager.TriggerEvent("checkColliderWithAgents", {"pos": self.pos - self.size / 2, "size": self.size})

        if dir1[2] != None or dir2[2] != None or dir3[2] != None or (dir4[2] != None and dir4[2].type != self.ignoreType):
            EventManager.TriggerEvent("deleteActor", {"tag": self.tag})

    def FixedUpdate(self):
        self.Move()
        self.CheckDestroy()

    def Update(self):
        pass

    def Delete(self):
        EventManager.StopListening("getCollidersBalls", self.GetColliderBall)
    
    def Render(self, screen):
        img = pygame.transform.rotate(self.defaultImg, self.angle)
        screen.blit(img, self.pos - pygame.math.Vector2(int(img.get_width() / 2), int(img.get_height() / 2)))