import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Player:
    def __init__(self):
        self.image = pygame.image.load('./asset/nave.png').convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(100, WIN_HEIGHT // 2))
        self.speed = 5
        self.shoot_cooldown = 0
        self.bullet_sprite = './asset/bulletplayer.png'
        self.health = 5
        self.max_health = 5
        self.invulnerable_timer = 0
        self.flash_duration = 30  # frames invulnerável
        self.visible = True
        self.flash_tick = 0

        self.shoot_sound = pygame.mixer.Sound('./asset/shoot.wav')

    def handle_input(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIN_WIDTH, WIN_HEIGHT))

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 15
            from code.Bullet import Bullet
            self.shoot_sound.play()
            return Bullet(self.rect.midright, direction=1, sprite_path=self.bullet_sprite)
        return None

    def take_damage(self, amount):
        if self.invulnerable_timer == 0:
            self.health -= amount
            self.invulnerable_timer = self.flash_duration
            print(f"Vida restante: {self.health}")

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            self.flash_tick += 1
            # alterna visibilidade
            self.visible = (self.flash_tick % 6 < 3)
            # muda a cor da nave para vermelha temporariamente
            if self.visible:
                red_image = self.original_image.copy()
                red_image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = red_image
            else:
                self.image = pygame.Surface((0, 0), pygame.SRCALPHA)  # invisível
        else:
            self.visible = True
            self.image = self.original_image
            self.flash_tick = 0

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

    def draw_health_bar(self, surface):
        bar_width = 100
        bar_height = 10
        x = 20
        y = 20
        fill = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, fill, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)
