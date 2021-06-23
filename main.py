import pygame
import os

BACKGROUND = pygame.image.load(os.path.join("assets", "background-black.png"))
# Enemy ships
RED_ENEMY_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_ENEMY_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small"))

if __name__ == '__main__':
    print("SpaceInvaders!")