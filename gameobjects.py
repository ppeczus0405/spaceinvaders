import pygame
import os
import config
from enum import Enum, auto

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))


# Support function
def load_surface(surfName):
    return pygame.image.load(os.path.join("assets", surfName))


# Pygame surfaces for each game element
BACKGROUND = pygame.transform.scale(load_surface("background-black.png"), (config.WIDTH, config.HEIGHT))

# Enemy ships
RED_ENEMY_SHIP = load_surface("pixel_ship_red_small.png")
GREEN_ENEMY_SHIP = load_surface("pixel_ship_green_small.png")
BLUE_ENEMY_SHIP = load_surface("pixel_ship_green_small.png")

# Lasers
RED_LASER = load_surface("pixel_laser_red.png")
GREEN_LASER = load_surface("pixel_laser_green.png")
BLUE_LASER = load_surface("pixel_laser_blue.png")
PLAYER_LASER = load_surface("pixel_laser_yellow.png")

# Player
PLAYER_SHIP = load_surface("pixel_ship_yellow.png")


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()


# Base class for Player, Enemy classes
class Ship:
    def __init__(self, x, y, color, health = 100):
        self.x = x
        self.y = y
        self.color = color
        self.health = health
        self.alive = health > 0
        self.texture = None
        self.lasers = []

    def render(self):
        screen.blit(self.texture, (self.x, self.y))
        for laser in self.lasers:
            laser.render()

    def get_wounded(self, hp):
        self.health -= hp
        if self.health <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive


# This class describes ships weapon
class Laser:
    dict = {Color.RED: RED_LASER,
            Color.GREEN: GREEN_LASER,
            Color.BLUE: BLUE_LASER,
            Color.YELLOW: PLAYER_LASER}

    def __init__(self, x, y, hp, color):
        self.x = x
        self.y = y
        self.hp = hp
        self.texture = Laser.dict[color]

    def move(self, dy):
        self.y += dy

    def render(self):
        screen.blit(self.texture, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, Color.YELLOW, health)
        self.texture = PLAYER_SHIP

    def move(self, dx):
        self.x += dx


class Enemy(Ship):
    dict = {Color.RED : RED_ENEMY_SHIP,
            Color.BLUE : BLUE_ENEMY_SHIP,
            Color.GREEN : GREEN_ENEMY_SHIP}

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, color, health)
        self.texture = Enemy.dict[color]
