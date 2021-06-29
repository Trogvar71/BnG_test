import pygame


class EnemySprite(pygame.sprite.Sprite):
    image = pygame.image.load('image/demon.png')
    image.set_colorkey(-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = EnemySprite.image
        self.rect = self.image.get_rect()
        self.speed = 1

    def update(self):
        self.rect = self.rect.move(self.speed, 0)


# класс врага с описанием его параметров.
# При дальнейшей разработке можно отнаследовать от него другие виды противников
class Enemy():
    def __init__(self):
        self.sprite = EnemySprite()
        self.speed = self.sprite.speed
        self.x = -100
        self.y = -100
        self.hp = 5

    def spawn(self, spawn_point):
        self.sprite.rect.x = spawn_point[0]
        self.sprite.rect.y = spawn_point[1]
        self.x = spawn_point[0]
        self.y = spawn_point[1]

    def move(self):
        self.x += self.speed
        self.sprite.update()

    def get_damage(self, damage):
        print('получил')
        self.hp -= damage