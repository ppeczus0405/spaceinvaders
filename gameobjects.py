import pygame
import os
import config
from enum import Enum, auto

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))


# Support function
def load_surface_and_scale(surfName, width = 0, height = 0):
    loaded_image =  pygame.image.load(os.path.join("assets", surfName))
    if width > 0 and height > 0:
        return pygame.transform.scale(loaded_image, (width, height))
    img_width = loaded_image.get_rect().width
    img_height = loaded_image.get_rect().height
    return pygame.transform.scale(loaded_image, (int(img_width * config.SCALE_OBJECTS), int(img_height * config.SCALE_OBJECTS)))


# Pygame surfaces for each game element
BACKGROUND = load_surface_and_scale("background-black.png", config.WIDTH, config.HEIGHT)

# Enemy ships
RED_ENEMY_SHIP = load_surface_and_scale("pixel_ship_red_small.png")
GREEN_ENEMY_SHIP = load_surface_and_scale("pixel_ship_green_small.png")
BLUE_ENEMY_SHIP = load_surface_and_scale("pixel_ship_blue_small.png")

# Lasers
RED_LASER = load_surface_and_scale("pixel_laser_red.png")
GREEN_LASER = load_surface_and_scale("pixel_laser_green.png")
BLUE_LASER = load_surface_and_scale("pixel_laser_blue.png")
PLAYER_LASER = load_surface_and_scale("pixel_laser_yellow.png")

# Player
PLAYER_SHIP = load_surface_and_scale("pixel_ship_yellow.png")


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()


# Base class for Player, Enemy classes
class Ship:
    def __init__(self, x, y, color, health=100):
        self.x = x
        self.y = y
        self.color = color
        self.max_health = health
        self.health = health
        self.alive = health > 0
        self.texture = None
        self.mask = None
        self.lasers = set()

    def render(self):
        screen.blit(self.texture, (self.x, self.y))
        for laser in self.lasers:
            laser.render()

    def render_hp(self, hp_y):
        hp_ratio = self.health / self.max_health
        green_width = max(0, int(hp_ratio * self.texture.get_width()))
        red_width = self.texture.get_width() - green_width
        green = (0, 255, 0)
        red = (255, 0, 0)
        pygame.draw.rect(screen, green,
                         pygame.Rect(self.x, hp_y, green_width, config.HP_HEIGHT))
        pygame.draw.rect(screen, red,
                         pygame.Rect(self.x + green_width, hp_y, red_width, config.HP_HEIGHT))

    def spawn_laser(self):
        self.lasers.add(Laser(self.x, self.y - config.LASER_CORRECTION, config.LASER_POWER, self.color))

    def delete_outside_lasers(self):
        to_delete = None
        for laser in self.lasers:
            if not laser.is_inside():
                to_delete = laser
        if to_delete is not None:
            self.lasers.remove(to_delete)

    def collide(self, other):
        offset = (other.x - self.x, other.y - self.y)
        return self.mask.overlap(other.mask, offset) is not None

    def get_wounded(self, hp):
        self.health -= hp
        if self.health <= 0:
            self.alive = False

    def update_shots(self, other_ship):
        hitted = []
        for laser in other_ship.lasers:
            if self.collide(laser):
                self.get_wounded(laser.hp)
                hitted.append(laser)
        for h in hitted:
            other_ship.lasers.remove(h)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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
        self.mask = pygame.mask.from_surface(self.texture)

    def move(self, dy):
        self.y += dy

    def render(self):
        screen.blit(self.texture, (self.x, self.y))

    def is_inside(self):
        return (self.y + self.texture.get_height() >= 0
                and self.y <= config.HEIGHT
                and self.x <= config.WIDTH
                and self.x + self.texture.get_width() >= 0)


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, Color.YELLOW, config.PLAYER_MAX_HEALTH)
        self.texture = PLAYER_SHIP
        self.mask = pygame.mask.from_surface(self.texture)

    def move(self, dx, dy):
        self.x = max(-config.SHIP_CORRECTION, min(self.x + dx,
                                                    config.WIDTH - self.texture.get_width() + config.SHIP_CORRECTION))
        self.y = max(-config.SHIP_CORRECTION, min(self.y + dy,
                                                    config.HEIGHT - self.texture.get_height()))

    def render(self):
        super().render()
        super().render_hp(self.y + self.texture.get_height() + config.SHIP_CORRECTION)


class Enemy(Ship):
    dict = {Color.RED: RED_ENEMY_SHIP,
            Color.BLUE: BLUE_ENEMY_SHIP,
            Color.GREEN: GREEN_ENEMY_SHIP}

    def __init__(self, x, color, health=config.ENEMY_BASE_HEALTH):
        super().__init__(x, config.ENEMY_START_Y, color, health)
        self.texture = Enemy.dict[color]
        self.mask = pygame.mask.from_surface(self.texture)

    def render(self):
        super().render()
        super().render_hp(self.y - config.SHIP_CORRECTION)

