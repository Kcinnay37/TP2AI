import pygame
from AI2 import AI

class Civil(AI):

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str):
        super().__init__(tag, type, imagePath1, imagePath2)

        self.AddState("defend", self.OnEnterDefend, self.OnExitDefend, self.UpdateDefend)
        self.AddState("wander", self.OnEnterWander, self.OnExitWander, self.UpdateWander)
        self.AddState("alert", self.OnEnterAlert, self.OnExitAlert, self.UpdateAlert)
        self.AddState("flee", self.OnEnterFlee, self.OnExitFlee, self.UpdateFlee)
        self.AddState("attack", self.OnEnterAttack, self.OnExitAttack, self.UpdateAttack)
        self.AddState("warn", self.OnEnterWarn, self.OnExitWarn, self.UpdateWarn)

        self.InitMachine("wander")

        allState = ["defend", "wander", "alert", "flee", "attack", "warn"]

        for state in allState:
            self.AddTransition(state, "defend", state, None)
            self.AddTransition(state, "wander", state, None)
            self.AddTransition(state, "alert", state, None)
            self.AddTransition(state, "flee", state, None)
            self.AddTransition(state, "attack", state, None)
            self.AddTransition(state, "warn", state, None)

        self.PlayTransition("wander")

# -------------------------------------------------------------------------------------------------

    def OnEnterDefend(self):
        self.SetCurrentState("defend")

    def OnExitDefend(self):
        pass

    def UpdateDefend(self):
        pass
# -------------------------------------------------------------------------------------------------
    def OnEnterWander(self):
        self.SetCurrentState("wander")

    def OnExitWander(self):
        pass

    def UpdateWander(self):
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

# -----------------------------------------------------------------------------------------------
    def OnEnterAttack(self):
        self.SetCurrentState("attack")

    def OnExitAttack(self):
        pass

    def UpdateAttack(self):
        pass

# ----------------------------------------------------------------------------------------------
    def OnEnterWarn(self):
        self.SetCurrentState("warn")

    def OnExitWarn(self):
        pass

    def UpdateWarn(self):
        pass