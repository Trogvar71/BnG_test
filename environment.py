import pygame
from towers import Tower

class Field:
    def __init__(self, level_number, screen):
        self.left = 5
        self.top = 5
        self.cellsize = 50
        filename = 'level' + str(level_number) + '.txt'
        self.typeDict = {'g': 'grass',
                        'r': 'road',
                        't': 'tower'}
        f = open(filename)
        level = [i.strip() for i in f.readlines()]
        f.close()
        level_size = [int(i) for i in level[0].split()]
        spawn_point = [int(i) for i in level[1].split()]
        self.spawn_point = spawn_point[0] * self.cellsize, spawn_point[1] * self.cellsize
        self.width = level_size[0]
        self.height = level_size[1]

        level_field = level[2:]
        field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i, j, type=self.typeDict[level_field[i][j]], screen=screen))
            field.append(row)

        self.field = field

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                self.field[i][j].cell_draw()

    def onclick(self, x, y):
        cell_x = x // self.cellsize
        cell_y = y // self.cellsize
        if cell_x < self.width and cell_y < self.height:
            self.field[cell_y][cell_x].onclick()


class Cell:
    def __init__(self, y, x, screen=None, size=50, type='grass', bordercolor='white'):
        self.colorDict = {'grass': 'green',
                          'road': 'brown',
                          'tower': 'grey'}
        self.x = x
        self.y = y
        self.x_pos = x * size
        self.y_pos = y * size
        self.size = size
        self.type = type
        self.color = self.colorDict[self.type]
        self.bordercolor = bordercolor
        self.sprite = None
        self.screen = screen

    def get_pos(self):
        return self.x, self.y

    def cell_draw(self):
        pygame.draw.rect(self.screen, self.bordercolor, (self.x_pos, self.y_pos, self.size, self.size), 2)
        pygame.draw.rect(self.screen, self.color, (self.x_pos + 2, self.y_pos + 2, self.size - 3, self.size - 3), 0)
        if self.sprite:
            self.sprite.rect.x = self.x_pos
            self.sprite.rect.y = self.y_pos

    def onclick(self):
        print('Клик в клетку', self.get_pos())
        if self.type == 'tower':
            self.color = 'red'
            tower = Tower()
            tower.spawn((self.x_pos, self.y_pos))
            global tower_list
            tower_list.append(tower)
            global tower_sprites
            tower_sprites.add(tower.sprite)