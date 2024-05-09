import pygame as py


class Bird:
    def __init__(self, window, play_mode, learn_mode):
        self.window = window

        self.y = self.window.get_height()//2
        self.x = 50

        self.width = 10
        self.height = 10

        self.acceleration_y = 0
        self.velocity_y = 0
        self.gravity = 9.8

        self.max_velocity = self.window.get_height()//3

        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 255, 255)

        self.play_mode = play_mode
        self.learn_mode = learn_mode

    def update(self, time_step):
        self.acceleration_y += self.gravity * time_step
        self.velocity_y = min(
            self.max_velocity, self.acceleration_y + self.velocity_y)
        self.y = max(0, self.y + self.velocity_y * time_step)
        self.y = min(self.window.get_height() - self.height, self.y)

        self.rect.y = self.y

    def jump(self):
        self.acceleration_y = 0
        if self.play_mode == "play":
            self.velocity_y = -self.window.get_height()//3
        elif self.learn_mode == "fixed":
            self.velocity_y = -self.window.get_height()//8
        else:
            self.velocity_y = -self.window.get_height()//5

    def draw(self):
        py.draw.rect(self.window, self.color, self.rect)
