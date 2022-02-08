"""
#TODO
-Expansion vertical
-mas tipos de bloques
-volar?
"""

import pygame
import random
from helper import *

pygame.init()


class Main:
    def __init__(self):
        self.player = Player()
        self.world = World()

    def loop(self):
        self.player.draw()
        self.player.move()
        self.world.generate_world()
        self.world.draw()
        self.world.get_hover()
        self.world.expand_world()


class Player:
    def __init__(self):
        self.raw_img = pygame.image.load('data/img/player.png').convert_alpha()
        self.img_r = pygame.transform.scale(self.raw_img, (34, 72))
        self.img_l = pygame.transform.flip(self.img_r, True, False)
        self.img_idx = 0
        self.imgs = [self.img_r, self.img_l]

        self.pos = [400, 100]
        self.speed = [0, 0]
        self.can_jump = False
        self.can_right = False
        self.can_left = False

    def draw(self):
        screen.blit(self.imgs[self.img_idx], self.pos)

    def move(self):
        self.pos = sum_array(self.pos, self.speed)
        coor_y = p_board_y(self.pos)

        # gravity
        offset = main.world.chunk * 16

        if main.world.world[coor_y[0] + offset][coor_y[1] - 1] == 1:
            self.speed[1] = 0
            self.can_jump = True
        else:
            self.speed[1] += 0.5
            self.can_jump = False

        # if block above, can't jump
        if main.world.world[coor_y[0] + offset][coor_y[1] + 1] == 1:
            self.can_jump = False
            if self.pos[1] < 450:
                self.speed[1] += 0.5

        # lateral collisions body and head
        coor_x = p_board_x(self.pos, self.img_idx)  # img_idx 0 right, 1 left

        if main.world.world[coor_x[0] + 1 + offset][coor_x[1]] == 0:  # if body free
            self.can_right = True
        else:
            if self.img_idx == 0:
                self.can_right = False
                self.speed[0] = 0
        if main.world.world[coor_x[0] - 1 + offset][coor_x[1]] == 0:
            self.can_left = True
        else:
            if self.img_idx == 1:
                self.can_left = False
                self.speed[0] = 0

        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > 755:
            self.pos[0] = 755


class World:
    def __init__(self):
        self.world = self.generate_world()
        self.blocks_pos = []
        self.blocks = []
        self.render_blocks()
        self.hover_img = pygame.image.load('data/img/hover.png')
        self.visited = [0]
        self.chunk = 0

    def generate_world(self):
        world = []

        for i in range(16):
            world.append(self.generate_column())

        return world

    def generate_column(self):
        column = []

        floor = random.choices(([1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]), weights=[8, 4, 2, 1])
        # floor = [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]
        column.append(floor[0][0])
        column.append(floor[0][1])
        column.append(floor[0][2])
        column.append(floor[0][3])

        for i in range(97):
            column.append(0)

        return column

    def expand_world(self):
        # right
        if p_board_y(main.player.pos)[0] == 15 and main.player.img_idx == 0:
            self.chunk += 1
            new = False if self.chunk in self.visited else True

            if self.chunk not in self.visited:
                self.visited.append(self.chunk)

            if new:
                for i in range(16):
                    self.world.append(self.generate_column())

            main.player.pos[0] -= 750
            for i in self.blocks_pos:
                i[0] -= 800

            self.re_render(new=new)

        # left
        if p_board_y(main.player.pos)[0] == 0 and main.player.img_idx == 1:
            self.chunk -= 1
            new = False if self.chunk in self.visited else True

            if self.chunk not in self.visited:
                self.visited.append(self.chunk)

            if new:
                for i in range(16):
                    self.world.append(self.generate_column())

            main.player.pos[0] += 750
            for i in self.blocks_pos:
                i[0] += 800

            self.re_render(new=new)

    def re_render(self, new):
        idx = [-1, -1]

        chunk_index = self.visited.index(self.chunk)

        rng = [16 * chunk_index, 16 * (chunk_index + 1)]

        for i in range(rng[0], rng[1]):
            idx[0] += 1
            idx[1] = -1
            for tile in self.world[i]:

                if idx[1] == 99:
                    idx[1] = -1
                idx[1] += 1

                if tile == 1:
                    self.blocks.append(Block())
                    self.blocks_pos.append(idx_to_pos(idx))

    def render_blocks(self):
        # appends Block()s and their positions
        # expensive, only run at init

        idx = [-1, -1]

        for col in self.world:
            idx[0] += 1
            idx[1] = -1
            for tile in col:

                if idx[1] == 99:
                    idx[1] = -1
                idx[1] += 1

                if tile == 1:
                    self.blocks.append(Block())
                    self.blocks_pos.append(idx_to_pos(idx))

    def draw(self):
        for i in self.blocks:
            i.draw()

    def get_hover(self):
        mouse = pygame.mouse.get_pos()
        tile = coor_to_pos(mouse)

        screen.blit(self.hover_img, (tile[0] * 50, tile[1] * 50))

        return tile[0] * 50, tile[1] * 50

    def block_click(self, coor):
        offset = -16  # last block chunk generated
        coor = list(coor)  # convert to list because it is tuple by default

        idx = coor_to_pos(coor)

        if self.world[idx[0] + offset][11 - idx[1]] == 0:
            self.world[idx[0] + offset][11 - idx[1]] = 1
            self.blocks_pos.append(coor)
            self.blocks.append(Block())
        elif self.world[idx[0] + offset][11 - idx[1]] == 1:
            self.world[idx[0] + offset][11 - idx[1]] = 0
            try:
                pos_to_pop = self.blocks_pos.index(coor)
                self.blocks_pos.pop(pos_to_pop)
                self.blocks.pop()
            except:
                self.world[idx[0] + offset][11 - idx[1]] = 1
                self.blocks_pos.append(coor)
                self.blocks.append(Block())


class Block:
    def __init__(self):
        self.img = pygame.image.load('data/img/block.png').convert()
        self.img = pygame.transform.scale(self.img, (50, 50))

    def draw(self):
        for i in range(len(main.world.blocks_pos)):
            pos = main.world.blocks_pos[i]
            if 0 <= pos[0] < 800:
                screen.blit(self.img, pos)


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main.player.can_right:
                    main.player.img_idx = 0
                    main.player.speed[0] = 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main.player.can_left:
                    main.player.img_idx = 1
                    main.player.speed[0] = -5
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                if main.player.can_jump:
                    main.player.speed[1] = -10
            if event.key == pygame.K_z:  # for developement purposes
                print_world(main.world.world)
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_a) and main.player.speed[0] > 0:
                main.player.speed[0] = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main.player.speed[0] < 0:
                main.player.speed[0] = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            main.world.block_click(main.world.get_hover())


screen = pygame.display.set_mode((800, 600))
main = Main()
clock = pygame.time.Clock()
main.world.generate_column()

while True:
    events()
    screen.fill((40, 150, 40))
    main.loop()
    clock.tick(60)
    pygame.display.update()
