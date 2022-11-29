import pygame
from StateMachine import StateMachine
from EventManager import EventManager
import copy

class Agent(StateMachine):
    defaultImg1:pygame.image.load
    defaultImg2:pygame.image.load
    currImg:pygame.image.load
    imgColor:pygame.image.load

    pos:pygame.math.Vector2
    oldPos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    vectRight:pygame.math.Vector2
    forward:pygame.math.Vector2
    
    angle:float
    maxSpeed:float
    minSpeed:float
    currSpeed:float
    rotateSpeed:float
    currRotateSpeed:float

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str):
        super().__init__(tag, type)

        EventManager.StartListening("getCollidersAgents", self.GetColliderAgent)

        self.pos = pygame.math.Vector2(500, 400)
        self.oldPos = self.pos
        self.size = pygame.math.Vector2(64, 64)
        self.midPos = self.pos + (self.size / 2)
        self.angle = 0

        self.defaultImg1 = pygame.image.load(imagePath1)
        self.defaultImg1 = pygame.transform.scale(self.defaultImg1, self.size)

        self.defaultImg2 = pygame.image.load(imagePath2)
        self.defaultImg2 = pygame.transform.scale(self.defaultImg2, self.size)

        self.currImg = self.defaultImg1

        self.moveSpeed = 200
        self.rotateSpeed = 150

        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)

    def GetColliderAgent(self, param):
        return [self.pos.x - (self.size.x / 2), self.pos.y - (self.size.y / 2), self.size.x, self.size.y, self.type]

    def SetPos(self, pos):
        self.pos.x = pos[0]
        self.pos.y = pos[1]

    def Rotate(self, dir:int):
        dt = EventManager.TriggerEnter("getDT", None)
        self.angle += dir * self.rotateSpeed * dt
        self.forward = self.vectRight.rotate(-self.angle)

    def Move(self, dir:int):
        dt = EventManager.TriggerEnter("getDT", None)
        
        self.oldPos = self.pos

        self.pos += self.forward * dir * self.moveSpeed * dt
        self.midPos = self.pos + (self.size / 2)

    def CheckHitBorder(self):
        screenSize = EventManager.TriggerEnter("getScreenSize", None)

        dir = EventManager.TriggerEnter("checkOutOfMap", {"pos": self.pos - (self.size / 2), "size": self.size})
        if dir[0] == -1:
            self.pos.x = 1 + self.size.x / 2
        if dir[0] == 1:
            self.pos.x = screenSize[0] - (1 + self.size.x / 2)
        if dir[1] == -1:
            self.pos.y = 1 + self.size.y / 2
        if dir[1] == 1:
            self.pos.y = screenSize[1] - (1 + self.size.y / 2)

        self.midPos = self.pos + (self.size / 2)

    def CheckColliderMap(self):
        dir = EventManager.TriggerEnter("checkColliderWithMap", {"pos": self.pos - (self.size / 2), "size": self.size})

        if dir[0] != 0:
            if (dir[0] > 0 and self.forward.x > 0) or (dir[0] < 0 and self.forward.x < 0):
                self.pos.x -= self.forward.x * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
            else:
                self.pos.x += self.forward.x * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
        if dir[1] != 0:
            if (dir[1] > 0 and self.forward.y > 0) or (dir[1] < 0 and self.forward.y < 0):
                self.pos.y -= self.forward.y * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
            else:
                self.pos.y += self.forward.y * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
        
        self.midPos = self.pos + (self.size / 2)

    def CheckColliderAgent(self):
        dir = EventManager.TriggerEnter("checkColliderWithAgents", {"pos": self.pos - (self.size / 2), "size": self.size})

        if dir[0] != 0:
            if (dir[0] > 0 and self.forward.x > 0) or (dir[0] < 0 and self.forward.x < 0):
                self.pos.x -= self.forward.x * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
            else:
                self.pos.x += self.forward.x * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
        if dir[1] != 0:
            if (dir[1] > 0 and self.forward.y > 0) or (dir[1] < 0 and self.forward.y < 0):
                self.pos.y -= self.forward.y * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
            else:
                self.pos.y += self.forward.y * self.moveSpeed * EventManager.TriggerEnter("getDT", None)
        
        self.midPos = self.pos + (self.size / 2)

    def CheckColliderWithBalls(self):
        dir = EventManager.TriggerEnter("checkColliderWithBalls", {"pos": self.pos - (self.size / 2), "size": self.size})
        return dir[2]

    def ChangeImgColor(self, image, rgb):
        self.imgColor = copy.copy(image)
        
        w, h = self.imgColor.get_size()
        for x in range(w):
            for y in range(h):
                a = self.imgColor.get_at((x, y))[3]
                if a != 0:
                    r = self.imgColor.get_at((x, y))[0]
                    r = rgb[0]
                    g = self.imgColor.get_at((x, y))[1]
                    g = rgb[1]
                    b = self.imgColor.get_at((x, y))[2]
                    b = rgb[2]
                    self.imgColor.set_at((x, y), pygame.Color(r, g, b, a))
        self.currImg = self.imgColor

    def Delete(self):
        EventManager.StopListening("getCollidersAgents", self.GetColliderAgent)

    def Render(self, screen):
        img = pygame.transform.rotate(self.currImg, self.angle)
        screen.blit(img, self.pos - pygame.math.Vector2(int(img.get_width() / 2), int(img.get_height() / 2)))