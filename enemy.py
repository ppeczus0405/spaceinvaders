import random
import gameobjects
import config
import pygame
from gameobjects import Color
from ship import Ship
from laser import Laser


class Enemy(Ship):
    dict = {Color.RED: (gameobjects.RED_ENEMY_SHIP, config.LASER_CORRECTION_RG_X, config.LASER_CORRECTION_RG_Y),
            Color.BLUE: (gameobjects.BLUE_ENEMY_SHIP, config.LASER_CORRECTION_B_X, config.LASER_CORRECTION_B_Y),
            Color.GREEN: (gameobjects.GREEN_ENEMY_SHIP, config.LASER_CORRECTION_RG_X, config.LASER_CORRECTION_RG_Y)}

    def __init__(self, x, color, level):
        super().__init__(x, config.ENEMY_START_Y,
                         color, config.ENEMY_BASE_HEALTH + level * config.LEVEL_HP)
        self.speed = config.ENEMY_BASE_SPEED + level * config.LEVEL_SPEED
        self.chance = config.ENEMY_BASE_CHANCE - level * config.LEVEL_CHANCE
        self.texture = Enemy.dict[color][0]
        self.mask = pygame.mask.from_surface(self.texture)

    def spawn_laser(self):
        if self.is_alive():
            self.lasers.add(Laser(self.x + Enemy.dict[self.color][1],
                                  self.y + Enemy.dict[self.color][2],
                                  self.color))

    def render(self):
        super().render()
        super().render_hp(self.y - config.SHIP_CORRECTION)

    def update(self):
        self.move(0, self.speed)
        r = int(random.random() * self.chance)
        if not r:
            self.spawn_laser()
        for laser in self.lasers:
            laser.move(config.LASER_MOVE)
