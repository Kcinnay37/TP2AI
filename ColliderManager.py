from EventManager import EventManager
from Actor import Actor

class ColliderManager:
    
    def __init__(self):
        EventManager.StartListening("checkOutOfMap", self.CheckOutOfMap)
        EventManager.StartListening("checkColliderLayer", self.CheckColliderLayer)
        EventManager.StartListening("checkColliderWithAgents", self.CheckColliderWithAgents)
        EventManager.StartListening("checkColliderWithBalls", self.CheckColliderWithBalls)
        EventManager.StartListening("checkColliderWithOther", self.CheckColliderWithOther)

    # regarde si il est hors de la map et regarde la direction
    def CheckOutOfMap(self, param):
        x = 0
        y = 1

        dir = [0, 0, None]

        screenSize = EventManager.TriggerEvent("getScreenSize", None)
        if screenSize == None:
            return

        if param["pos"][x] < 0:
            dir[0] = -1
        if param["pos"][x] + param["size"][x] > screenSize[x]:
            dir[0] = 1
        if param["pos"][y] < 0:
            dir[1] = -1
        if param["pos"][y] + param["size"][y] > screenSize[y]:
            dir[1] = 1

        if dir[0] != 0 or dir[1] != 0:
            dir[2] = Actor("screen", "screen")
        
        return dir

    # regarde si il collide avec un l;ayer et regarde la direction 
    def CheckColliderLayer(self, param):
        x = 0
        y = 1
        
        gridCollider = EventManager.TriggerEvent("getLayerGrid", {"layer": param["layer"]})
        if gridCollider == None:
            return

        pos = param["pos"]
        size = param["size"]

        dir = [0, 0, None]

        for object in gridCollider:
            sizeObject = [object[2], object[3]]
            posObject = [object[0] * sizeObject[x], object[1] * sizeObject[y]]

            if pos[x] <= (posObject[x] + sizeObject[x]) \
                and (pos[x] + size[x]) >= posObject[x] \
                and pos[y] <= (posObject[y] + sizeObject[y]) \
                and (pos[y] + size[y]) >= posObject[y]:

                midPoint1 = [pos[x] + (size[x] / 2), pos[y] + (size[y] / 2)]
                midPoint2 = [posObject[x] + (sizeObject[x] / 2), posObject[y] + (sizeObject[y] / 2)]

                tempDir = self.GetDirPoint(midPoint1, midPoint2)

                for i in range(len(tempDir)):
                    if tempDir[i] != 0:
                        dir[i] = tempDir[i]
                dir[2] = Actor(param["layer"], param["layer"])

        return dir

    # regarde si il collide avec un autre agent et regarde la direction
    def CheckColliderWithAgents(self, param):
        x = 0
        y = 1

        currPos = param["pos"]
        currSize = param["size"]

        colliders = EventManager.TriggerEvent("getCollidersAgents", None)
        if colliders == None:
            return

        dir = [0, 0, None]

        if colliders == None:
            return dir

        if type(colliders[0]) != list:
            colliders = [colliders]

        for collider in colliders:
            otherPos = [collider[0], collider[1]]
            otherSize = [collider[2], collider[3]]

            if currPos[x] == otherPos[x] \
                and currPos[y] == otherPos[y] \
                and currSize[x] == otherSize[x] \
                and currSize[y] == otherSize[y]:

                continue

            if currPos[x] <= (otherPos[x] + otherSize[x]) \
                and (currPos[x] + currSize[x]) >= otherPos[x] \
                and currPos[y] <= (otherPos[y] + otherSize[y]) \
                and (currPos[y] + currSize[y]) >= otherPos[y]:

                midPoint1 = [currPos[x] + (currSize[x] / 2), currPos[y] + (currSize[y] / 2)]
                midPoint2 = [otherPos[x] + (otherSize[x] / 2), otherPos[y] + (otherSize[y] / 2)]

                tempDir = self.GetDirPoint(midPoint1, midPoint2)

                for i in range(len(tempDir)):
                    if tempDir[i] != 0:
                        dir[i] = tempDir[i]

                dir[2] = collider[4]

        return dir
    
    # regarde si il a été toucher par une ball et regarde la direction
    def CheckColliderWithBalls(self, param):
        x = 0
        y = 1

        currPos = param["pos"]
        currSize = param["size"]

        colliders = EventManager.TriggerEvent("getCollidersBalls", None)

        dir = [0, 0, None]

        if colliders == None:
            return dir

        if type(colliders[0]) != list:
            colliders = [colliders]

        for collider in colliders:
            otherPos = [collider[0], collider[1]]
            otherSize = [collider[2], collider[3]]

            if currPos[x] == otherPos[x] \
                and currPos[y] == otherPos[y] \
                and currSize[x] == otherSize[x] \
                and currSize[y] == otherSize[y]:

                continue

            if currPos[x] <= (otherPos[x] + otherSize[x]) \
                and (currPos[x] + currSize[x]) >= otherPos[x] \
                and currPos[y] <= (otherPos[y] + otherSize[y]) \
                and (currPos[y] + currSize[y]) >= otherPos[y]:

                midPoint1 = [currPos[x] + (currSize[x] / 2), currPos[y] + (currSize[y] / 2)]
                midPoint2 = [otherPos[x] + (otherSize[x] / 2), otherPos[y] + (otherSize[y] / 2)]

                tempDir = self.GetDirPoint(midPoint1, midPoint2)

                for i in range(len(tempDir)):
                    if tempDir[i] != 0:
                        dir[i] = tempDir[i]

                dir[2] = collider[4]

        return dir

    # regarde si un collider a collider l'autre et regarde la direction
    def CheckColliderWithOther(self, param):
        collider1 = param["collider1"]
        collider2 = param["collider2"]

        posX = 0
        posY = 1
        sizeX = 2
        sizeY = 3
        
        dir = [0, 0, None]

        if collider1[posX] <= (collider2[posX] + collider2[sizeX]) \
            and (collider1[posX] + collider1[sizeX]) >= collider2[posX] \
            and collider1[posY] <= (collider2[posY] + collider2[sizeY]) \
            and (collider1[posY] + collider1[sizeY]) >= collider2[posY]:

            midPoint1 = [collider1[posX] + (collider1[sizeX] / 2), collider1[posY] + (collider1[sizeY] / 2)]
            midPoint2 = [collider2[posX] + (collider2[sizeX] / 2), collider2[posY] + (collider2[sizeY] / 2)]

            tempDir = self.GetDirPoint(midPoint1, midPoint2)

            for i in range(len(tempDir)):
                if tempDir[i] != 0:
                    dir[i] = tempDir[i]

            dir[2] = collider2[4]

        return dir
    
    # regarde la direction d'un point par rapport a un autre
    def GetDirPoint(self, point1, point2):
        x = 0
        y = 1
        
        distance = [point1[x] - point2[x], point1[y] - point2[y]]
        absDistance = [abs(distance[x]), abs(distance[y])]

        dir = [0, 0]

        if absDistance[x] > absDistance[y]:
            if distance[x] < 0:
                dir[0] = 1
            elif distance[x] > 0:
                dir[0] = -1
        elif absDistance[x] < absDistance[y]:
            if distance[y] < 0:
                dir[1] = 1
            elif distance[y] > 0:
                dir[1] = -1
        else:
            if distance[x] < 0:
                dir[0] = 1
            elif distance[x] > 0:
                dir[0] = -1
            if distance[y] < 0:
                dir[1] = 1
            elif distance[y] > 0:
                dir[1] = -1

        return dir