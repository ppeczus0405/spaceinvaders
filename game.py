import pygame
import gameobjects
import config
import random
from player import Player
from enemy import Enemy
from gameobjects import screen, game_font, begin_font, Color
from endmenu import EndUI


class Game:
    def __init__(self):
        self.is_game_start = True
        self.enemies = set()
        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.to_spawn = -(2**100)
        self.level = 0
        self.levelup_score = config.FIRST_LEVEL_SCORE
        self.chance = config.SPAWN_ENEMY_CHANCE
        self.running = True
        self.end_ui = None

    @staticmethod
    def how_many_spawn():
        return random.choices((1, 2, 3),
                              weights=[config.SINGLE_SPAWN_PROB,
                                       config.DOUBLE_SPAWN_PROB,
                                       config.TRIPLE_SPAWN_PROB], k=1)[0]

    @staticmethod
    def render_begin_string():
        begin_string = "Press SPACE to start the game ..."
        begin_surface = begin_font.render(begin_string, False, (255, 255, 255))
        begin_x = (config.WIDTH - begin_surface.get_width()) / 2
        begin_y = ((config.HEIGHT - begin_surface.get_height()) / 2)
        screen.blit(begin_surface, (begin_x, begin_y))

    def is_running(self):
        return self.running

    def update(self):
        self._update_shots_and_enemies()
        self._delete_out_enemies()
        self._update_level()
        self._update_enemy_spawn()
        self.player.update()
        if not self.player.is_alive() and self.end_ui is None:
            self.end_ui = EndUI(self.player.score)
            self.to_spawn = -(2**100)
        if self.end_ui is not None:
            self.end_ui.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.is_game_start:
                        self.is_game_start = False
                        self.to_spawn = 1
                    self.player.spawn_laser()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.end_ui is not None:
                    if self.end_ui.is_retry():
                        self._restart_game()
                    elif self.end_ui.is_quit():
                        self.running = False

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
        if self.is_game_start:
            Game.render_begin_string()
        self.player.render()
        for enemy in self.enemies:
            enemy.render()
        self._lives_and_score_display()
        if self.end_ui is not None:
            self.end_ui.render()
        pygame.display.flip()

    def _update_enemy_spawn(self):
        if not self._count_alive_enemies() and not self.to_spawn:
            self.to_spawn += Game.how_many_spawn()
        many_spawned = 0
        for i in range(self.to_spawn):
            if self._spawn_enemy():
                many_spawned += 1
        self.to_spawn -= many_spawned
        r = int(random.random() * (config.SPAWN_ENEMY_CHANCE -
                                   self.level * config.LEVEL_CHANCE))
        if not r:
            self.to_spawn += Game.how_many_spawn()

    def _count_alive_enemies(self):
        return len([e for e in self.enemies if e.is_alive()])

    def _update_level(self):
        if self.player.score >= self.levelup_score:
            self.level += 1
            self.levelup_score = int(self.levelup_score * config.NEXT_LEVEL_BASE)

    def _delete_out_enemies(self):
        out = [e for e in self.enemies
               if not gameobjects.is_inside_window(e)]
        for o in out:
            if o.is_alive():
                self.player.get_wounded(config.ENEMY_COLLISION_HP)
            self.enemies.remove(o)

    def _lives_and_score_display(self):
        score_string = "Score: " + str(self.player.score)
        lives_string = "Lives: " + str(self.player.lives)
        font_surface = game_font.render(score_string, False, (255, 255, 255))
        screen.blit(font_surface, (config.SCORE_X, 0))
        font_surface = game_font.render(lives_string, False, (255, 255, 255))
        screen.blit(font_surface, (config.LIVES_X, 0))

    def _update_shots_and_enemies(self):
        for e in self.enemies:
            alive_before = e.is_alive()
            e.update_shots(self.player)
            self.player.update_shots(e)
            if e.collide(self.player) and self.player.is_alive():
                e.alive = False
                self.player.get_wounded(config.ENEMY_COLLISION_HP)
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

    def _restart_game(self):
        self.__init__()
