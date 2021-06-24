import pygame
import gameobjects
import config
from gameobjects import screen, Player, Enemy

class Game:
    def __init__(self):
        self.enemies= []
        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.running = True

    def is_running(self):
        return self.running

    def update(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        screen.fill((0, 0, 0))
        screen.blit(gameobjects.BACKGROUND, (0, 0))
        self.player.render()
        for enemy in self.enemies:
            enemy.render()
        pygame.display.flip()
