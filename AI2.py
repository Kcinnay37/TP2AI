import pygame
from Agent import Agent
from EventManager import EventManager

class AI(Agent):

    def __init__(self, tag:str, type:str, imagePath1:str, imagePath2:str):
        super().__init__(tag, type, imagePath1, imagePath2)