from Actor import Actor
from EventManager import EventManager

class Engine:
    actors:Actor = []
    toDelete:int = []

    def __init__(self):
        EventManager.StartListening("addActor", self.AddActor)
        EventManager.StartListening("deleteActor", self.DeleteActor)

        self.actors = []
        self.toDelete = []

    # fait le start de tout les acteur
    def Start(self):
        for i in range(len(self.actors)):
            self.actors[i].Start()

    # fait le fixedUpdate de tout les acteur et delete les actor qui doivent l'etre
    def FixedUpdate(self):
        self.toDelete.sort()
        for i in range(len(self.toDelete)):
            self.actors[self.toDelete[i] - i].Delete()
            self.actors.pop(self.toDelete[i] - i)
        self.toDelete.clear()

        for i in range(len(self.actors)):
            self.actors[i].FixedUpdate()

    # appel le update de tout les acteur
    def Update(self):
        for i in range(len(self.actors)):
            self.actors[i].Update()

    # appel le render de tout les acteur
    def Render(self, screen):
        for i in range(len(self.actors)):
            self.actors[i].Render(screen)
    
    # ajoute un acteur dans l'engine
    def AddActor(self, param):
        self.actors.append(param["actor"])

    # delete un acteur de l,engine
    def DeleteActor(self, param):
        for i in self.toDelete:
            if self.actors[i].tag == param["tag"]:
                return

        for i in range(len(self.actors)):
            if self.actors[i].tag == param["tag"]:
                self.toDelete.append(i) 
                break
