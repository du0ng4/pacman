# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 2: Pacman
# This File: game.py contains classes and methods relating to characters (pacman and ghosts)

import pygame as pg
import numpy
import math
import SpriteSheet
from timer import Timer
from settings import Settings

settings = Settings()


class Character:
    def __init__(self, game, image, pt, pt_next, pt_prev, velocity):
        self.game = game
        self.screen = game.screen
        self.angle = 0
        self.image = image
        self.pt, self.pt_next, self.pt_prev = pt, pt_next, pt_prev
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.pt
        self.velocity = velocity
        self.at_point = False
        self.turning = False
        self.dead = False

    def at_destination(self):
        delta = tuple(numpy.subtract((self.rect.centerx, self.rect.centery), self.pt_next.pt))
        if delta == (0, 0):
            self.at_point = True
            self.pt_prev = self.pt
            self.pt = self.pt_next
            self.rect.centerx, self.rect.centery = self.pt.pt

            # automatically chooses next point based on direction to keep going
            if self.angle == 0 and self.pt.index - 1 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index - 1]
            elif self.angle == 180 and self.pt.index + 1 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index + 1]
            elif self.angle == 90 and self.pt.index + 17 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index + 17]
            elif self.angle == 270 and self.pt.index - 17 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index - 17]
            else:
                if type(self) is Pacman:
                    self.velocity = 0
        else:
            self.at_point = False

    def update_angle(self):
        # 0 left, 90 down, 180 right, 270 up
        if self.pt_next.index == self.pt.index + 1:
            self.angle = 180
        if self.pt_next.index == self.pt.index - 1:
            self.angle = 0
        if self.pt_next.index == self.pt.index + 17:
            self.angle = 90
        if self.pt_next.index == self.pt.index - 17:
            self.angle = 270

    def movement(self):
        if self.angle == 0:
            self.rect.centerx -= self.velocity
        if self.angle == 90:
            self.rect.centery += self.velocity
        if self.angle == 180:
            self.rect.centerx += self.velocity
        if self.angle == 270:
            self.rect.centery -= self.velocity


