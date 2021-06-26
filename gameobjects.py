import pygame
import os
import config
from enum import Enum, auto


# Support functions
def load_surface_and_scale(surf_name, width=0, height=0):
    loaded_image = pygame.image.load(os.path.join("assets", surf_name))
    if width > 0 and height > 0:
        return pygame.transform.scale(loaded_image, (width, height))
    img_width = loaded_image.get_rect().width
    img_height = loaded_image.get_rect().height
    return pygame.transform.scale(loaded_image, (int(img_width * config.SCALE_OBJECTS),
                                                 int(img_height * config.SCALE_OBJECTS)))


def is_inside_window(obj):
    return (obj.y + obj.texture.get_height() >= 0
            and obj.y <= config.HEIGHT
            and obj.x <= config.WIDTH
            and obj.x + obj.texture.get_width() >= 0)


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()


# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = pygame.font.Font(os.path.join("assets", "Premier.ttf"), config.FONT_SIZE)
icon = load_surface_and_scale("icon.png", 50, 50)
pygame.display.set_icon(icon)
pygame.display.set_caption("SpaceInvaders v.1.0")

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
