from Actor import Actor
import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from EventManager import EventManager

class Map(Actor):
    image:pytmx.TiledMap

    def __init__(self, tag:str, type:str, path:str):
        super().__init__(tag, type)

        EventManager.StartListening("getLayerGrid", self.GetLayerGrid)

        self.image = load_pygame(path)

    def Render(self, screen):
        for i in range(6):
            for x, y, image in self.image.layers[i].tiles():
                screen.blit(image, (x * 64, y * 64))

    # retourn un grid de tout les information sur les tile de la layer
    def GetLayerGrid(self, param):
        gridObstacle = []
        for x, y, image in self.image.layernames[param["layer"]].tiles():
            gridObstacle.append([x, y, 64, 64, image])

        return gridObstacle