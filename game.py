import pygame
import gameobjects
import config
import random
from gameobjects import screen, font, Player, Enemy, Color


class Game:
    def __init__(self):
        self.enemies = set()
        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.level = 0
        self.levelup_score = config.FIRST_LEVEL_SCORE
        self.spawn = 1
        self.chance = config.SPAWN_ENEMY_CHANCE
        self.running = True

    def is_running(self):
        return self.running

    def update(self):
        self._update_shots_and_enemies()
        self._delete_out_enemies()
        self._update_level()
        self._update_enemy_spawn()
        self.player.update()

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
        self._score_display()
        pygame.display.flip()

    def _update_enemy_spawn(self):
        many_spawned = 0
        for i in range(self.spawn):
            if self._spawn_enemy():
                many_spawned += 1
        self.spawn -= many_spawned
        r = int(random.random() * (config.SPAWN_ENEMY_CHANCE -
                                   self.level * config.LEVEL_CHANCE))
        if not r:
            self.spawn += random.choices((1, 2, 3),
                                         weights=[0.95, 0.04, 0.01], k=1)[0]

    def _update_level(self):
        if self.player.score >= self.levelup_score:
            self.level += 1
            self.levelup_score = int(self.levelup_score * config.NEXT_LEVEL_BASE)

    def _delete_out_enemies(self):
        out = [e for e in self.enemies
               if not gameobjects.is_inside_window(e)]
        for o in out:
            if o.is_alive():
                self.player.get_wounded()
            self.enemies.remove(o)

    def _score_display(self):
        score_string = "Score: " + str(self.player.score)
        font_surface = font.render(score_string, False, (255, 255, 255))
        screen.blit(font_surface, (config.FONT_X, 0))

    def _update_shots_and_enemies(self):
        for e in self.enemies:
            alive_before = e.is_alive()
            e.update_shots(self.player)
            self.player.update_shots(e)
            if e.collide(self.player):
                e.alive = False
                self.player.get_wounded()
            if alive_before ^ e.is_alive():
                self.player.score += 1
            e.update()

    def _spawn_enemy(self):
        trials = config.SPAWN_ENEMY_TRIALS
        success = False
        while trials > 0 and not success:
            success = True
            color = random.choice((Color.RED, Color.GREEN, Color.BLUE))
            enemy = Enemy(0, color, self.level)
            enemy.x = int(random.random() * (config.WIDTH - enemy.texture.get_width() - config.SHIP_CORRECTION))
            for e in self.enemies:
                if e.collide(enemy):
                    success = False
                    break
            if success:
                self.enemies.add(enemy)
                return True
            trials -= 1
        return False
