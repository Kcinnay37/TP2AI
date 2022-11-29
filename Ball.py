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

    def __init__(self, tag:str, type:str, pathImage:str, initialPos:pygame.math.Vector2, forward:pygame.math.Vector2, angle:float):
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

    def GetColliderBall(self, param):
        return [self.pos.x - (self.size.x / 2), self.pos.y - (self.size.y / 2), self.size.x, self.size.y, self.type]

    def Move(self):
        dt = EventManager.TriggerEnter("getDT", None)
        self.pos += self.forward * 1000 * dt
        self.midPos = self.pos + (self.size / 2)

    def CheckDestroy(self):
        dir1 = EventManager.TriggerEnter("checkOutOfMap", {"pos": self.pos - self.size / 2, "size": self.size})
        dir2 = EventManager.TriggerEnter("checkColliderWithMap", {"pos": self.pos - self.size / 2, "size": self.size})
        dir3 = EventManager.TriggerEnter("checkColliderWithAgents", {"pos": self.pos - self.size / 2, "size": self.size})

        if (dir1[0] != 0 or dir1[1] != 0) \
            or (dir2[0] != 0 or dir2[1] != 0) \
            or ((dir3[0] != 0 or dir3[1] != 0) and dir3[2] != self.type):
            EventManager.TriggerEnter("deleteActor", {"tag": self.tag})

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