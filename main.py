import pygame
import sys
from enemies import Enemy
from towers import Tower
from projectiles import Projectile
# инициализация модуля и холста
pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hold\'em\'''All')
clock = pygame.time.Clock()
fps = 30

# определение глобальных для параметров и списков спрайтов и объектов
total_levels = 2
tower_list = []
enemy_list = []
projectile_list = []
tower_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()


# класс уровня. В нем содержится вся информация об уровне - а именно
# количество золота у игрока, количество жизней, карта, размеры элементов,
# точки спауна и точка, до которой нельзя доходить врагам, количество волн и так далее
class Level:
    def __init__(self, level_number):
        self.left = 200
        self.top = 75
        self.cellsize = 50
        filename = 'levels/level' + str(level_number) + '.txt'
        self.typeDict = {'g': 'grass',
                         'r': 'road',
                         't': 'tower',
                         'e': 'end'}
        f = open(filename)
        level = [i.strip() for i in f.readlines()]
        f.close()
        self.width = int(level[0].split(':')[1])
        self.height = int(level[1].split(':')[1])
        self.spawn_point = int(level[2].split(':')[1]) * self.cellsize, int(level[3].split(':')[1]) * self.cellsize
        self.end_point = int(level[4].split(':')[1]) * self.cellsize, int(level[5].split(':')[1]) * self.cellsize
        self.waves_number = int(level[6].split(':')[1])
        self.enemies_number = [int(i) for i in level[7].split(':')[1].split(',')]
        self.current_wave = 0
        self.current_enemies = 0
        self.lives = 10
        self.gold = 75

        level_field = level[10:]
        field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i, j, type=self.typeDict[level_field[i][j]]))
            field.append(row)

        self.field = field

    def new_wave(self):
        if self.current_wave < self.waves_number:
            self.current_wave += 1
            self.current_enemies = self.enemies_number[self.current_wave - 1]
        # else:
            # print('уровень завершен')

    def spawn_enemy(self):
        if self.current_enemies > 0:
            enemy = Enemy()
            enemy_list.append(enemy)
            enemy.spawn(self.spawn_point)
            enemy_sprites.add(enemy.sprite)
            self.current_enemies -= 1
        # else:
            # print('Враги закончились')

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                self.field[i][j].cell_draw()

    def onclick(self, x, y):
        cell_x = x // self.cellsize
        cell_y = y // self.cellsize
        if cell_x < self.width and cell_y < self.height:
            self.field[cell_y][cell_x].onclick(self)
        else:
            # print('boom')
            if len(tower_list) > 0:
                shoot(tower_list[0])


# класс клетки игрового поля. Хранит информацию о своем цвете, спрайте, типе
# обрабатывает событие клика, если это поле для башни
class Cell:
    def __init__(self, y, x, size=50, type='grass', bordercolor='white'):
        self.colorDict = {'grass': '#5da130',
                          'road': '#e8d6a0',
                          'tower': 'grey',
                          'end': 'blue'}
        self.x = x
        self.y = y
        self.x_pos = x * size
        self.y_pos = y * size
        self.size = size
        self.type = type
        self.color = self.colorDict[self.type]
        self.bordercolor = self.color
        self.sprite = None

    def get_pos(self):
        return self.x, self.y

    def cell_draw(self):
        pygame.draw.rect(screen, self.bordercolor, (self.x_pos, self.y_pos, self.size, self.size), 2)
        pygame.draw.rect(screen, self.color, (self.x_pos + 2, self.y_pos + 2, self.size - 3, self.size - 3), 0)
        if self.sprite:
            self.sprite.rect.x = self.x_pos
            self.sprite.rect.y = self.y_pos

    def onclick(self, level):
        # print('Клик в клетку', self.get_pos())
        if self.type == 'tower':
            tower = Tower()
            if level.gold >= tower.cost:
                self.color = 'red'
                level.gold -= tower.cost
                tower.spawn((self.x_pos, self.y_pos))
                global tower_list
                tower_list.append(tower)
                global tower_sprites
                tower_sprites.add(tower.sprite)
            else:
                pass  # здесь можно в дальнейшем добавить какую-то индикацию, что золота не хватает для постройки


# функция принимает в аргумент башню и инициирует выстрел (спаунит снаряд) из нее по ближайшему
# к концу маршрута врагу, если позволяет радиус.
# Выбор врага и проверка дистанции реализованы в методе choose_victim у башни
def shoot(tower):
    if len(enemy_list) > 0 and len(tower_list) > 0:
        victim = tower.choose_victim(enemy_list)
        projectile = Projectile()
        projectile_list.append(projectile)
        projectile.spawn((tower.x, tower.y))
        projectile_sprites.add(projectile.sprite)
        projectile.target = victim
        projectile.damage = tower.damage
    else:
        pass
        # print('не в кого стрелять')


