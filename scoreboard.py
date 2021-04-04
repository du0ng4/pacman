# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 2: Pacman
# This File: scoreboard.py contains class and methods for the scoreboard

import pygame as pg
from settings import Settings

settings = Settings()


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.cache = []
        self.time = []

    def add_points(self, num, location=None):
        self.score += num
        if location:
            font = pg.font.SysFont('Ariel', 30, False)
            score = font.render(str(num), True, (0, 255, 0))
            score_rect = score.get_rect()
            score_rect.centerx, score_rect.centery = location
            self.cache.append([score, score_rect])
            self.time.append(0)

    def show_score(self, screen):
        font = pg.font.SysFont('Ariel', 40, False)
        score = font.render('Points: ' + str(self.score), True, (0, 255, 0))
        score_rect = score.get_rect()
        score_rect.right, score_rect.centery = settings.screen_width - 16, settings.screen_height - 64
        screen.blit(score, score_rect)

    def persist(self, screen):
        for i in self.cache:
            screen.blit(i[0], i[1])
            index = self.cache.index(i)
            self.time[index] += 1
        for i in range(len(self.time)):
            if self.time[i] > 50:
                self.time.pop(i)
                self.cache.pop(i)
