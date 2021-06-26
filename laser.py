import pygame
import gameobjects
import config
from gameobjects import Color, screen


# This class describes ships weapon
class Laser:
    dict = {Color.RED: gameobjects.RED_LASER,
            Color.GREEN: gameobjects.GREEN_LASER,
            Color.BLUE: gameobjects.BLUE_LASER,
            Color.YELLOW: gameobjects.PLAYER_LASER}

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.hp = config.LASER_POWER
        self.texture = Laser.dict[color]
        self.mask = pygame.mask.from_surface(self.texture)

    def move(self, dy):
        self.y += dy

    def render(self):
        screen.blit(self.texture, (self.x, self.y))
