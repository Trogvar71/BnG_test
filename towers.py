import pygame


class TowerSprite(pygame.sprite.Sprite):
    image = pygame.image.load('image/tower.png')
    image.set_colorkey(-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = TowerSprite.image
        self.rect = self.image.get_rect()

    def update(self):
        pass


# класс башни с описанием параметров
# При дальнейшей разработке можно отнаследовать от него другие виды башен
class Tower():
    def __init__(self):
        self.sprite = TowerSprite()
        self.x = -100
        self.y = -100
        self.range = 1000
        self.damage = 1
        self.cost = 50
        self.countdown = 15
        self.ready = True

    def spawn(self, spawn_point):
        self.sprite.rect.x = spawn_point[0]
        self.sprite.rect.y = spawn_point[1]
        self.x = spawn_point[0]
        self.y = spawn_point[1]

    def choose_victim(self, enemy_list):
        for i in range(len(enemy_list)):
            if ((self.x - enemy_list[i].x) ** 2 + (self.y - enemy_list[i].y) ** 2) ** 0.5 <= self.range:
                return i
        return None