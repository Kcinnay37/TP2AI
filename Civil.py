import pygame
from AI2 import AI
from EventManager import EventManager
import random

class Civil(AI):

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str, pos, life):
        super().__init__(tag, type, imagePath1, imagePath2, pos, life)

        EventManager.StartListening("alarmSounded", self.AlarmSounded)

        # ajout de state
        self.AddState("wander", self.OnEnterWander, self.OnExitWander, self.UpdateWander, self.OnColliderWander)
        self.AddState("objectif", self.OnEnterObjectif, self.OnExitObjectif, self.UpdateObjectif, self.OnColliderObjectif)
        self.AddState("alert", self.OnEnterAlert, self.OnExitAlert, self.UpdateAlert, self.OnColliderAlert)
        self.AddState("flee", self.OnEnterFlee, self.OnExitFlee, self.UpdateFlee, self.OnColliderFlee)
        self.AddState("dead", self.OnEnterDead, self.OnExitDead, self.UpdateDead, self.OnColliderDead)

        self.InitMachine("wander")

        # connect tout les state entre eu
        allState = ["wander", "objectif", "alert", "flee", "dead"]

        for state in allState:
            self.AddTransition(state, "wander", state, None)
            self.AddTransition(state, "objectif", state, None)
            self.AddTransition(state, "alert", state, None)
            self.AddTransition(state, "flee", state, None)
            self.AddTransition(state, "dead", state, None)

        self.PlayTransition("wander")

#  Wander state-------------------------------------------------------------------------------------------------
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
            self.PlayTransition("objectif")
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

# Objectif state -------------------------------------------------------------------------------------------------
    isArrive = False
    timeObjectif:float
    currTimeObjectif:float
    
    def OnEnterObjectif(self):
        self.SetCurrentState("objectif")
        self.currImg = self.defaultImg1
        self.isArrive = False 

        self.timeObjectif = random.randint(5, 10)
        self.currTimeObjectif = 0

        self.GoInActivity()

    def OnExitObjectif(self):
        self.currImg = self.defaultImg1

    def UpdateObjectif(self):
        self.CheckListenAround()
        self.LookForward()
        self.CheckLookForward()

        if self.currTimeObjectif >= self.timeObjectif and not self.changeManually:
            self.PlayTransition("wander")
        elif self.isArrive:
            self.currTimeObjectif += EventManager.TriggerEvent("getDT", None)

        if self.currSpeed == 0 and not self.isArrive:
            self.GoInActivity()

        self.Move(1)

        self.CheckColliderWithBalls()
        self.CheckColliderAgent()

        if self.CheckIsArrived() and self.CheckInActivity():
            self.currSpeed = 0
            self.isArrive = True
            self.currImg = self.defaultImg2
            self.SetDestination([self.pos.x, self.pos.y - 1])

    def OnColliderObjectif(self, dir):
        if dir[2].type == "playerBall":
            self.TakeHit()
        elif dir[2].type == "player" or dir[2].type == "civil" or dir[2].type == "garde":
            self.DodgeObstacle(dir)

    def GoInActivity(self):
        gridActivity = EventManager.TriggerEvent("getLayerGrid", {"layer": "Activity"})
        index = random.randint(0, len(gridActivity) - 1)
        activityToGo = gridActivity[index]
        self.SetBestPathAt([activityToGo[0], activityToGo[1]])
        self.InitMove()

    def CheckInActivity(self):
        dir = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - (self.size / 2), "size": self.size, "layer": "Activity"})
        if dir[2] != None:
            return True
        else:
            return False

# Alert State non implementé ------------------------------------------------------------------------------------------------
    def OnEnterAlert(self):
        self.SetCurrentState("alert")
        self.currImg = self.defaultImg1

    def OnExitAlert(self):
        pass

    def UpdateAlert(self):
        pass

    def OnColliderAlert(self, dir):
        pass

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

    def GoInSafeZone(self):
        gridSafeZone = EventManager.TriggerEvent("getLayerGrid", {"layer": "SafeZone"})
        index = random.randint(0, len(gridSafeZone) - 1)
        posToGo = gridSafeZone[index]
        self.SetBestPathAt([posToGo[0], posToGo[1]])
        self.InitMove()

    def CheckInSafeZone(self):
        dir = EventManager.TriggerEvent("checkColliderLayer", {"pos": self.pos - (self.size / 2), "size": self.size, "layer": "SafeZone"})
        if dir[2] != None:
            return True
        else:
            return False
# Dead state ----------------------------------------------------------------------------------------------
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

    def TakeHit(self):
        self.life -= 1
        if self.life <= 0:
            if not self.changeManually:
                self.PlayTransition("dead")


# ---------------------------------------------------------------------------------------------

    # regarde si il a entendu quelque chose
    def CheckListenAround(self):
        if self.listenAround:
            self.listenAround = False
            if not self.changeManually:
                self.PlayTransition("flee")

    # regarde si il voit devant lui
    def CheckLookForward(self):
        if self.lookForward:
            self.lookForward = False
            if not self.changeManually:
                self.PlayTransition("flee")

    # regarde si l'alarm a été sonné
    def AlarmSounded(self, param):
        if self.currentState != "dead":
            if not self.changeManually:
                self.PlayTransition("flee")