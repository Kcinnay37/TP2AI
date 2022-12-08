import pygame
from AI2 import AI
import random
from EventManager import EventManager
import math
from Ball import Ball

class Garde(AI):

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str, pos, life):
        super().__init__(tag, type, imagePath1, imagePath2, pos, life)
        
        EventManager.StartListening("alarmSounded", self.AlarmSounded)

        # ajoute tout les state
        self.AddState("defend", self.OnEnterDefend, self.OnExitDefend, self.UpdateDefend, self.OnColliderDefend)
        self.AddState("wander", self.OnEnterWander, self.OnExitWander, self.UpdateWander, self.OnColliderWander)
        self.AddState("search", self.OnEnterSearch, self.OnExitSearch, self.UpdateSearch, self.OnColliderSearch)
        self.AddState("flee", self.OnEnterFlee, self.OnExitFlee, self.UpdateFlee, self.OnColliderFlee)
        self.AddState("attack", self.OnEnterAttack, self.OnExitAttack, self.UpdateAttack, self.OnColliderAttack)
        self.AddState("warn", self.OnEnterWarn, self.OnExitWarn, self.UpdateWarn, self.OnColliderWarn)
        self.AddState("dead", self.OnEnterDead, self.OnExitDead, self.UpdateDead, self.OnColliderDead)
        self.AddState("alarm", self.OnEnterAlarm, self.OnExitAlarm, self.UpdateAlarm, self.OnColliderAlarm)

        self.InitMachine("wander")

        # relie tout les states entre elle
        allState = ["defend", "wander", "search", "flee", "attack", "warn", "dead", "alarm"]

        for state in allState:
            self.AddTransition(state, "defend", state, None)
            self.AddTransition(state, "wander", state, None)
            self.AddTransition(state, "search", state, None)
            self.AddTransition(state, "flee", state, None)
            self.AddTransition(state, "attack", state, None)
            self.AddTransition(state, "warn", state, None)
            self.AddTransition(state, "dead", state, None)
            self.AddTransition(state, "alarm", state, None)

        self.PlayTransition("wander")

# Defend state -------------------------------------------------------------------------------------------------
    isArrive = False
    timeDefend:float
    currTimeDefend:float

    def OnEnterDefend(self):
        self.SetCurrentState("defend")

        self.currImg = self.defaultImg1
        self.isArrive = False 

        self.timeDefend = random.randint(5, 10)
        self.currTimeDefend = 0

        self.GoDefend()

    def OnExitDefend(self):
        pass

    def UpdateDefend(self):
        self.CheckListenAround()
        self.LookForward()
        self.CheckLookForward()

        if self.currTimeDefend >= self.timeDefend and not self.changeManually:
            self.PlayTransition("wander")
        elif self.isArrive:
            self.currTimeDefend += EventManager.TriggerEvent("getDT", None)

        if self.currSpeed == 0 and not self.isArrive:
            self.GoDefend()

        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

        if self.CheckIsArrived() and self.CheckDefend():
            self.currSpeed = 0
            self.isArrive = True
            self.currImg = self.defaultImg2
            self.SetDestination([self.pos.x, self.pos.y - 1])
    
    def OnColliderDefend(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)

    # va a une zone de defend
    def GoDefend(self):
        gridDefend = EventManager.TriggerEvent("getLayerGrid", {"layer": "Defend"})
        index = random.randint(0, len(gridDefend) - 1)
        activityToGo = gridDefend[index]
        self.SetBestPathAt([activityToGo[0], activityToGo[1]])
        self.InitMove()

    # regarde si le joueur est dans la zone de defend
    def CheckDefend(self):
        dir = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - (self.size / 2), "size": self.size, "layer": "Defend"})
        if dir[2] != None:
            return True
        else:
            return False

# Wander state -------------------------------------------------------------------------------------------------
    timeWander:float
    currTimeWander:float

    def OnEnterWander(self):
        self.SetCurrentState("wander")
        self.currImg = self.defaultImg1

        self.timeWander = random.randint(10, 30)
        self.currTimeWander = 0

        self.SetRandomBestPathDest()
        self.InitMove()

    def OnExitWander(self):
        pass

    def UpdateWander(self):
        self.CheckListenAround()
        self.LookForward()
        self.CheckLookForward()

        if self.currTimeWander >= self.timeWander and not self.changeManually:
            self.PlayTransition("defend")
        else:
            self.currTimeWander += EventManager.TriggerEvent("getDT", None)
        
        if self.currSpeed == 0:
            self.SetRandomBestPathDest()
            self.InitMove()
        
        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()
        
        if self.CheckIsArrived():
            self.SetRandomBestPathDest() == False
            self.InitMove()
    
    def OnColliderWander(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)

