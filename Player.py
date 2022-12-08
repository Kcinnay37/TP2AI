import pygame
from Agent import Agent
from Ball import Ball
from EventManager import EventManager

class Player(Agent):
    canChangeArm:bool
    canShoot:bool

    ballShoot:int = 0

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str, pos, life):
        super().__init__(tag, type, imagePath1, imagePath2, pos, life)

        EventManager.StartListening("getPlayerPos", self.GetPos)
        EventManager.StartListening("getPlayerIsArm", self.GetPlayerIsArm)
        EventManager.StartListening("getPlayerIsDead", self.GetPlayerIsDead)

        # AJoute tout les state
        self.AddState("dropArm", self.OnEnterDropArm, self.OnExitDropArm, self.UpdateDropArm, self.OnColliderDropArm)
        self.AddState("takeArm", self.OnEnterTakeArm, self.OnExitTakeArm, self.UpdateTakeArm, self.OnColliderTakeArm)
        self.AddState("dead", self.OnEnterDead, self.OnExitDead, self.UpdateDead, self.OnColliderDead)

        self.InitMachine("dropArm")

        # mets toute les transition
        self.AddTransition("changeArm", "dropArm", "takeArm", None)
        self.AddTransition("changeArm", "takeArm", "dropArm", None)
        self.AddTransition("dead", "dropArm", "dead", None)
        self.AddTransition("dead", "takeArm", "dead", None)

        self.canChangeArm = True
        self.canShoot = True

        self.currSpeed = 200

# TakeArm state --------------------------------------------------------------------------
    def OnEnterTakeArm(self):
        self.SetCurrentState("takeArm")
        self.currImg = self.defaultImg2

        EventManager.StartListening("getColliderDanger", self.GetColliderAgent)

    def OnExitTakeArm(self):
        pass
    
    def UpdateTakeArm(self):
        self.UpdateDropArm()
        self.Shoot()

    def OnColliderTakeArm(self, dir):
        if dir[2].type == "aiBall":
            self.TakeHit()

# DropArm state --------------------------------------------------------------------------
    def OnEnterDropArm(self):
        self.SetCurrentState("dropArm")
        self.currImg = self.defaultImg1

        EventManager.StopListening("getColliderDanger", self.GetColliderAgent)

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

        self.CheckColliderWithBalls()
        self.CheckHitBorder()
        self.CheckColliderLayer("Obstacle")
        self.CheckColliderLayer("SafeZone")
        self.CheckColliderAgent()

        if not self.canChangeArm and not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.canChangeArm = True

    def OnColliderDropArm(self, dir):
        if dir[2].type == "aiBall":
            self.TakeHit()

# Dead state ---------------------------------------------------------------------------------
    def OnEnterDead(self):
        self.SetCurrentState("dead")
        self.ChangeImgColor(self.defaultImg1, [50, 50, 50])

    def OnExitDead(self):
        pass

    def UpdateDead(self):
        pass

    def OnColliderDead(self, dir):
        pass

    def TakeHit(self):
        self.life -= 1
        if self.life <= 0:
            self.PlayTransition("dead")
# --------------------------------------------------------------------------------

    # change de state
    def ChangeArm(self):
        if self.canChangeArm and self.currentState != "dead":
            self.PlayTransition("changeArm")
            self.canChangeArm = False

    # instantie une ball
    def Shoot(self):
        if pygame.mouse.get_pressed()[0] and self.canShoot:
            offsetGun = self.vectRight.rotate(-self.angle + 26) * 32

            ball:Ball = Ball("ball" + str(self.ballShoot), "playerBall", self.type, "Image\\Ball.png", self.pos + offsetGun, self.forward, self.angle)
            self.ballShoot += 1
            
            EventManager.TriggerEvent("addActor", {"actor": ball})

            self.canShoot = False

            EventManager.TriggerEvent("listenAroundAll", {"ball": ball})
        elif not self.canShoot and not pygame.mouse.get_pressed()[0]:
            self.canShoot = True


    def GetPos(self, param):
        return self.pos

    # regarde si le player est armé
    def GetPlayerIsArm(self, param):
        if self.currentState == "takeArm":
            return True
        else:
            return False

    # regarde si le player est dead
    def GetPlayerIsDead(self, param):
        if self.currentState == "dead":
            return True
        else:
            return False