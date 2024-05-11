import pygame as py 
import random


class Obstacle: 
    def __init__ (self, window, learn_mode):
    
        self.learn_mode = learn_mode
        
        self.window = window

        
        self.x = self.window.get_width()
        self.y = self.window.get_height()
        self.width = 25
        
        self.velo_x = -3.5
            
        self.rect1 = py.Rect(self.x, 0, self.width, (self.y - 100)//2)
        self.rect2 = py.Rect(self.x, (self.y + 100)//2, self.width, self.y)
        
        
        
        
    def update(self):
        self.x += self.velo_x
        self.rect1.x = self.x
        self.rect2.x = self.x
        
        if self.x < 0:
            self.x = self.window.get_width()
            self.rect1.x = self.x
            self.rect2.x = self.x
            if self.learn_mode == "random":
                new_y = random.randint(60, self.window.get_height() - 60) # Random height
                self.rect1.height = new_y - 50
                self.rect2.y = new_y + 50
    def draw(self):
        py.draw.rect(self.window, (255, 255, 255), self.rect1)
        py.draw.rect(self.window, (255, 255, 255), self.rect2)