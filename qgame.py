# This includes the q-learning implementation without neural networks. 

from bird import Bird
from obstacle import Obstacle
import pygame as py
import time
import numpy as np
import random
from collections import defaultdict
import math 
import datetime

# Q-Learning Parameters
LEARNING_RATE = 0.1 # Learning rate for Q-Learning
DISCOUNT_FACTOR = 0.8  # Discount factor for future rewards
EPSILON = 0 # Exploration rate //NOT USED
NUM_EPISODES = 10 ** 8 # Number of training episodes

class QGame:
    def __init__(self, q_table = defaultdict(lambda: [0, 0]), epsilon = 0.4, learn_mode = "fixed"):
        py.init()
        
        self.learning_rate = LEARNING_RATE
        self.discount_factor = DISCOUNT_FACTOR
        self.epsilon = epsilon
        self.num_episodes = NUM_EPISODES
        
        self.q_table = q_table
        
        self.WIDTH = 400
        self.HEIGHT = 400
        
        self.window = py.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.FPS = 60 * 13
        
        self.color = (0, 0, 0)
        py.display.set_caption("Flappy Bird")
        self.bird = Bird(self.window)
        self.obstacle = Obstacle(self.window, learn_mode)
        
        self.clock = py.time.Clock()
        
        self.score = 0
        self.max_score = 0
        
        self.game_over = False
        
        self.kill = False
        self.elapsed_time = 0
        self.elapsed_seconds = 0
        self.start_time = time.time()
        self.learn_mode = learn_mode
        
        self.max_score_episode = 0
        self.max_score_time = 0

    def play(self):
        for episode in range(self.num_episodes):
            self.reset_game()  # Reset game state for each episode
            total_reward = 0  # Track total reward in this episode
            state = self.get_state()
            self.epsilon = self.epsilon * 0.98 # Decay epsilon
            
            while not self.game_over:
                self.update_time()
                action = self.get_action(state)  # Choose an action based on current state
                self.perform_action(action)  # Perform the chosen action
                
                self.update(episode + 1)  # Update game state
                self.draw(self.max_score_episode, self.max_score_time)  # Draw game elements
                self.handle_events()
                
                next_state = self.get_state()  # Get the new state after the action
                reward = self.get_reward(next_state, action)  # Get the reward for the action
                
                # Update the Q-Table using the Q-Learning update rule
                self.update_q_table(state, action, next_state, reward)  # Update Q-table
                total_reward += reward  # Add the reward to the total for this episode
                state = next_state  # Update the current state
            
            if self.kill:
                break
            print(f"Episode {episode + 1}: Total Reward = {total_reward} Score = {math.ceil(self.score)}")

        py.quit()  # Quit the game when done
        
    # Update the Q-Table using the Q-Learning update rule
    def update_q_table(self, state, action, next_state, reward):
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    # Reset the game to the initial state
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(self.window)
        self.obstacle = Obstacle(self.window, self.learn_mode)
        
    # Returns the state described by the distance to the next obstacle and the bird's height relative to the gap
    def get_state(self):
        obstacle_gap_y = self.obstacle.rect1.height + 50
        
        dist_x = int(self.obstacle.rect2.x - self.bird.rect.x) 
        dist_y = int(self.bird.rect.y - obstacle_gap_y)
        return (dist_x, dist_y)

    def get_action(self, state):
        # Epsilon-greedy exploration
        if random.random() < self.epsilon:
            return np.random.choice([0,1], p = [0.9, 0.1])  # Random action (exploration)
        else:
            return np.argmax(self.q_table[state])  # Best action from Q-Table (exploitation)

    # Perform the chosen action (0 = no jump, 1 = jump)
    def perform_action(self, action):
        if action == 1:
            self.bird.jump()

    # - Positive reward for scoring
    # - Negative reward for collisions
    def get_reward(self, next_state, action):
        if self.game_over:
            return -100  # Negative reward for game over
        
        dist_x = next_state[0]
        dist_y = next_state[1]

        if dist_x < self.obstacle.rect1.width and self.elapsed_time >= 1 * 60 / self.FPS:
            self.elapsed_time = 0
            self.score += 1
            return 10
        if dist_y > 20 and action == 0: # Bird is below the gap and does not jump
            return -1
        elif dist_y < -10 and action == 1: # Bird is above the gap and jumps
            return -1
        return 1

    def update(self,episode):
        self.window.fill(self.color)  # Clear the screen
        self.bird.update()
        self.obstacle.update()
        self.check_collision()
        if self.score > 20: # No exploration after reaching 20 points
            self.epsilon = 0 
        
        if self.score > self.max_score: # Update max score
            self.max_score = self.score
            self.max_score_episode = episode
            self.max_score_time = self.elapsed_seconds
            

    def draw(self, episode, time):
        self.bird.draw()
        self.obstacle.draw()
        
        time_elapsed = datetime.timedelta(seconds=self.elapsed_seconds)
        
        font = py.font.Font(None, 22)
        text = font.render(str(time_elapsed), True, (255, 255, 255)) # Display time
        self.window.blit(text, (self.WIDTH - 100, 20))

        text = font.render(f"Score = {self.score}", True, (255, 255, 255)) # Display score
        self.window.blit(text, (0, 20))
        
        time = datetime.timedelta(seconds=time) 
        text = font.render(f"Max Score = {self.max_score}", True, (255, 255, 255)) # Display max score
        self.window.blit(text, (0, 60))
        
        text = font.render(f"Reached at episode: {episode}, at time: {time}", True, (255, 255, 255))
        self.window.blit(text, (0,80))
        
        py.display.flip()  # Update the display

    # Check for collisions with obstacles or hits the ground
    def check_collision(self):
        if self.bird.rect.colliderect(self.obstacle.rect1) or self.bird.rect.colliderect(self.obstacle.rect2):
            self.game_over = True

        if self.bird.rect.y >= self.HEIGHT - self.bird.height:
            self.game_over = True

    def update_time(self):
        current_time = time.time()
        self.elapsed_seconds = int(current_time - self.start_time)
        self.elapsed_time +=  self.clock.tick(self.FPS) / 1000 # Control frame rate

    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game_over = True
                self.kill = True
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.bird.jump()