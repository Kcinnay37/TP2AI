import pygame
from Agent import Agent
from Ball import Ball
from EventManager import EventManager

class Player(Agent):
    canChangeArm:bool
    canShoot:bool

    ballShoot:int = 0

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str):
        super().__init__(tag, type, imagePath1, imagePath2)

        self.AddState("dropArm", self.OnEnterDropArm, self.OnExitDropArm, self.UpdateDropArm)
        self.AddState("takeArm", self.OnEnterTakeArm, self.OnExitTakeArm, self.UpdateTakeArm)

        self.InitMachine("dropArm")

        self.AddTransition("changeArm", "dropArm", "takeArm", None)
        self.AddTransition("changeArm", "takeArm", "dropArm", None)

        self.canChangeArm = True
        self.canShoot = True

# TakeArm --------------------------------------------------------------------------
    def OnEnterTakeArm(self):
        self.SetCurrentState("takeArm")
        self.currImg = self.defaultImg2

    def OnExitTakeArm(self):
        pass
    
    def UpdateTakeArm(self):
        self.UpdateDropArm()
        self.Shoot()

# DropArm --------------------------------------------------------------------------
    def OnEnterDropArm(self):
        self.SetCurrentState("dropArm")
        self.currImg = self.defaultImg1

    def OnExitDropArm(self):
        pass

    def UpdateDropArm(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.Rotate(1)
        if pygame.key.get_pressed()[pygame.K_d]:
            self.Rotate(-1)
        if pygame.key.get_pressed()[pygame.K_w]:
            self.Move(1)
        if pygame.key.get_pressed()[pygame.K_s]:
            self.Move(-1)

        self.CheckHitBorder()
        self.CheckColliderMap()
        self.CheckColliderAgent()

        if not self.canChangeArm and not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.canChangeArm = True

# ---------------------------------------------------------------------------------

    def ChangeArm(self):
        if self.canChangeArm:
            self.PlayTransition("changeArm")
            self.canChangeArm = False

    def Shoot(self):
        if pygame.mouse.get_pressed()[0] and self.canShoot:
            offsetGun = self.vectRight.rotate(-self.angle + 26) * 32

            ball:Ball = Ball("ball" + str(self.ballShoot), "player", "Image\\Ball.png", self.pos + offsetGun, self.forward, self.angle)
            self.ballShoot += 1
            
            EventManager.TriggerEnter("addActor", {"actor": ball})

            self.canShoot = False
        elif not self.canShoot and not pygame.mouse.get_pressed()[0]:
            self.canShoot = True