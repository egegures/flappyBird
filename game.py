# This does not implement q-learning, only used for test purposes

import bird
import obstacle
import pygame as py
import time


class Game: 
    
    def __init__(self):
        py.init()
        
        self.TIME_STEP = 0.0166
        
        self.WIDTH = 400
        self.HEIGHT = 400
        self.window = py.display.set_mode((self.WIDTH, self.HEIGHT))
        self.color = (0,0,0)
        py.display.set_caption("Flappy Bird")
        
        self.bird = bird.Bird(self.window)
        self.obstacle = obstacle.Obstacle(self.window, learn_mode = "random")

        self.game_over = False
        self.score = 0
        
        self.clock = py.time.Clock()
        
        self.elapsed_time = 0
        
    def play(self):
        while not self.game_over:
            dt = self.clock.tick(1//self.TIME_STEP)
            self.elapsed_time += dt/1000
            self.window.fill(self.color)
            self.handle_events()
            self.update()
            self.draw()
            
            py.display.flip()
            
        py.quit()
        
    def update(self):
        self.bird.update()
        self.obstacle.update()
        self.check_collision()
        if self.bird.rect.x > self.obstacle.rect1.x and self.elapsed_time > 1:
            self.elapsed_time = 0
            self.score += 1
        
    def draw(self):
        self.bird.draw()
        self.obstacle.draw()
        self.draw_score()
        
    def check_collision(self):
        if self.bird.rect.colliderect(self.obstacle.rect1) or self.bird.rect.colliderect(self.obstacle.rect2):
            self.game_over = True
            
        if self.bird.rect.y > self.HEIGHT - self.bird.height - 1:
            self.game_over = True
            
            
    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game_over = True
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.bird.jump()
    
    def draw_score(self):
        font = py.font.Font(None, 36)
        text = font.render(str(self.score), True, (255, 255, 255))
        self.window.blit(text, (self.WIDTH//2, 50))
    
        
        
        
        