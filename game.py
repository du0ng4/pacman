# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 2: Pacman
# This File: game.py main driver for program

import sys
from pygame.locals import *
from maze import *
from characters import *
from game_functions import *
from scoreboard import Scoreboard

from settings import Settings
settings = Settings()


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
        pg.display.set_caption("Pacman")
        self.clock = pg.time.Clock()
        self.running = False
        self.scoreboard = None
        self.maze = None
        self.pacman = None
        self.blinky = None
        self.pinky = None
        self.inkey = None
        self.clyde = None
        self.high_scores = read_high_score()

    def run_game(self):
        self.running = True
        self.scoreboard = Scoreboard()
        self.maze = Maze(self.screen)
        start_point = self.maze.grid_points[246]
        next_point = self.maze.grid_points[245]
        prev_point = self.maze.grid_points[247]
        self.pacman = Pacman(self, start_point, next_point, prev_point, 1)
        start_point = self.maze.grid_points[110]
        next_point = self.maze.grid_points[109]
        prev_point = self.maze.grid_points[111]
        self.blinky = Ghost(self, start_point, next_point, prev_point, self.maze, 'blinky', 1)
        start_point = self.maze.grid_points[144]
        next_point = self.maze.grid_points[127]
        prev_point = self.maze.grid_points[145]
        self.pinky = Ghost(self, start_point, next_point, prev_point, self.maze, 'pinky', 1)
        start_point = self.maze.grid_points[143]
        next_point = self.maze.grid_points[144]
        prev_point = self.maze.grid_points[143]
        self.inkey = Ghost(self, start_point, next_point, prev_point, self.maze, 'inkey', 1)
        start_point = self.maze.grid_points[145]
        next_point = self.maze.grid_points[144]
        prev_point = self.maze.grid_points[145]
        self.clyde = Ghost(self, start_point, next_point, prev_point, self.maze, 'clyde', 1)
        start_sound = pg.mixer.Sound('assets/sounds/start.wav')
        pg.mixer.Sound.play(start_sound)
        pg.event.wait()
        pg.mixer.music.load('assets/sounds/waka.mp3')
        pg.mixer.music.play(-1)

        # game loop
        while self.running:
            keys = pg.key.get_pressed()  # gets key presses
            self.screen.fill(settings.bg_color)
            self.clock.tick(144)

            self.maze.update()
            self.scoreboard.show_score(self.screen)
            self.pacman.update(keys, self.blinky, self.pinky, self.inkey, self.clyde, self.scoreboard)
            self.blinky.update(self.maze, self.pacman)
            self.pinky.update(self.maze, self.pacman)
            self.inkey.update(self.maze, self.pacman)
            self.clyde.update(self.maze, self.pacman)

            self.scoreboard.persist(self.screen)
            tunnel(self.maze, self.pacman)
            portal(self.maze, self.pacman)
            check_for_game_over(self)
            check_for_eat_ghost(self, self.scoreboard)
            spawn_fruit(self.maze)

            pg.display.update()

            # stops the game loop when exiting
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    self.running = False
                    sys.exit()

    def start_screen(self):
        start = True
        self.screen.fill(settings.bg_color)

        # credits
        font = pg.font.SysFont('Ariel', 24, False)
        text = font.render('By Andy Duong for CPSC 386', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.left, text_rect.centery = 16, settings.screen_height - 16
        self.screen.blit(text, text_rect)

        # pacman title
        # from https://www.pinterest.com/pin/531002612301180531/
        title_img = pg.image.load('assets/images/title.png')
        title_img = pg.transform.rotozoom(title_img, 0, 0.15)
        title_rect = title_img.get_rect()
        title_rect.centerx, title_rect.centery = settings.screen_width / 2, 150
        self.screen.blit(title_img, title_rect)

        # play game
        font = pg.font.SysFont('Ariel', 40, False)
        play = font.render('PLAY GAME', True, (255, 255, 255))
        play_rect = play.get_rect()
        play_rect.centerx, play_rect.centery = settings.screen_width / 2, 800
        self.screen.blit(play, play_rect)

        # high scores
        font = pg.font.SysFont('Ariel', 40, False)
        high = font.render('HIGH SCORES', True, (255, 255, 255))
        high_rect = high.get_rect()
        high_rect.centerx, high_rect.centery = settings.screen_width / 2, 850
        self.screen.blit(high, high_rect)

        # intro
        ss = SpriteSheet.Spritesheet('assets/images/all_ghosts.png')
        ghosts = []
        names = ['Blinky', 'Clyde', 'Inkey', 'Pinky']
        for i in range(4):
            ghosts.append(ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
            ghost_rect = ghosts[i].get_rect()
            ghost_rect.x, ghost_rect.y = settings.screen_width / 2 - 100, (settings.screen_height / 3 + 64 * i) - 64
            self.screen.blit(ghosts[i], ghost_rect)

            font = pg.font.SysFont('Ariel', 40, False)
            txt = names[i]
            p = font.render(txt, True, (255, 255, 255))
            p_rect = p.get_rect()
            p_rect.centerx, p_rect.centery = settings.screen_width / 2 + 64, settings.screen_height / 3 + 64 * i - 16
            self.screen.blit(p, p_rect)
            pg.display.update()
            pg.time.delay(250)

        while start:
            # chase
            pg.draw.rect(self.screen, (0, 0, 0), (0, 550, 720, 200))
            ss1 = SpriteSheet.Spritesheet('assets/images/chase1.png')
            ss2 = SpriteSheet.Spritesheet('assets/images/chase2.png')
            chase1, chase2 = [], []
            for i in range(5):
                chase1.append(ss1.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
                chase2.append(ss2.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
            x_values = [64, 128, 192, 256, 384]
            if pg.time.get_ticks() < 4500:
                for i in range(5):
                    ghost_rect = chase1[i].get_rect()
                    ghost_rect.x, ghost_rect.y = x_values[i] + (pg.time.get_ticks() / 5) - 100, 600
                    self.screen.blit(chase1[i], ghost_rect)
            else:
                for i in range(5):
                    ghost_rect = chase2[i].get_rect()
                    ghost_rect.x, ghost_rect.y = x_values[i] - (pg.time.get_ticks() / 5) + 1500, 600
                    self.screen.blit(chase2[i], ghost_rect)

            pg.display.update()

            x, y = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_rect.collidepoint(x, y):
                            start = False
                            self.run_game()
                        if high_rect.collidepoint(x, y):
                            self.high_score_screen()
                            start = False

    def high_score_screen(self):
        on_menu = True
        self.screen.fill(settings.bg_color)
        font = pg.font.SysFont('Ariel', 100, False)
        text = font.render('HIGH SCORES', True, (255, 0, 0))
        rect = text.get_rect()
        rect.centerx, rect.centery = settings.screen_width / 2, 100
        self.screen.blit(text, rect)

        font = pg.font.SysFont('Ariel', 40, False)
        for i in self.high_scores:
            text = font.render(str(i), True, (255, 255, 255))
            rect = text.get_rect()
            rect.centerx, rect.centery = settings.screen_width / 2, self.high_scores.index(i) * 32 + 200
            self.screen.blit(text, rect)

        pg.display.update()
        while on_menu:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        on_menu = False
                        self.start_screen()

    def game_over_screen(self):
        game_over = True
        self.screen.fill(settings.bg_color)
        result = 'Score: ' + str(self.scoreboard.score)
        pg.mixer.music.stop()
        font = pg.font.SysFont('Ariel', 100, True)
        text = font.render(result, True, (255, 0, 0))
        rect = text.get_rect()
        rect.centerx, rect.centery = settings.screen_width / 2, 250
        self.screen.blit(text, rect)

        font = pg.font.SysFont('Ariel', 40, False)
        restart = font.render('RESTART', True, (255, 255, 255))
        restart_rect = restart.get_rect()
        restart_rect.centerx, restart_rect.centery = settings.screen_width / 2, 850
        self.screen.blit(restart, restart_rect)

        pg.display.update()

        write_high_score(self.high_scores, self.scoreboard.score)

        while game_over:
            x, y = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_rect.collidepoint(x, y):
                            game_over = False
                            self.reset()

    def reset(self):
        self.running = False
        self.scoreboard = None
        self.maze = None
        self.pacman = None
        self.blinky = None
        self.pinky = None
        self.inkey = None
        self.clyde = None
        self.start_screen()


def main():
    game = Game()  # creates instance of the game
    game.start_screen()  # runs the game


if __name__ == '__main__':
    main()
