import pygame
from code.Const import WIN_WIDTH

class Bullet:
    def __init__(self, position, direction=1, sprite_path='./asset/bulletenemy.png'):
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 8))
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=position)
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.right < 0 or self.rect.left > WIN_WIDTH
