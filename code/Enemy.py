import pygame
import random
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Enemy:
    def __init__(self):
        self.image_original = pygame.image.load('./asset/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (70, 70))
        x = WIN_WIDTH + 40
        y = random.randint(30, WIN_HEIGHT - 30)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 4)
        self.vertical_speed = random.uniform(-1.5, 1.5)
        self.shoot_cooldown = random.randint(60, 120)
        self.bullet_sprite = './asset/bulletenemy.png'
        self.shoot_sound = pygame.mixer.Sound('./asset/shoot.wav')

        self.dying = False
        self.fade_timer = 10

    def update(self):
        if not self.dying:
            self.rect.x -= self.speed
            self.rect.y += self.vertical_speed
            if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
                self.vertical_speed *= -1
            self.vertical_speed += random.uniform(-0.2, 0.2)
            self.vertical_speed = max(-2, min(2, self.vertical_speed))

            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
        else:
            self.fade_timer -= 1
            if self.fade_timer <= 0:
                self.kill()

    def shoot(self):
        if not self.dying and self.shoot_cooldown <= 0:
            self.shoot_cooldown = random.randint(90, 150)
            from code.Bullet import Bullet
            self.shoot_sound.play()
            return Bullet(self.rect.midleft, direction=-1, sprite_path=self.bullet_sprite)
        return None

    def draw(self, surface):
        if self.dying:
            fade = int((self.fade_timer / 10) * 255)
            faded_image = self.image.copy()
            for x in range(faded_image.get_width()):
                for y in range(faded_image.get_height()):
                    r, g, b, a = faded_image.get_at((x, y))
                    faded_image.set_at((x, y), (r // 2, g // 2, 255, min(a, fade)))
            surface.blit(faded_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.right < 0 and not self.dying

    def start_dying(self):
        self.dying = True

    def is_dead(self):
        return self.dying and self.fade_timer <= 0

    def kill(self):
        self.dying = True
        self.fade_timer = 0
