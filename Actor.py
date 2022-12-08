from abc import abstractmethod

#plus haut parent des object dans le jeux
class Actor:
    tag:str
    type:str

    def __init__(self, tag:str, type:str):
        self.tag = tag
        self.type = type

    @abstractmethod
    def Render(self, screen):
        pass

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def FixedUpdate(self):
        pass

    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def Delete(self):
        pass

    @abstractmethod
    def OnColliderEnter(self , dir):
        pass

    def GetTag(self):
        return self.tag
