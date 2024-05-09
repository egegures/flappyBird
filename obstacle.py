import pygame as py
import random


class Obstacle:
    def __init__(self, window, play_mode, learn_mode):

        self.play_mode = play_mode
        self.learn_mode = learn_mode

        self.window = window

        self.x = self.window.get_width()
        self.y = self.window.get_height()
        self.width = 50

        if play_mode == "play":
            self.velo_x = -200  # For personal use
        else:
            self.velo_x = -self.window.get_width()//3  # For q-learning

        self.rect1 = py.Rect(self.x, 0, self.width, (self.y - 100)//2)
        self.rect2 = py.Rect(self.x, (self.y + 100)//2, self.width, self.y)

    def update(self, time_step):
        self.x += self.velo_x * time_step
        self.rect1.x = self.x
        self.rect2.x = self.x

        if self.x < -self.width:
            self.x = self.window.get_width()
            self.rect1.x = self.x
            self.rect2.x = self.x
            if self.learn_mode == "random":
                new_y = random.randint(
                    100, self.window.get_height() - 100)  # Random height
                self.rect1.height = new_y - 50
                self.rect2.y = new_y + 50

    def draw(self):
        py.draw.rect(self.window, (255, 255, 255), self.rect1)
        py.draw.rect(self.window, (255, 255, 255), self.rect2)
