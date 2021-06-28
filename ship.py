import pygame
import config
from gameobjects import screen, is_inside_window


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
        if self.alive:
            screen.blit(self.texture, (int(self.x), int(self.y)))
        for laser in self.lasers:
            laser.render()

    def render_hp(self, hp_y):
        if not self.alive:
            return

        hp_ratio = self.health / self.max_health
        green_width = max(0, int(hp_ratio * self.texture.get_width()))
        red_width = self.texture.get_width() - green_width
        green = (0, 255, 0)
        red = (255, 0, 0)
        pygame.draw.rect(screen, green,
                         pygame.Rect(int(self.x), int(hp_y), green_width, config.HP_HEIGHT))
        pygame.draw.rect(screen, red,
                         pygame.Rect(int(self.x + green_width), int(hp_y), red_width, config.HP_HEIGHT))

    def delete_outside_lasers(self):
        to_delete = None
        for laser in self.lasers:
            if not is_inside_window(laser):
                to_delete = laser
                break
        if to_delete is not None:
            self.lasers.remove(to_delete)

    def collide(self, other):
        if not self.alive:
            return False

        offset = (int(other.x - self.x), int(other.y - self.y))
        return self.mask.overlap(other.mask, offset) is not None

    def get_wounded(self, hp=config.LASER_POWER):
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
