# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 2: Pacman
# This File: game_functions.py contains misc. functions used during runtime

from random import randint
import pygame as pg
from settings import Settings

settings = Settings()


def check_for_game_over(game):
    all_points_eaten = True
    for value in game.maze.grid_points.values():
        if value.collected is False:
            all_points_eaten = False
    if all_points_eaten is True:
        game.game_over_screen()
    ghosts = [game.blinky, game.pinky, game.inkey, game.clyde]
    for ghost in ghosts:
        if game.pacman.pt == ghost.pt and ghost.state == 0:
            death = pg.mixer.Sound('assets/sounds/death.wav')
            pg.mixer.Sound.play(death)
            game.game_over_screen()
            # GAME OVER


def check_for_eat_ghost(game, scoreboard):
    ghosts = [game.blinky, game.pinky, game.inkey, game.clyde]
    num_in_state = 0
    for ghost in ghosts:
        if ghost.state == 3:
            num_in_state += 1
    for ghost in ghosts:
        if game.pacman.pt == ghost.pt and (ghost.state == 1 or ghost.state == 2):
            ghost.state = 3
            points = 200 * num_in_state + 200 * (num_in_state + 1)
            scoreboard.add_points(points, ghost.pt.pt)


def tunnel(maze, pacman):
    if pacman.pt.index == 136 and pacman.angle == 0:
        pacman.pt = maze.grid_points[152]
        pacman.pt_next = maze.grid_points[151]
        pacman.pt_prev = maze.grid_points[136]
        pacman.rect.centerx, pacman.rect.centery = pacman.pt.pt
        pacman.velocity = 1
    if pacman.pt.index == 152 and pacman.angle == 180:
        pacman.pt = maze.grid_points[136]
        pacman.pt_next = maze.grid_points[137]
        pacman.pt_prev = maze.grid_points[152]
        pacman.rect.centerx, pacman.rect.centery = pacman.pt.pt
        pacman.velocity = 1


def spawn_fruit(maze):
    if maze.grid_points[178].collected is True:
        chance = randint(0, 5000)
        if chance == 1:
            maze.grid_points[178].collected = False
            maze.grid_points[178].type = 2


def portal(maze, pacman):
    if pacman.orange_portal and pacman.blue_portal:
        if pacman.pt == pacman.orange_portal:
            pacman.pt = pacman.blue_portal
            pacman.pt_next = maze.grid_points[pacman.pt.adjacency_list[0]]
            pacman.velocity = 1
            pacman.rect.centerx, pacman.rect.centery = pacman.pt.pt


def read_high_score():
    high_scores = []
    with open('scores.txt', 'r') as file:
        for line in file:
            current = line[:-1]
            high_scores.append(int(current))
    return high_scores


def write_high_score(high_scores, current):
    if len(high_scores) < 5:
        high_scores.append(current)
        high_scores.sort(reverse=True)
    else:
        is_a_high_score = False
        for score in high_scores:
            if current > score:
                is_a_high_score = True
        if is_a_high_score:
            high_scores.sort(reverse=True)
            high_scores.pop()
            high_scores.append(current)
            high_scores.sort(reverse=True)
    with open('scores.txt', 'w') as file:
        for score in high_scores:
            file.write('%s\n' % str(score))
