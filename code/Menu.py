#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from code.Const import MENU_OPTION, WIN_WIDTH, TEXT_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        start_y = 370
        spacing = 20

        while True:
            self.window.blit(self.surf, self.rect)

            for i, option in enumerate(MENU_OPTION):
                self.menu_text(
                    20,
                    option,
                    TEXT_WHITE,
                    (WIN_WIDTH / 1.95, start_y + i * spacing)
                )

            pygame.display.flip()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Lucida Sans TypeWriter', text_size)
        text_surf: Surface = text_font.render(text, True, text_color)
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
