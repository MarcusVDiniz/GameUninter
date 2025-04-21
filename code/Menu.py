#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import math
import sys
import json
from code.Const import MENU_OPTION, WIN_WIDTH, WIN_HEIGHT, TEXT_WHITE
from code.Level import Level, load_scores

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.selected_index = 0
        self.clock = pygame.time.Clock()

        self.sound_select = pygame.mixer.Sound('./asset/menuoption.wav')
        self.sound_confirm = pygame.mixer.Sound('./asset/menuselect.wav')
        self.font = pygame.font.SysFont("Lucida Sans TypeWriter", 20)

    def run(self):
        pygame.mixer.init()
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        start_y = 390
        spacing = 20

        while True:
            self.window.blit(self.surf, self.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(MENU_OPTION)
                        self.sound_select.play()
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(MENU_OPTION)
                        self.sound_select.play()
                    elif event.key == pygame.K_RETURN:
                        self.sound_confirm.play()
                        self.execute_option(MENU_OPTION[self.selected_index])

            ticks = pygame.time.get_ticks()

            for i, option in enumerate(MENU_OPTION):
                x_pos = WIN_WIDTH / 1.95
                y_pos = start_y + i * spacing

                if i == self.selected_index:
                    scale = 1.0 + 0.05 * math.sin(ticks * 0.005)
                    font_size = int(20 * scale)
                    color = TEXT_WHITE
                else:
                    font_size = 20
                    color = self.rgb_cycle_color(ticks + i * 150)

                self.menu_text(font_size, option, color, (x_pos, y_pos))

            pygame.display.flip()
            self.clock.tick(60)

    def menu_text(self, text_size, text, text_color, text_center_pos):
        text_font = pygame.font.SysFont('Lucida Sans TypeWriter', text_size)
        text_surf = text_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)

    def rgb_cycle_color(self, time_ms):
        frequency = 0.002
        r = int(127 * math.sin(frequency * time_ms + 0) + 128)
        g = int(127 * math.sin(frequency * time_ms + 2) + 128)
        b = int(127 * math.sin(frequency * time_ms + 4) + 128)
        return (r, g, b)

    def execute_option(self, option):
        if option == "EXIT":
            pygame.quit()
            sys.exit()
        elif option == "START GAME":
            level = Level(self.window)
            level.run()
        elif option == "SCORE":
            self.show_scores()

    def show_scores(self):
        scores = load_scores()
        bg = pygame.image.load('./asset/stage_space.png').convert()
        bg2 = pygame.image.load('./asset/stage_space_overlay.png').convert_alpha()
        bg2.set_alpha(100)

        bg_x1 = 0
        bg_x2 = bg.get_width()
        bg2_x1 = 0
        bg2_x2 = bg2.get_width()
        bg_speed = 2
        bg2_speed = 1

        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False

            bg_x1 -= bg_speed
            bg_x2 -= bg_speed
            if bg_x1 <= -bg.get_width():
                bg_x1 = bg.get_width()
            if bg_x2 <= -bg.get_width():
                bg_x2 = bg.get_width()

            bg2_x1 -= bg2_speed
            bg2_x2 -= bg2_speed
            if bg2_x1 <= -bg2.get_width():
                bg2_x1 = bg2.get_width()
            if bg2_x2 <= -bg2.get_width():
                bg2_x2 = bg2.get_width()

            self.window.blit(bg, (bg_x1, 0))
            self.window.blit(bg, (bg_x2, 0))
            self.window.blit(bg2, (bg2_x1, 0))
            self.window.blit(bg2, (bg2_x2, 0))

            title = self.font.render("TOP 10 SCORES", True, (255, 255, 255))
            self.window.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 80))

            for i, score in enumerate(scores):
                score_text = self.font.render(f"{i+1}. {score}", True, (255, 255, 255))
                self.window.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 120 + i * 30))

            back_text = self.font.render("Pressione ESC para voltar", True, (180, 180, 180))
            self.window.blit(back_text, (WIN_WIDTH // 2 - back_text.get_width() // 2, WIN_HEIGHT - 60))

            pygame.display.flip()
            self.clock.tick(60)
