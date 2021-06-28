import config
import pygame
import gameobjects
from gameobjects import screen, end_font


class EndUI:
    def __init__(self, score):
        self.__score = score
        self.__quit_texture = gameobjects.QUIT
        self.__retry_texture = gameobjects.RETRY
        width_correct = (config.WIDTH - 2 * self.__quit_texture.get_width()) / 3
        retry_x =  self.__quit_texture.get_width() + 2 * width_correct
        self.__quit_position = (width_correct, config.BUTTON_Y)
        self.__retry_position = (retry_x, config.BUTTON_Y)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.__is_inside(mouse_pos, self.__quit_position):
            self.__quit_texture = gameobjects.QUIT_HOVER
            self.__retry_texture = gameobjects.RETRY
        elif self.__is_inside(mouse_pos, self.__retry_position):
            self.__retry_texture = gameobjects.RETRY_HOVER
            self.__quit_texture = gameobjects.QUIT
        else:
            self.__quit_texture = gameobjects.QUIT
            self.__retry_texture = gameobjects.RETRY

    def render(self):
        blur_surf = pygame.Surface((config.WIDTH, config.HEIGHT))
        blur_surf.set_alpha(240)
        blur_surf.fill((0, 0, 0))
        color = (255, 255, 90)
        string_surf = end_font.render("Your Score:", False, color)
        score_surf = end_font.render(str(self.__score), False, color)
        screen.blit(blur_surf, (0, 0))
        screen.blit(string_surf, ((config.WIDTH - string_surf.get_width()) / 2,
                                  config.HEIGHT / 2 - string_surf.get_height() - config.END_HEIGHT_CORRECTION))
        screen.blit(score_surf, ((config.WIDTH - score_surf.get_width()) / 2,
                                 config.HEIGHT / 2 - config.END_HEIGHT_CORRECTION))
        screen.blit(self.__quit_texture, self.__quit_position)
        screen.blit(self.__retry_texture, self.__retry_position)

    def is_quit(self):
        return self.__is_inside(pygame.mouse.get_pos(), self.__quit_position)

    def is_retry(self):
        return self.__is_inside(pygame.mouse.get_pos(), self.__retry_position)

    def __is_inside(self, mouse_position, button_position):
        button_width = self.__quit_texture.get_width()
        button_height = self.__quit_texture.get_height()
        return (button_position[0] <= mouse_position[0] <= button_position[0] + button_width and
                button_position[1] <= mouse_position[1] <= button_position[1] + button_height)
