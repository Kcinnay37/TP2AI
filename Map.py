from Actor import Actor
import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from EventManager import EventManager

class Map(Actor):
    image:pytmx.TiledMap

    def __init__(self, tag:str, type:str, path:str):
        super().__init__(tag, type)

        EventManager.StartListening("getObstacleGrid", self.GetObstacleGrid)

        self.image = load_pygame(path)

    def Render(self, screen):
        for i in range(len(self.image.layers)):
            for x, y, image in self.image.layers[i].tiles():
                screen.blit(image, (x * 64, y * 64))

    #return vrai si un obstacle ce trouve a ce point
    def CheckObstacle(self, point):
        x = int(point[0] / 64)
        y = int(point[1] / 64)

        for o in self.obstacle:
            if o.ComparPos([x, y]):
                return [x, y]
        return None

    def GetObstacleGrid(self, param):
        gridObstacle = []
        for x, y, image in self.image.layers[2].tiles():
            gridObstacle.append([x, y, 64, 64])

        return gridObstacle