import pygame
from Agent import Agent
from EventManager import EventManager
import copy
import random
import math

# class parent des AI
class AI(Agent):
    destination:pygame.math.Vector2
    destinations = []

    finalDest = []

    listenAround:bool
    lookForward:bool
    dangerForward:Agent

    changeManually:bool

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str, pos, life):
        super().__init__(tag, type, imagePath1, imagePath2, pos, life)

        EventManager.StartListening("listenAroundAll", self.ListenAround)

        self.destination = copy.copy(self.pos)
        self.destinations = []
        self.finalDest = None
        self.listenAround = False
        self.lookForward = False
        self.dangerForward = None
        self.changeManually = False

    # permet au AI de commencer sont chemin
    def InitMove(self):
        if len(self.destinations) > 0:
            self.currSpeed = self.maxSpeed
            dest = self.destinations.pop(0)
            self.SetDestination(dest)

    # regarde si il est arrivé a destination et agit en concequence
    def CheckIsArrived(self):
        dt = EventManager.TriggerEvent("getDT", None)
        offset = (self.pos - self.destination).magnitude()
        if offset <= self.currSpeed * dt:
            if len(self.destinations) > 0:
                dest = self.destinations.pop(0)
                self.SetDestination(dest)
                return False
            elif self.finalDest != None:
                self.SetBestPathAt((self.finalDest / 64) - 32)
                self.finalDest = None
                dest = self.destinations.pop(0)
                self.SetDestination(dest)
                return False
            else:
                self.currSpeed = 0
                return True
        return False

    # set la destination et ajuste la rotation du joueur selon elle
    def SetDestination(self, dest):
        self.destination.x = dest[0]
        self.destination.y = dest[1]
        self.UpdateForward()

    # ajoute une destination dans le tableau de tout les destination qu'il doit aller
    def AddDestination(self, dest):
        self.destinations.append(dest)

    # Ajoute une destination aleatoir
    def SetRandomDestination(self):
        gridDeplacement = EventManager.TriggerEvent("getLayerGrid", {"layer": "DeplacementZone"})
        
        index = random.randint(0, len(gridDeplacement) - 1)
        
        tileToGo = gridDeplacement[index]

        dest = [(tileToGo[0] * tileToGo[2]) + (tileToGo[2] / 2), (tileToGo[1] * tileToGo[3]) + (tileToGo[3] / 2)]

        self.SetDestination(dest)

    # set un path aleatoir avec le astar
    def SetRandomBestPathDest(self):
        gridDeplacement = EventManager.TriggerEvent("getLayerGrid", {"layer": "DeplacementZone"})
        
        index = random.randint(0, len(gridDeplacement) - 1)
        tileToGo = gridDeplacement[index]
        dest = [tileToGo[0], tileToGo[1]]

        self.SetBestPathAt(dest)

    # Set le meilleur path avec l'astar à une destination
    def SetBestPathAt(self, dest):
        self.destinations.clear()

        start = [int(self.pos.x / 64), int(self.pos.y / 64)]

        path = EventManager.TriggerEvent("getBestPath", {"dest": dest, "start": start, "currAgent": self})
        if path == None:
            self.currSpeed = 0
            return "boib"

        for dest in path:
            dest[0] *= 64
            dest[1] *= 64
            dest[0] += 32
            dest[1] += 32

            self.AddDestination(dest)
        return path


    # Reprend un nouveau path
    def DodgeObstacle(self, dir):
        if(len(self.destinations) == 0):
            self.AddDestination(self.destination)

        dest = copy.copy(self.destinations[len(self.destinations) - 1])
        
        dest[0] -= 32
        dest[1] -= 32
        dest[0] /= 64
        dest[1] /= 64

        dest[0] = int(dest[0])
        dest[1] = int(dest[1])

        self.destinations.clear()
        self.SetBestPathAt(dest)
        self.InitMove()

    # move dans une direction et update sont forward en consequence de sa destination
    def Move(self, dir:int):
        dt = EventManager.TriggerEvent("getDT", None)
        
        self.UpdateForward()

        self.oldPos = self.pos

        self.pos += self.forward * dir * self.currSpeed * dt
        self.midPos = self.pos + (self.size / 2)

    # met le forward en direction de ca destination
    def UpdateForward(self):
        #pour eviter un bug car on ne peux pas normalizer un vecteur d'une longueur de 0
        if (self.destination - self.pos).length() > 0:
            self.forward = self.destination - self.pos
            self.forward = self.forward.normalize()

        #ici j'inverse l'angle car ca me donne l'angle dans l'autre sens
        self.angle = -self.vectRight.angle_to(self.forward)

    # regarde devant lui a une distance denviron 2 case
    def LookForward(self):
        pos = copy.copy(self.pos)

        pos[0] -= 128
        pos[1] -= 128

        size = self.size * 5

        colliders = EventManager.TriggerEvent("getColliderDanger", None)
        if colliders == None:
            return

        if type(colliders[0]) != list:
            colliders = [colliders]

        collider1 = [pos[0], pos[1], size[0], size[1], self]

        dirActor = [0, 0]

        if self.angle < 10 and self.angle > -10:
            dirActor = [1, 0]
        elif self.angle < 100 and self.angle > 80:
            dirActor = [0, -1]
        elif self.angle < -170 or self.angle > 170:
            dirActor = [-1, 0]
        elif self.angle < -80 and self.angle > -100:
            dirActor = [0, 1]
        elif self.angle <= 80 and self.angle >= 10:
            dirActor = [1, -1]
        elif self.angle <= 170 and self.angle >= 100:
            dirActor = [-1, -1]
        elif self.angle <= -10 and self.angle >= -80:
            dirActor = [1, 1]
        elif self.angle <= -100 and self.angle >= -170:
            dirActor = [-1, 1]

        for collider in colliders:
            dir = EventManager.TriggerEvent("checkColliderWithOther", {"collider1": collider1, "collider2": collider})
            if (dir[0] == dirActor[0] and dir[0] != 0) or (dir[1] == dirActor[1] and dir[1] != 0):
                self.lookForward = True
                self.dangerForward = dir[2]

    # ecoute autour de lui a une distance d'environ 2 case
    def ListenAround(self, param):
        pos = copy.copy(self.pos)

        pos[0] -= 128
        pos[1] -= 128

        size = self.size * 5

        collider1 = [pos[0], pos[1], size[0], size[1], self]
        collider2 = param["ball"].GetColliderBall(None)

        dir = EventManager.TriggerEvent("checkColliderWithOther", {"collider1": collider1, "collider2": collider2})

        if dir[2] != None:
            self.listenAround = True

    # connect le AI a l'interface
    def ConnectToInterface(self):
        EventManager.StartListening("getAgentConnect", self.GetAgent)

    # deconnect l'agent de l'interface
    def DisconnectToInterface(self):
        EventManager.StopListening("getAgentConnect", self.GetAgent)

    # retourn une reference de lui meme
    def GetAgent(self, param):
        return self