import pygame
from AI2 import AI

class Civil(AI):

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str):
        super().__init__(tag, type, imagePath1, imagePath2)

        self.AddState("wander", self.OnEnterWander, self.OnExitWander, self.UpdateWander)
        self.AddState("objectif", self.OnEnterObjectif, self.OnExitObjectif, self.UpdateObjectif)
        self.AddState("alert", self.OnEnterAlert, self.OnExitAlert, self.UpdateAlert)
        self.AddState("flee", self.OnEnterFlee, self.OnExitFlee, self.UpdateFlee)
        self.AddState("dead", self.OnEnterDead, self.OnExitDead, self.UpdateDead)

        self.InitMachine("wander")

        allState = ["wander", "objectif", "alert", "flee", "dead"]

        for state in allState:
            self.AddTransition(state, "wander", state, None)
            self.AddTransition(state, "objectif", state, None)
            self.AddTransition(state, "alert", state, None)
            self.AddTransition(state, "flee", state, None)
            self.AddTransition(state, "dead", state, None)

        self.PlayTransition("wander")

        self.SetPos([500, 700])

# -------------------------------------------------------------------------------------------------
    def OnEnterWander(self):
        self.SetCurrentState("wander")
        self.currImg = self.defaultImg1

    def OnExitWander(self):
        pass

    def UpdateWander(self):
        self.Move(1)
        self.CheckHitBorder()
        self.CheckColliderMap()
        if self.CheckColliderWithBalls() == "player":
            self.PlayTransition("dead")

# -------------------------------------------------------------------------------------------------
    def OnEnterObjectif(self):
        self.SetCurrentState("objectif")

    def OnExitObjectif(self):
        pass

    def UpdateObjectif(self):
        pass

# ------------------------------------------------------------------------------------------------
    def OnEnterAlert(self):
        self.SetCurrentState("alert")

    def OnExitAlert(self):
        pass

    def UpdateAlert(self):
        pass

# -----------------------------------------------------------------------------------------------
    def OnEnterFlee(self):
        self.SetCurrentState("flee")

    def OnExitFlee(self):
        pass

    def UpdateFlee(self):
        pass

# ----------------------------------------------------------------------------------------------
    def OnEnterDead(self):
        self.SetCurrentState("dead")
        self.ChangeImgColor(self.defaultImg1, [50, 50, 50])

    def OnExitDead(self):
        pass

    def UpdateDead(self):
        pass