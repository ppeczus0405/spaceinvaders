import pygame
import gameobjects
import config
from gameobjects import screen, Player, Enemy, Color


class Game:
    def __init__(self):
        self.enemies = {Enemy(50, Color.GREEN), Enemy(200, Color.BLUE), Enemy(350, Color.RED)}
        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.running = True

    def is_running(self):
        return self.running

    def update(self):
        self.update_enemies()
        for laser in self.player.lasers:
            laser.move(-config.LASER_MOVE)
        self.player.delete_outside_lasers()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.spawn_laser()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.player.move(-config.PLAYER_MOVE, 0)
        if pressed[pygame.K_RIGHT]:
            self.player.move(config.PLAYER_MOVE, 0)
        if pressed[pygame.K_UP]:
            self.player.move(0, -config.PLAYER_MOVE)
        if pressed[pygame.K_DOWN]:
            self.player.move(0, config.PLAYER_MOVE)

    def render(self):
        screen.fill((0, 0, 0))
        screen.blit(gameobjects.BACKGROUND, (0, 0))
        self.player.render()
        for enemy in self.enemies:
            enemy.render()
        pygame.display.flip()

    def update_enemies(self):
        dead = []
        for e in self.enemies:
            e.update_shots(self.player)
            if not e.is_alive():
                dead.append(e)
        for d in dead:
            self.enemies.remove(d)