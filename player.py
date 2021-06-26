import config
import pygame
from gameobjects import Color, PLAYER_SHIP
from ship import Ship
from laser import Laser


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, Color.YELLOW, config.PLAYER_MAX_HEALTH)
        self.texture = PLAYER_SHIP
        self.mask = pygame.mask.from_surface(self.texture)
        self.score = 0

    def move(self, dx, dy):
        self.x = max(-config.SHIP_CORRECTION, min(self.x + dx,
                                                  config.WIDTH - self.texture.get_width() + config.SHIP_CORRECTION))
        self.y = max(-config.SHIP_CORRECTION, min(self.y + dy,
                                                  config.HEIGHT - self.texture.get_height()))

    def render(self):
        super().render()
        self.render_hp(self.y + self.texture.get_height() + config.SHIP_CORRECTION)

    def spawn_laser(self):
        self.lasers.add(Laser(self.x, self.y - config.LASER_CORRECTION_PLAYER, self.color))

    def update(self):
        for laser in self.lasers:
            laser.move(-config.LASER_MOVE)
        self.delete_outside_lasers()