# стартовое окно
def game_start():
    intro_text = ["                  Hold'em'All", "",
                  "      Игра в жанре Tower Defence.",
                  "Стройте башни на серых площадках у дороги",
                  "и не дайте врагам достичь лазурного портала!"]

    fon = pygame.transform.scale(pygame.image.load('image/start_back.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    intro_rect.top = text_coord + 100
    intro_rect.x = 300
    font = pygame.font.Font(None, 60)
    screen.blit(font.render('НАЧАТЬ', True, pygame.Color('red')), intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 500 > event.pos[0] > 300 and intro_rect.top + 30 > event.pos[1] > intro_rect.top:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


# окно поражения
def game_over():
    text = 'GAME OVER'
    screen.fill('black')
    font = pygame.font.Font(None, 60)
    screen.blit(font.render(text, True, pygame.Color('white')), (250, 100))
    text = 'НАЧАТЬ СНОВА'
    screen.blit(font.render(text, True, pygame.Color('red')), (220, 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 400 > event.pos[0] > 200 and 360 > event.pos[1] > 300:
                    game_restart()
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def game_restart():
    global tower_list
    tower_list = []
    global enemy_list
    enemy_list = []
    global projectile_list
    projectile_list = []
    global tower_sprites
    tower_sprites = pygame.sprite.Group()
    global enemy_sprites
    enemy_sprites = pygame.sprite.Group()
    global projectile_sprites
    projectile_sprites = pygame.sprite.Group()
    main(1)


def new_level(level_number):
    global tower_list
    tower_list = []
    global enemy_list
    enemy_list = []
    global projectile_list
    projectile_list = []
    global tower_sprites
    tower_sprites = pygame.sprite.Group()
    global enemy_sprites
    enemy_sprites = pygame.sprite.Group()
    global projectile_sprites
    projectile_sprites = pygame.sprite.Group()
    if level_number > total_levels:
        main(1)
    else:
        main(level_number)


# вывод текстовой информации в нижней части окна
def show_stats(gold, lives, current_wave):
    if current_wave == 0:
        current_wave = 'Приготовьтесь!'
    else:
        current_wave = str(current_wave)
    text = 'Золото:' + str(gold) + '    Жизней:' + str(lives) + '  Волна:' + current_wave
    font = pygame.font.Font(None, 40)
    screen.blit(font.render(text, True, pygame.Color('gold')), (30, 300))


# main. Здесь выполняется игровой цикл, отрисовка и все такое
def main(level_number):
    running = True
    screen.fill('black')
    level_number = level_number
    if level_number == 1:
        game_start()

    ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, 1000)
    NEW_WAVE_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(NEW_WAVE_EVENT, 10000)

    # сначала башни стреляли одновременно по общему событию, но позже я сделал им отдельную стрельбу у каждой
    # ибо их скорострельности отличаются. Но этот код для отладки еще пригодится
    # TOWERS_FIRE = pygame.USEREVENT + 3
    # pygame.time.set_timer(TOWERS_FIRE, 1000)

    level = Level(level_number)
    level.show()

    while running:
        screen.fill(pygame.Color("black"))
        level.show()
        enemy_sprites.draw(screen)
        show_stats(level.gold, level.lives, level.current_wave)

        for e in enemy_list:
            e.move()
            if e.hp == 0:
                enemy_sprites.remove(e.sprite)
                del enemy_list[enemy_list.index(e)]
                level.gold += 5
            if e.x >= level.end_point[0]:  # временное решение, но вообще лучше нарисовать в конце маршрута портал
                enemy_sprites.remove(e.sprite)  # и проверять столкновение со спрайтом портала, а не координаты
                del enemy_list[enemy_list.index(e)]
                level.lives -= 1
                if level.lives == 0:
                    game_over()
                # print('Осталось', level.lives, 'жизней')

        tower_sprites.draw(screen)

        projectile_sprites.draw(screen)
        for proj in projectile_list:
            if enemy_list:
                proj.move(enemy_list)
                if pygame.sprite.spritecollideany(proj.sprite, enemy_sprites):
                    enemy_list[proj.target].get_damage(proj.damage)
                    projectile_sprites.remove(proj.sprite)
                    projectile_list.remove(proj)
            else:
                projectile_sprites.remove(proj.sprite)
                projectile_list.remove(proj)
        for tower in tower_list:
            if tower.ready:
                shoot(tower)
                tower.ready = False
                tower.countdown = 15
            else:
                tower.countdown -= 1
                if tower.countdown == 0:
                    tower.ready = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                level.onclick(event.pos[0], event.pos[1])
            if event.type == NEW_WAVE_EVENT and level.current_wave <= level.waves_number:
                level.new_wave()
            if event.type == ENEMY_SPAWN_EVENT:
                level.spawn_enemy()
            # if event.type == TOWERS_FIRE:
            #     for tower in tower_list:
            #         shoot(tower)

        if level.current_wave == level.waves_number and level.current_enemies == 0 and len(enemy_list) == 0:
            # print('Уровень пройден')
            level_number += 1
            new_level(level_number)

        # обновление экрана
        clock.tick(fps)
        pygame.display.flip()

    terminate()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main(1)