class Pacman(Character):
    def __init__(self, game, pt, pt_next, pt_prev, velocity):
        self.timer = self.create_timers()
        self.image = self.timer.imagerect()
        self.image = pg.transform.rotozoom(self.image, 0, 0.45)
        self.original_image = self.image
        self.blue_portal = None
        self.orange_portal = None
        super().__init__(game=game, image=self.image, pt=pt, pt_next=pt_next, pt_prev=pt_prev, velocity=velocity)

    def update(self, keys, blinky, pinky, inkey, clyde, scoreboard):
        self.draw()
        Character.at_destination(self)
        self.eat_pills_and_points(blinky, pinky, inkey, clyde, scoreboard)
        self.create_portal(keys)
        self.turn(keys)
        self.reverse(keys)
        Character.update_angle(self)
        Character.movement(self)

    def create_portal(self, keys):
        # if self.pt_next.collected is True:
        if keys[pg.K_r]:
            if self.orange_portal:
                self.orange_portal.type = 0
            self.pt_next.type = 3
            self.orange_portal = self.pt_next
        if keys[pg.K_v]:
            if self.blue_portal:
                self.blue_portal.type = 0
            self.pt_prev.type = 4
            self.blue_portal = self.pt_prev

    def turn(self, keys):
        # key presses
        if self.at_point is True:
            self.turning = True
            if keys[pg.K_LEFT] and self.pt.index - 1 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index - 1]
                self.velocity = 1
            if keys[pg.K_RIGHT] and self.pt.index + 1 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index + 1]
                self.velocity = 1
            if keys[pg.K_UP] and self.pt.index - 17 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index - 17]
                self.velocity = 1
            if keys[pg.K_DOWN] and self.pt.index + 17 in self.pt.adjacency_list:
                self.pt_next = self.game.maze.grid_points[self.pt.index + 17]
                self.velocity = 1
            self.turning = False

    def reverse(self, keys):
        if ((self.angle == 0 and keys[pg.K_RIGHT]) or
                (self.angle == 90 and keys[pg.K_UP]) or
                (self.angle == 180 and keys[pg.K_LEFT]) or
                (self.angle == 270 and keys[pg.K_DOWN]) and
                self.turning is False):
            temp = self.pt_prev
            self.pt_prev = self.pt_next
            self.pt_next = temp

    def draw(self):
        self.image = self.timer.imagerect()
        self.image = pg.transform.rotozoom(self.image, self.angle, 0.45)
        self.screen.blit(self.image, self.rect)

    def eat_pills_and_points(self, blinky, pinky, inkey, clyde, scoreboard):
        if self.at_point is True and self.pt.collected is False:
            if self.pt.type == 0:
                scoreboard.add_points(10)
            elif self.pt.type == 1:
                scoreboard.add_points(50, self.pt.pt)
                if blinky.state != 3:
                    blinky.state = 1
                    blinky.rect.centerx, blinky.rect.centery = blinky.pt.pt
                    blinky.blue_time = pg.time.get_ticks()
                if pinky.state != 3:
                    pinky.state = 1
                    pinky.rect.centerx, pinky.rect.centery = pinky.pt.pt
                    pinky.blue_time = pg.time.get_ticks()
                if inkey.state != 3:
                    inkey.state = 1
                    inkey.rect.centerx, inkey.rect.centery = inkey.pt.pt
                    inkey.blue_time = pg.time.get_ticks()
                if clyde.state != 3:
                    clyde.state = 1
                    clyde.rect.centerx, clyde.rect.centery = clyde.pt.pt
                    clyde.blue_time = pg.time.get_ticks()
            elif self.pt.type == 2:
                scoreboard.add_points(100, self.pt.pt)

            self.pt.collected = True

    @staticmethod
    def create_timers():
        ss = SpriteSheet.Spritesheet('assets/images/pacman.png')
        images = []
        for i in range(2):
            images.append(ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
        return Timer(frames=images, wait=200)


class Ghost(Character):
    def __init__(self, game, pt, pt_next, pt_prev, maze, name, velocity):
        self.maze = maze
        self.name = name
        self.state = 0  # 0 is normal, 1 is blue/running, 2 is expiring blue, 3 is eaten and returning to spawn
        self.timers = self.create_timers()
        self.timer = self.timers['0']
        self.blue_time = None
        self.rotation = ['blinky', 'pinky', 'inkey', 'clyde'].index(name)
        super().__init__(game=game, image=self.timer.imagerect(),
                         pt=pt, pt_next=pt_next, pt_prev=pt_prev, velocity=velocity)

    def update(self, maze, pacman):
        self.draw()
        Character.at_destination(self)
        self.running()
        targets = [maze.grid_points[0], maze.grid_points[16],
                   maze.grid_points[322], maze.grid_points[306]]
        if self.state == 0:
            if self.distance(pacman, self) > 200:
                if self.name == 'blinky':
                    self.calculate_shortest_path(pacman.pt)
                if self.name == 'pinky':
                    if self.pt == targets[self.rotation]:
                        self.rotation = (self.rotation + 3) % 4
                        self.rect.centerx, self.rect.centery = self.pt.pt
                    self.calculate_shortest_path(targets[self.rotation])
                if self.name == 'inkey' or self.name == 'clyde':
                    if self.pt == targets[self.rotation]:
                        self.rotation = (self.rotation + 1) % 4
                        self.rect.centerx, self.rect.centery = self.pt.pt
                    self.calculate_shortest_path(targets[self.rotation])
            else:
                self.calculate_shortest_path(pacman.pt)
        elif self.state == 1 or self.state == 2:
            if self.distance(pacman, self) > 200:
                self.calculate_shortest_path(targets[self.rotation])
            else:
                index = self.find_farthest(pacman, maze)
                self.calculate_shortest_path(targets[index])
        elif self.state == 3:
            self.calculate_shortest_path(maze.grid_points[144])
            if self.pt == maze.grid_points[144]:
                self.state = 0
                self.rect.centerx, self.rect.centery = self.pt.pt
        Character.update_angle(self)
        Character.movement(self)

    def draw(self):
        if self.state == 0:
            self.timer = self.timers[str(self.angle)]
        elif self.state == 1:
            self.timer = self.timers['blue']
        elif self.state == 2:
            self.timer = self.timers['expire']
        elif self.state == 3:
            self.timer = self.timers['eyes_' + str(self.angle)]

        if self.state != 3:
            image = self.timer.imagerect()
        else:
            image = self.timer

        image = pg.transform.rotozoom(image, 0, 0.5)
        rect = image.get_rect()
        rect.centerx, rect.centery = self.rect.centerx, self.rect.centery
        self.screen.blit(image, rect)

    def calculate_shortest_path(self, target):
        graph = self.maze.grid_points
        start = self.pt.index
        goal = target.index

        shortest_path = {}
        predecessor = {}
        unseen_nodes = graph.copy()
        infinity = float("inf")
        path = []

        for node in unseen_nodes:
            shortest_path[node] = infinity
        shortest_path[start] = 0

        while unseen_nodes:
            min_node = None
            for node in unseen_nodes:
                if min_node is None:
                    min_node = node
                elif shortest_path[node] < shortest_path[min_node]:
                    min_node = node

            for child in graph[min_node].adjacency_list:
                if 1 + shortest_path[min_node] < shortest_path[child]:
                    shortest_path[child] = shortest_path[min_node] + 1
                    predecessor[child] = min_node
            unseen_nodes.pop(min_node)

        current = goal
        while current != start:
            path.insert(0, current)
            current = predecessor[current]

        if self.pt != target and self.at_point:
            self.pt_next = self.maze.grid_points[path[0]]

    @staticmethod
    def distance(pacman, target):
        a, b = pacman.pt.pt
        if type(target) is Ghost:
            dx, dy = a - target.rect.centerx, b - target.rect.centery
        else:
            x, y = target.pt
            dx, dy = a - x, b - y

        return math.sqrt(dx ** 2 + dy ** 2)

    def find_farthest(self, pacman, maze):
        points = [maze.grid_points[0], maze.grid_points[16],
                  maze.grid_points[322], maze.grid_points[306]]
        distances = []
        for i in points:
            distances.append(self.distance(pacman, i))
        return distances.index(max(distances))

    def running(self):
        if self.state == 1 and (self.blue_time + 7000) < pg.time.get_ticks() < (self.blue_time + 10000):
            self.state = 2
            self.rect.centerx, self.rect.centery = self.pt.pt
        if self.state == 2 and pg.time.get_ticks() > (self.blue_time + 10000):
            self.state = 0
            self.rect.centerx, self.rect.centery = self.pt.pt

    def create_timers(self):
        ss = []
        directions = ['270', '90', '0', '180']
        for direction in directions:
            ss.append(SpriteSheet.Spritesheet('assets/images/' + str(self.name) + '_' + direction + '.png'))
        ss = {k: v for (k, v) in zip(directions, ss)}
        timers = {}
        for direction in directions:
            temp = []
            for j in range(2):
                temp.append(ss[direction].image_at(rectangle=(0, j * 64, 64, 64), colorkey=(0, 0, 0)))
            timers[direction] = Timer(frames=temp, wait=700)
        blue_ss = SpriteSheet.Spritesheet('assets/images/blue.png')
        blue_img = [blue_ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)) for i in range(2)]
        timers['blue'] = Timer(frames=blue_img, wait=700)
        expire_ss = SpriteSheet.Spritesheet('assets/images/expire.png')
        expire_img = [expire_ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)) for i in range(4)]
        timers['expire'] = Timer(frames=expire_img, wait=400)
        eyes_ss = SpriteSheet.Spritesheet('assets/images/eyes.png')
        eyes_img = [eyes_ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)) for i in range(4)]
        for i, direction in enumerate(directions):
            string = 'eyes_' + str(direction)
            timers[string] = eyes_img[i]

        return timers
