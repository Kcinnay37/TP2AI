from EventManager import EventManager
import math

class PathFinding:
    nodes:dict

    def __init__(self):
        EventManager.StartListening("getBestPath", self.GetBestPath)

        gridDeplacement = EventManager.TriggerEvent("getLayerGrid", {"layer": "DeplacementZone"})
        
        self.nodes = {}

        # ajoute une node dans un dictionnair pour tout les tile de la grid avec leur emplacment comme key
        for tile in gridDeplacement:
            key:str = str(tile[0]) + "," + str(tile[1])
            self.nodes[key] = Node([tile[0], tile[1]])

        # init tout les node en mettant leur voisin
        for node in self.nodes.values():
            node.InitNode(self.nodes)

    # le astar
    def GetBestPath(self, param):
        keyDest = self.ToKey(param["dest"])
        keyStart = self.ToKey(param["start"])

        if not keyDest in self.nodes or not keyStart in self.nodes:
            return None

        for node in self.nodes.values():
            node.ResetNode(999999999)

        self.nodes[keyStart].ResetNode(0)

        dictDeadNode = self.GetDeadGrid(param["currAgent"])

        currKey = keyStart
        while True:
            # dit que la node est visite
            self.nodes[currKey].visite = True

            # set le cost des voisin
            for keyVoisin in self.nodes[currKey].voisins:
                cost = self.GetDistance(keyVoisin, keyDest) + self.nodes[currKey].cost
                if not self.nodes[keyVoisin].visite:
                    self.nodes[keyVoisin].cost = cost
                    self.nodes[keyVoisin].keyFrom = currKey
                else:
                    if cost < self.nodes[keyVoisin].cost:
                        self.nodes[keyVoisin].cost = cost
                        self.nodes[keyVoisin].keyFrom = currKey
                        #self.nodes[keyVoisin].visite = False

            destination = self.nodes[currKey].keyFrom
            costDestination = 999999999

            # prend la destination la moin cher
            for keyVoisin in self.nodes[currKey].voisins:
                if not self.nodes[keyVoisin].visite and not keyVoisin in dictDeadNode:
                    if self.nodes[keyVoisin].cost < costDestination:
                        destination = self.ToKey(self.nodes[keyVoisin].pos)
                        costDestination = self.nodes[keyVoisin].cost

            currKey = destination
            # si chemin inateniable
            if currKey == "":
                return None
            # si toute possibiliter regarder
            if currKey == keyStart:
                break
        
        path = []

        currKey = keyDest

        # set le best path
        while currKey != keyStart:
            path.append(self.ToValue(currKey))
            currKey = self.nodes[currKey].keyFrom
            if currKey == "":
                return None

        path.reverse()
        return path

    # retourn une gris de tout les case avec un agent par dessus
    def GetDeadGrid(self, currAgent):
        colliders = EventManager.TriggerEvent("getCollidersAgents", None)
        if colliders == None:
            return None
        
        dictDeadGrid = {}

        for collider in colliders:
            upLeftCorner = [int((collider[0]) / 64), int((collider[1]) / 64)]
            upRightCorner = [int((((collider[0]) + collider[2])) / 64), int((collider[1]) / 64)]
            downLeftCorner = [int((collider[0]) / 64), int(((collider[1] + collider[3])) / 64)]
            downRightCorner = [int(((collider[0] + collider[2])) / 64), int(((collider[1] + collider[3])) / 64)]

            if collider[4].pos.x == currAgent.pos.x and collider[4].pos.y == currAgent.pos.y:
                continue

            dictDeadGrid[self.ToKey(upLeftCorner)] = 1
            dictDeadGrid[self.ToKey(upRightCorner)] = 1
            dictDeadGrid[self.ToKey(downLeftCorner)] = 1
            dictDeadGrid[self.ToKey(downRightCorner)] = 1

        return dictDeadGrid

    # get la distance entre duex case
    def GetDistance(self, startKey, destKey):
        startPos = self.ToValue(startKey)
        destPos = self.ToValue(destKey)

        a = abs(destPos[0] - startPos[0])
        b = abs(destPos[1] - startPos[1])

        a = math.pow(a, 2)
        b = math.pow(b, 2)
        
        c = math.sqrt(a + b)

        return c

    # transform une value en key
    def ToKey(self, value):
        return str(value[0]) + "," + str(value[1])
    
    # transform un key en value
    def ToValue(self, key):
        value1:str = ""
        value2:str = ""

        first:bool = True
        for c in key:
            if c == ',':
                first = False
                continue

            if first:
                value1 += c
            else:
                value2 += c

        return [int(value1), int(value2)]



class Node:
    voisins:list
    pos:list
    cost:int
    visite:bool
    keyFrom:str

    def __init__(self, pos):
        self.pos = pos
        self.cost = 999999999
        self.voisins = []
        self.visite = False

    # mets c'est voisin
    def InitNode(self, nodes:dict):
        keyLeft = self.ToKey([self.pos[0] - 1, self.pos[1]])
        keyRight = self.ToKey([self.pos[0] + 1, self.pos[1]])
        keyUp = self.ToKey([self.pos[0], self.pos[1] - 1])
        keyDown = self.ToKey([self.pos[0], self.pos[1] + 1])

        self.CheckAddVoisin(keyLeft, nodes)
        self.CheckAddVoisin(keyRight, nodes)
        self.CheckAddVoisin(keyUp, nodes)
        self.CheckAddVoisin(keyDown, nodes)

        if keyLeft in nodes and keyUp in nodes:
            keyLeftUp = self.ToKey([self.pos[0] - 1, self.pos[1] - 1])
            self.CheckAddVoisin(keyLeftUp, nodes)
        if keyRight in nodes and keyUp in nodes:
            keyRightUp = self.ToKey([self.pos[0] + 1, self.pos[1] - 1])
            self.CheckAddVoisin(keyRightUp, nodes)
        if keyLeft in nodes and keyDown in nodes:
            keyLeftDown = self.ToKey([self.pos[0] - 1, self.pos[1] + 1])
            self.CheckAddVoisin(keyLeftDown, nodes)
        if keyRight in nodes and keyDown in nodes:
            keyRightDown = self.ToKey([self.pos[0] + 1, self.pos[1] + 1])
            self.CheckAddVoisin(keyRightDown, nodes)



        # for y in range(3):
        #     for x in range(3):
        #         if self.pos[0] == currPos[0] + x and self.pos[1] == currPos[1] + y:
        #             continue
                
        #         key = str(currPos[0] + x) + "," + str(currPos[1] + y)
        #         if key in nodes:
        #             self.voisins.append(key)

    # check si il peut ajouter le voisin
    def CheckAddVoisin(self, key, nodes):
        if key in nodes:
            self.voisins.append(key)

    # reset les valeurs de la nodoe
    def ResetNode(self, cost):
        self.cost = cost 
        self.visite = False
        self.keyFrom = ""

    # transform une value en key
    def ToKey(self, value):
        return str(value[0]) + "," + str(value[1])