import pygame
from EventManager import EventManager

class Timer:
    clock = None
    dt:float = 0

    def __init__(self):
        EventManager.StartListening("getDT", self.GetDeltaTime)

        self._clock = pygame.time.Clock()

    def Update(self):
        self._dt = self._clock.tick(60)/1000

    def GetDeltaTime(self, param):
        return self._dt
