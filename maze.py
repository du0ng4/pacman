# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 2: Pacman
# This File: maze.py contains class and methods relating to the maze

import pygame as pg
import copy
from settings import Settings
settings = Settings()


class Maze:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load('assets/images/maze.png')
        self.image = pg.transform.rotozoom(self.image, 0, settings.screen_width / 1510)
        self.rect = self.image.get_rect()
        self.grid = self.create_grid()
        self.grid_points = {}
        self.create_grid_points()
        # special cases
        self.grid_points[0].type = 1
        self.grid_points[16].type = 1
        self.grid_points[306].type = 1
        self.grid_points[322].type = 1
        self.grid_points[127].collected = True
        self.grid_points[143].collected = True
        self.grid_points[144].collected = True
        self.grid_points[145].collected = True

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        for value in self.grid_points.values():
            value.draw()

    @staticmethod
    def create_grid():
        return [
            [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16],        # row 0
            [0, 3, 7, 9, 13, 16],                                           # row 1
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],     # row 2
            [0, 3, 5, 11, 13, 16],                                          # row 3
            [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16],               # row 4
            [3, 7, 9, 13],                                                  # row 5
            [3, 5, 6, 7, 8, 9, 10, 11, 13],                                 # row 6
            [3, 5, 8, 11, 13],                                              # row 7
            [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15, 16],            # row 8
            [3, 5, 11, 13],                                                 # row 9
            [3, 5, 6, 7, 8, 9, 10, 11, 13],                                 # row 10
            [3, 5, 11, 13],                                                 # row 11
            [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16],        # row 12
            [0, 3, 7, 9, 13, 16],                                           # row 13
            [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16],            # row 14
            [1, 3, 5, 11, 13, 15],                                          # row 15
            [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16],               # row 16
            [0, 7, 9, 16],                                                  # row 17
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]      # row 18
        ]

    def create_grid_points(self):
        positions = {0: 60, 1: 97, 2: 134, 3: 171, 4: 209, 5: 249, 6: 286, 7: 323, 8: 360, 9: 397, 10: 434, 11: 471,
                     12: 511, 13: 549, 14: 587, 15: 624, 16: 665, 17: 702, 18: 739}
        for y in range(len(self.grid)):
            for x in self.grid[y]:
                index = x + (y * 17)

                # check for adjacent
                adjacent_to = []
                if y != 0:  # up
                    if x in self.grid[y-1]:
                        adjacent_to.append(index - 17)
                if y != 18:  # down
                    if x in self.grid[y+1]:
                        adjacent_to.append(index + 17)
                if x-1 in self.grid[y]:  # left
                    adjacent_to.append(index - 1)
                if x+1 in self.grid[y]:  # right
                    adjacent_to.append(index + 1)

                self.grid_points[index] = GridPoint(screen=self.screen, index=index, pt=(positions[x], positions[y]),
                                                    adjacency_list=adjacent_to)


class GridPoint:
    def __init__(self, screen, index, pt, adjacency_list):
        self.index = index
        self.pt = pt
        self.adjacency_list = adjacency_list
        self.screen = screen
        self.collected = False
        self.type = 0   # 0 is a normal point, 1 is a power pill, 2 is a fruit, 3 is orange portal, 4 is blue portal
        self.fruit_img = pg.image.load('assets/images/fruit.png')
        self.fruit_img = pg.transform.rotozoom(self.fruit_img, 0, 0.4)
        self.orange_img = pg.image.load('assets/images/orange_portal.png')
        self.orange_img = pg.transform.rotozoom(self.orange_img, 0, 0.5)
        self.blue_img = pg.image.load('assets/images/blue_portal.png')
        self.blue_img = pg.transform.rotozoom(self.blue_img, 0, 0.5)

    # used to make deep copy of grid points dictionary
    # adapted from https://stackoverflow.com/a/57225764
    def copy(self):
        copy_obj = GridPoint(self.screen, self.index, self.pt, self.adjacency_list)
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copy_obj.__dict__[name] = attr.copy()
            else:
                copy_obj.__dict__[name] = copy.deepcopy(attr)
            return copy_obj

    def update(self):
        self.draw()

    def draw(self):
        if self.type == 0 and self.collected is False:
            pg.draw.circle(surface=self.screen, color=(255, 0, 0), center=self.pt, radius=2)
        if self.type == 1 and self.collected is False:
            pg.draw.circle(surface=self.screen, color=(255, 0, 0), center=self.pt, radius=8)
        if self.type == 2 and self.collected is False:
            rect = self.fruit_img.get_rect()
            rect.centerx, rect.centery = self.pt
            self.screen.blit(self.fruit_img, rect)
        if self.type == 3:
            rect = self.orange_img.get_rect()
            rect.centerx, rect.centery = self.pt
            self.screen.blit(self.orange_img, rect)
        if self.type == 4:
            rect = self.blue_img.get_rect()
            rect.centerx, rect.centery = self.pt
            self.screen.blit(self.blue_img, rect)
