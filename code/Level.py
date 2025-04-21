#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import json
import os
from code.Player import Player
from code.EntityFactory import EntityFactory
from code.Const import WIN_WIDTH, WIN_HEIGHT

SCORE_FILE = './scores.json'

def save_score(score):
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'w') as f:
            json.dump([], f)
    with open(SCORE_FILE, 'r') as f:
        scores = json.load(f)
    scores.insert(0, score)
    scores = scores[:10]
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    return []

class Level:
    def __init__(self, window, name="Fase Espacial"):
        pygame.mixer.init()
        pygame.mixer_music.load('./asset/bg_music.wav')
        pygame.mixer_music.play(-1)

        self.window = window
        self.name = name
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0
        self.running = True

        self.background = pygame.image.load('./asset/stage_space.png').convert()
        self.bg_x1 = 0
        self.bg_x2 = self.background.get_width()
        self.bg_speed = 2

        self.background2 = pygame.image.load('./asset/stage_space_overlay.png').convert_alpha()
        self.background2.set_alpha(100)
        self.bg2_x1 = 0
        self.bg2_x2 = self.background2.get_width()
        self.bg2_speed = 1

        self.score = 0
        self.font = pygame.font.SysFont("Lucida Sans TypeWriter", 20)
        self.hit_sound = pygame.mixer.Sound('./asset/hit.wav')

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause_menu()

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.append(bullet)

    def pause_menu(self):
        pause_font = pygame.font.SysFont("Lucida Sans TypeWriter", 28)
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False

            self.window.blit(self.background, (self.bg_x1, 0))
            self.window.blit(self.background, (self.bg_x2, 0))
            self.window.blit(self.background2, (self.bg2_x1, 0))
            self.window.blit(self.background2, (self.bg2_x2, 0))

            pause_text = pause_font.render("Jogo Pausado", True, (255, 255, 255))
            continue_text = self.font.render("Pressione ESC para continuar", True, (200, 200, 200))

            self.window.blit(pause_text, (WIN_WIDTH // 2 - pause_text.get_width() // 2, 180))
            self.window.blit(continue_text, (WIN_WIDTH // 2 - continue_text.get_width() // 2, 230))

            pygame.display.flip()
            self.clock.tick(10)

    def update(self):
        self.player.update()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen():
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.off_screen():
                self.enemies.remove(enemy)

            bullet = enemy.shoot()
            if bullet:
                self.bullets.append(bullet)

        for enemy in self.enemies[:]:
            if enemy.is_dead():
                self.enemies.remove(enemy)

        self.spawn_timer += 1
        if self.spawn_timer >= 40:
            enemy = EntityFactory.create_enemy()
            self.enemies.append(enemy)
            self.spawn_timer = 0

        self.check_collisions()

        self.bg_x1 -= self.bg_speed
        self.bg_x2 -= self.bg_speed
        if self.bg_x1 <= -self.background.get_width():
            self.bg_x1 = self.background.get_width()
        if self.bg_x2 <= -self.background.get_width():
            self.bg_x2 = self.background.get_width()

        self.bg2_x1 -= self.bg2_speed
        self.bg2_x2 -= self.bg2_speed
        if self.bg2_x1 <= -self.background2.get_width():
            self.bg2_x1 = self.background2.get_width()
        if self.bg2_x2 <= -self.background2.get_width():
            self.bg2_x2 = self.background2.get_width()

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect) and bullet.speed > 0 and not enemy.dying:
                    self.hit_sound.play()
                    self.bullets.remove(bullet)
                    enemy.start_dying()
                    self.score += 100
                    break

        for bullet in self.bullets[:]:
            if bullet.rect.colliderect(self.player.rect) and bullet.speed < 0:
                self.hit_sound.play()
                self.bullets.remove(bullet)
                self.player.take_damage(1)

        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect) and not enemy.dying:
                self.hit_sound.play()
                enemy.start_dying()
                self.player.take_damage(1)

        if self.player.health <= 0:
            save_score(self.score)
            self.show_game_over()
            self.running = False

    def draw(self):
        self.window.blit(self.background, (self.bg_x1, 0))
        self.window.blit(self.background, (self.bg_x2, 0))
        self.window.blit(self.background2, (self.bg2_x1, 0))
        self.window.blit(self.background2, (self.bg2_x2, 0))

        self.player.draw(self.window)

        for bullet in self.bullets:
            bullet.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw_health_bar(self.window)
        life_text = self.font.render("LIFE", True, (255, 255, 255))
        self.window.blit(life_text, (20, 0))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, 20))
        self.window.blit(score_text, score_rect)

        pygame.display.flip()

    def show_game_over(self):
        bg_x1 = 0
        bg_x2 = self.background.get_width()
        bg2_x1 = 0
        bg2_x2 = self.background2.get_width()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            bg_x1 -= self.bg_speed
            bg_x2 -= self.bg_speed
            if bg_x1 <= -self.background.get_width():
                bg_x1 = self.background.get_width()
            if bg_x2 <= -self.background.get_width():
                bg_x2 = self.background.get_width()

            bg2_x1 -= self.bg2_speed
            bg2_x2 -= self.bg2_speed
            if bg2_x1 <= -self.background2.get_width():
                bg2_x1 = self.background2.get_width()
            if bg2_x2 <= -self.background2.get_width():
                bg2_x2 = self.background2.get_width()

            self.window.blit(self.background, (bg_x1, 0))
            self.window.blit(self.background, (bg_x2, 0))
            self.window.blit(self.background2, (bg2_x1, 0))
            self.window.blit(self.background2, (bg2_x2, 0))

            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
            retry_text = self.font.render("Pressione ENTER para voltar ao menu", True, (255, 255, 255))

            self.window.blit(game_over_text, (WIN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
            self.window.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 200))
            self.window.blit(retry_text, (WIN_WIDTH // 2 - retry_text.get_width() // 2, 260))

            pygame.display.flip()
            self.clock.tick(60)
