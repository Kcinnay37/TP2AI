from EventManager import EventManager

class ColliderManager:
    
    def __init__(self):
        EventManager.StartListening("checkOutOfMap", self.CheckOutOfMap)
        EventManager.StartListening("checkColliderWithMap", self.CheckColliderWithMap)
        EventManager.StartListening("checkColliderWithAgents", self.CheckColliderWithAgents)
        EventManager.StartListening("checkColliderWithBalls", self.CheckColliderWithBalls)

    def CheckOutOfMap(self, param):
        x = 0
        y = 1

        dir = [0, 0]

        screenSize = EventManager.TriggerEnter("getScreenSize", None)
        if screenSize == None:
            return

        if param["pos"][x] <= 0:
            dir[0] = -1
        if param["pos"][x] + param["size"][x] >= screenSize[x]:
            dir[0] = 1
        if param["pos"][y] <= 0:
            dir[1] = -1
        if param["pos"][y] + param["size"][y] >= screenSize[y]:
            dir[1] = 1
        
        return dir

    def CheckColliderWithMap(self, param):
        x = 0
        y = 1
        
        gridCollider = EventManager.TriggerEnter("getObstacleGrid", None)
        if gridCollider == None:
            return

        pos = param["pos"]
        size = param["size"]

        dir = [0, 0]

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

        return dir

    def CheckColliderWithAgents(self, param):
        x = 0
        y = 1

        currPos = param["pos"]
        currSize = param["size"]

        colliders = EventManager.TriggerEnter("getCollidersAgents", None)
        if colliders == None:
            return

        dir = [0, 0, ""]

        if colliders == None:
            return dir

        if type(colliders[0]) != list:
            colliders = [colliders]

        for collider in colliders:
            otherPos = [collider[0], collider[1]]
            otherSize = [collider[2], collider[3]]
            otherType = collider[4]

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

                dir[len(tempDir)] = otherType

        return dir
            
    def CheckColliderWithBalls(self, param):
        x = 0
        y = 1

        currPos = param["pos"]
        currSize = param["size"]

        colliders = EventManager.TriggerEnter("getCollidersBalls", None)

        dir = [0, 0, ""]

        if colliders == None:
            return dir

        if type(colliders[0]) != list:
            colliders = [colliders]

        for collider in colliders:
            otherPos = [collider[0], collider[1]]
            otherSize = [collider[2], collider[3]]
            otherType = collider[4]

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

                dir[len(tempDir)] = otherType

        return dir

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