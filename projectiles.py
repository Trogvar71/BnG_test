import pygame, math


class ProjectileSprite(pygame.sprite.Sprite):
    image = pygame.image.load('image/ball.png')
    image.set_colorkey(-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ProjectileSprite.image
        self.rect = self.image.get_rect()
        self.speed = 15

    def update(self, speedx, speedy):
        self.rect = self.rect.move(speedx, speedy)


# класс снаряда, котоырй выпускает башня
# При дальнейшей разработке можно отнаследовать от него другие виды снарядов
class Projectile():
    def __init__(self):
        self.sprite = ProjectileSprite()
        self.x = -100
        self.y = -100
        self.target = None
        self.speedx = 0
        self.speedy = 0
        self.damage = 1

    def spawn(self, spawn_point):
        self.sprite.rect.x = spawn_point[0] + 15
        self.sprite.rect.y = spawn_point[1] + 15
        self.x = spawn_point[0] + 15
        self.y = spawn_point[1] + 15

    def move(self, enemy_list):
        a = self.x - enemy_list[self.target].x - 15
        b = self.y - enemy_list[self.target].y - 15
        c = (a ** 2 + b ** 2) ** 0.5
        self.speedx = self.sprite.speed * (- a / c)
        self.speedy = self.sprite.speed * (- b / c)

        self.x += self.speedx
        self.y += self.speedy
        self.sprite.update(self.speedx, self.speedy)