# Search state ------------------------------------------------------------------------------------------------
    currRotation:float
    
    def OnEnterSearch(self):
        self.SetCurrentState("search")
        self.currImg = self.defaultImg1

        self.currRotation = 0

    def OnExitSearch(self):
        pass

    def UpdateSearch(self):
        self.CheckListenAround()
        self.LookForward()
        self.CheckLookForward()

        if not self.TurnAround() and not self.changeManually:
            self.PlayTransition("wander")

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

    def OnColliderSearch(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()

    # tourne sur lui meme
    def TurnAround(self):
        if self.currRotation < 360:
            self.currRotation += self.Rotate(1)
            return True
        return False

# Flee state -----------------------------------------------------------------------------------------------
    def OnEnterFlee(self):
        self.SetCurrentState("flee")
        self.currImg = self.defaultImg1
        self.isArrive = False 

        self.GoInSafeZone()

    def OnExitFlee(self):
        pass

    def UpdateFlee(self):
        if self.currSpeed == 0 and not self.isArrive:
            self.GoInSafeZone()

        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

        if self.CheckIsArrived() and self.CheckInSafeZone():
            self.currSpeed = 0
            self.isArrive = True

    def OnColliderFlee(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            if self.CheckInSafeZone():
                self.GoInSafeZone()
            else:
                self.DodgeObstacle(dir)

    # va dans une zone de securité
    def GoInSafeZone(self):
        gridSafeZone = EventManager.TriggerEvent("getLayerGrid", {"layer": "SafeZone"})
        index = random.randint(0, len(gridSafeZone) - 1)
        posToGo = gridSafeZone[index]
        self.SetBestPathAt([posToGo[0], posToGo[1]])
        self.InitMove()

    # regarde si il est dans la zone de securité
    def CheckInSafeZone(self):
        dir = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - (self.size / 2), "size": self.size, "layer": "SafeZone"})
        if dir[2] != None:
            return True
        else:
            return False

# Attack state -----------------------------------------------------------------------------------------------

    ballShoot:int = 0
    canShoot:bool
    timeShoot:float
    currTimeShoot:float

    def OnEnterAttack(self):
        self.SetCurrentState("attack")
        self.currImg = self.defaultImg2

        self.timeShoot = 0.5
        self.currTimeShoot = 0
        self.canShoot = True

        self.GoOnPlayer()

    def OnExitAttack(self):
        pass

    def UpdateAttack(self):
        if EventManager.TriggerEvent("getPlayerIsDead", None) and not self.changeManually:
            self.PlayTransition("wander")

        if not self.canShoot:
            self.currTimeShoot += EventManager.TriggerEvent("getDT", None)
            if self.currTimeShoot >= self.timeShoot:
                self.canShoot = True
                self.currTimeShoot = 0
        
        self.CheckIsArrived()
        if self.CheckDistanceToPlayer(256):
            self.currSpeed = 0
            self.RotateToPlayer()
            self.Shoot()
        elif self.currSpeed == 0:
            self.GoOnPlayer()
        
        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

    def OnColliderAttack(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)

    # instanci une ball
    def Shoot(self):
        if self.canShoot:
            offsetGun = self.vectRight.rotate(-self.angle + 26) * 32

            ball:Ball = Ball("ball" + str(self.ballShoot), "aiBall", self.type, "Image\\Ball.png", self.pos + offsetGun, self.forward, self.angle)
            self.ballShoot += 1
            
            EventManager.TriggerEvent("addActor", {"actor": ball})

            self.canShoot = False

