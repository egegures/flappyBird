import pygame as py


class Bird:
    def __init__ (self, window):
        
        self.window = window

        self.y = self.window.get_height()//2
        self.x = 50

        self.width = 15
        self.height = 15
        
        self.acceleration_y = 0
        self.velocity_y = 0
        self.gravity = 0.03
        
        self.max_velocity = 15
        
        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 255, 255)
        
    def update(self): 
        self.acceleration_y += self.gravity
        self.velocity_y = min(self.max_velocity, self.acceleration_y + self.velocity_y)
        self.y = max(0, self.y + self.velocity_y)
        self.rect.y = self.y

    def jump(self):
        self.acceleration_y = 0
        self.velocity_y = -4.5
        
    def draw(self):
        py.draw.rect(self.window, self.color, self.rect)
