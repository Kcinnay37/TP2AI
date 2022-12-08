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
    maxRotateSpeed:float
    minRotateSpeed:float
    currRotateSpeed:float

    life:int

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str, pos, life:int):
        super().__init__(tag, type)

        EventManager.StartListening("getCollidersAgents", self.GetColliderAgent)

        self.size = pygame.math.Vector2(64, 64)
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.oldPos = self.pos
        self.midPos = self.pos + (self.size / 2)
        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)

        self.defaultImg1 = pygame.image.load(imagePath1)
        self.defaultImg1 = pygame.transform.scale(self.defaultImg1, self.size)
        self.defaultImg2 = pygame.image.load(imagePath2)
        self.defaultImg2 = pygame.transform.scale(self.defaultImg2, self.size)
        self.currImg = self.defaultImg1

        self.angle = 0
        self.maxSpeed = 200
        self.minSpeed = 0
        self.currSpeed = 0
        self.maxRotateSpeed = 200
        self.minRotateSpeed = 0
        self.currRotateSpeed = 200

        self.life = life

    # retourne les information relié au collider de l'agent
    def GetColliderAgent(self, param):
        return [self.pos.x - (self.size.x / 2), self.pos.y - (self.size.y / 2), self.size.x, self.size.y, self]

    # set la position et set la midPosition
    def SetPos(self, pos):
        self.pos.x = pos[0]
        self.pos.y = pos[1]
        self.midPos = self.pos + (self.size / 2)

    # rotate dans une direction a sa speed pre etablie
    def Rotate(self, dir:int):
        dt = EventManager.TriggerEvent("getDT", None)
        self.angle += dir * self.currRotateSpeed * dt
        self.forward = self.vectRight.rotate(-self.angle)

        return dir * self.currRotateSpeed * dt

    # avance devant ou derriere lui a une speed pre definie
    def Move(self, dir:int):
        dt = EventManager.TriggerEvent("getDT", None)
        
        self.oldPos = self.pos

        self.pos += self.forward * dir * self.currSpeed * dt
        self.midPos = self.pos + (self.size / 2)

    # regarde si l'agent sort de l'ecran si oui apport une correction
    def CheckHitBorder(self):
        screenSize = EventManager.TriggerEvent("getScreenSize", None)

        dir = EventManager.TriggerEvent("checkOutOfMap", {"pos": self.pos - (self.size / 2), "size": self.size})
        if dir[0] == -1:
            self.pos.x = self.size.x / 2
        if dir[0] == 1:
            self.pos.x = screenSize[0] - (self.size.x / 2)
        if dir[1] == -1:
            self.pos.y = self.size.y / 2
        if dir[1] == 1:
            self.pos.y = screenSize[1] - (self.size.y / 2)

        self.midPos = self.pos + (self.size / 2)

        if dir[0] != 0 or dir[1] != 0:
            self.OnColliderEnter(dir)

    # Check les collision avec un layer sur la tile si oui apport une correction
    def CheckColliderLayer(self, layer:str):
        dir = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - (self.size / 2), "size": self.size, "layer": layer})

        if dir[0] != 0:
            if (dir[0] > 0 and self.forward.x > 0) or (dir[0] < 0 and self.forward.x < 0):
                self.pos.x -= self.forward.x * self.currSpeed * EventManager.TriggerEvent("getDT", None)
            else:
                self.pos.x += self.forward.x * self.currSpeed * EventManager.TriggerEvent("getDT", None)
        if dir[1] != 0:
            if (dir[1] > 0 and self.forward.y > 0) or (dir[1] < 0 and self.forward.y < 0):
                self.pos.y -= self.forward.y * self.currSpeed * EventManager.TriggerEvent("getDT", None)
            else:
                self.pos.y += self.forward.y * self.currSpeed * EventManager.TriggerEvent("getDT", None)
        
        self.midPos = self.pos + (self.size / 2)

        if dir[0] != 0 or dir[1] != 0:
            self.OnColliderEnter(dir)

    # check les collision avec les autres agent dans la game si oui apport une correction
    def CheckColliderAgent(self):
        dir = EventManager.TriggerEvent("checkColliderWithAgents", {"pos": self.pos - (self.size / 2), "size": self.size})

        if dir[0] != 0:
            if (dir[0] > 0 and self.forward.x > 0) or (dir[0] < 0 and self.forward.x < 0):
                self.pos.x -= self.forward.x * self.currSpeed * EventManager.TriggerEvent("getDT", None)
            else:
                self.pos.x += self.forward.x * self.currSpeed * EventManager.TriggerEvent("getDT", None)
        if dir[1] != 0:
            if (dir[1] > 0 and self.forward.y > 0) or (dir[1] < 0 and self.forward.y < 0):
                self.pos.y -= self.forward.y * self.currSpeed * EventManager.TriggerEvent("getDT", None)
            else:
                self.pos.y += self.forward.y * self.currSpeed * EventManager.TriggerEvent("getDT", None)
        
        self.midPos = self.pos + (self.size / 2)
        
        if dir[0] != 0 or dir[1] != 0:
            self.OnColliderEnter(dir)

    # check les collisions avec les ball
    def CheckColliderWithBalls(self):
        dir = EventManager.TriggerEvent("checkColliderWithBalls", {"pos": self.pos - (self.size / 2), "size": self.size})
        
        if dir[0] != 0 or dir[1] != 0:
            self.OnColliderEnter(dir)

    # change la couleur de l'image et l'assigne a sa curr image
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

    # lorsqu'il est delete il mais fin a ses evenement
    def Delete(self):
        EventManager.StopListening("getCollidersAgents", self.GetColliderAgent)

    # affiche a l'ecran l'agent
    def Render(self, screen):
        img = pygame.transform.rotate(self.currImg, self.angle)
        screen.blit(img, self.pos - pygame.math.Vector2(int(img.get_width() / 2), int(img.get_height() / 2)))