# Warn state ----------------------------------------------------------------------------------------------
    timeWarn:float
    currTimeWarn:float

    timeSwapImage:float
    currTimeSwap:float
    red:bool
    
    def OnEnterWarn(self):
        self.SetCurrentState("warn")
        self.currImg = self.defaultImg2

        self.timeWarn = 3
        self.currTimeWarn = 0

        self.timeSwapImage = 0.5
        self.currTimeSwap = 0
        self.red = False

        self.GoOnPlayer()

    def OnExitWarn(self):
        pass

    def UpdateWarn(self):
        if not EventManager.TriggerEvent("getPlayerIsArm", None) and not self.changeManually:
            self.PlayTransition("wander")

        dt = EventManager.TriggerEvent("getDT", None)

        self.currTimeWarn += dt
        self.currTimeSwap += dt

        if self.currTimeWarn >= self.timeWarn and not self.changeManually:
            self.PlayTransition("attack")
        elif self.currTimeSwap >= self.timeSwapImage:
            self.currTimeSwap = 0
            if self.red:
                self.currImg = self.defaultImg2
            else:
                self.ChangeImgColor(self.defaultImg2, [255, 0, 0])

            self.red = not self.red

        self.CheckIsArrived()
        if self.CheckDistanceToPlayer(128):
            self.currSpeed = 0
            self.RotateToPlayer()
        elif self.currSpeed == 0:
            self.GoOnPlayer()
        
        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

    def OnColliderWarn(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)

    # va sur le joueur
    def GoOnPlayer(self):
        playerPos = EventManager.TriggerEvent("getPlayerPos", None)
        self.SetBestPathAt([math.floor(playerPos[0] / 64), math.floor(playerPos[1] / 64)])
        self.InitMove()

    # regarde si il est dans la distance rentré du player
    def CheckDistanceToPlayer(self, dist):
        playerPos = EventManager.TriggerEvent("getPlayerPos", None)
        vect = playerPos - self.pos

        a = math.floor(vect[0] * vect[0])
        b = math.floor(vect[1] * vect[1])
        c = a + b
        c = math.sqrt(c)

        if c <= dist:
            return True

    # rotate dans la direction du joueur
    def RotateToPlayer(self):
        playerPos = EventManager.TriggerEvent("getPlayerPos", None)
        self.SetDestination(playerPos)

# Alarm state --------------------------------------------------------------------------------------------

    def OnEnterAlarm(self):
        self.SetCurrentState("alarm")
        self.currImg = self.defaultImg1
        self.isArrive = False 

        self.GoAlarm()

    def OnExitAlarm(self):
        pass

    def UpdateAlarm(self):
        self.CheckIsArrived()

        if self.currSpeed == 0:
            self.GoAlarm()

        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()
        self.CheckColliderLayer("Alarm")

    def OnColliderAlarm(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)
        elif dir[2].type == "Alarm":
            EventManager.TriggerEvent("alarmSounded", None)

    # va sur l'alarm      
    def GoAlarm(self):
        gridAlarm = EventManager.TriggerEvent("getLayerGrid", {"layer": "Alarm"})
        pos = gridAlarm[0]
        self.SetBestPathAt([pos[0], pos[1]])
        self.InitMove()
# Dead state --------------------------------------------------------------------------------------------

    def OnEnterDead(self):
        self.SetCurrentState("dead")
        self.ChangeImgColor(self.defaultImg1, [50, 50, 50])
        EventManager.StartListening("getColliderDanger", self.GetColliderAgent)

    def OnExitDead(self):
        pass

    def UpdateDead(self):
        pass

    def OnColliderDead(self, dir):
        pass

    # enleve un point de vie et agit en consequence
    def TakeHit(self):
        self.life -= 1
        if self.life == 1:
            if not self.changeManually:
                self.PlayTransition("flee")
        elif self.life <= 0:
            if not self.changeManually:
                self.PlayTransition("dead")
        else:
            if not self.changeManually:
                self.PlayTransition("attack")

# -------------------------------------------------------------------------------------

    # ecoute si il a entendu quelque chose
    def CheckListenAround(self):
        if self.listenAround:
            self.listenAround = False
            if not self.changeManually:
                self.PlayTransition("search")

    # regarde si il a vue quelque chose
    def CheckLookForward(self):
        if self.lookForward:
            self.lookForward = False
            if self.dangerForward.type == "player":
                if not self.changeManually:
                    self.PlayTransition("warn")
            else:
                if not self.changeManually:
                    self.PlayTransition("alarm")

    # l'alarm a ete sonné
    def AlarmSounded(self, param):
        if self.life > 1:
            if not self.changeManually:
                self.PlayTransition("attack")