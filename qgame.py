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
LEARNING_RATE = 0.2  # Learning rate for Q-Learning
DISCOUNT_FACTOR = 0.8  # Discount factor for future rewards
EPSILON = 0  # Exploration rate //NOT USED
NUM_EPISODES = 10_000_000  # Number of training episodes

# Q-Table to store Q-values for state-action pairs


class QGame:
    def __init__(self, q_table=defaultdict(lambda: [0, 0]), epsilon=0, learn_mode="fixed"):
        py.init()

        self.learning_rate = LEARNING_RATE
        self.discount_factor = DISCOUNT_FACTOR
        self.epsilon = epsilon
        self.num_episodes = NUM_EPISODES

        self.q_table = q_table

        self.WIDTH = 400
        self.HEIGHT = 600

        self.window = py.display.set_mode((self.WIDTH, self.HEIGHT))

        self.TIME_STEP = 0.0166

        self.color = (0, 0, 0)
        py.display.set_caption("Flappy Bird")
        self.bird = Bird(self.window, "qlearn", learn_mode)
        self.obstacle = Obstacle(self.window, "qlearn", learn_mode)

        self.clock = py.time.Clock()

        self.score = 0
        self.max_score = 0

        self.game_over = False

        self.kill = False
        self.elapsed_time = 0
        self.elapsed_seconds = 0
        self.start_time = time.time()
        self.learn_mode = learn_mode

    def get_state(self):
        # Simplified state representation:
        # Distance to the next obstacle and bird's height relative to obstacles
        dist_x = int(self.obstacle.rect1.x) - int(self.bird.rect.x)
        dist_y = int(self.bird.rect.y) - int(self.obstacle.rect1.height) - 50
        return (dist_x, dist_y, +self.game_over)

    def get_action(self, state):
        # Epsilon-greedy exploration
        if random.random() < self.epsilon:
            return random.choice([0, 0, 0, 1])  # Random action (exploration)
        else:
            # Best action from Q-Table (exploitation)
            return np.argmax(self.q_table[state])

    def play(self):
        for episode in range(self.num_episodes):
            self.reset_game()  # Reset game state for each episode
            total_reward = 0  # Track total reward in this episode
            state = self.get_state()
            self.epsilon = self.epsilon * 0.95  # Decay epsilon
            while not self.game_over:
                current_time = time.time()
                self.elapsed_seconds = int(current_time - self.start_time)
                dt = self.clock.tick(1//self.TIME_STEP) / \
                    1000  # Control frame rate
                self.elapsed_time += dt
                # Choose an action based on current state
                action = self.get_action(state)
                self.perform_action(action)  # Perform the chosen action

                self.window.fill(self.color)  # Clear the screen
                self.update()  # Update game state
                self.draw()  # Draw game elements
                self.handle_events()

                py.display.flip()  # Update the display

                next_state = self.get_state()  # Get the new state after the action
                # Get the reward for the action
                reward = self.get_reward(next_state, action)

                # Update the Q-Table using the Q-Learning update rule
                current_q = self.q_table[state][action]
                max_next_q = max(self.q_table[next_state])
                new_q = current_q + self.learning_rate * (
                    reward + self.discount_factor * max_next_q - current_q)
                self.q_table[state][action] = new_q
                total_reward += reward  # Add the reward to the total for this episode
                state = next_state  # Update the current state
            if self.kill:
                break
            print(f"Episode {
                  episode + 1}: Total Reward = {total_reward} Score = {math.ceil(self.score)}")

        py.quit()  # Quit the game when done

    def reset_game(self):
        # Reset the game to the initial state
        self.game_over = False
        self.score = 0
        self.bird = Bird(self.window, "qlearn", self.learn_mode)
        self.obstacle = Obstacle(self.window, "qlearn", self.learn_mode)

    def perform_action(self, action):
        # Perform the chosen action (0 = no jump, 1 = jump)
        if action == 1:
            self.bird.jump()  # Bird jumps if the action is 1

    def get_reward(self, next_state, action):
        # Define the reward system:
        # - Positive reward for scoring
        # - Negative reward for collisions
        if self.game_over:
            return -100  # Negative reward for game over

        dist_x = next_state[0]
        dist_y = next_state[1]

        if dist_x < 0 and self.elapsed_time >= 2:
            self.elapsed_time = 0
            self.score += 1
            return 10
        if dist_y > 20 and action == 0:
            return -1
        elif dist_y < -20 and action == 1:
            return -1
        return 1

    def update(self):
        self.bird.update(self.TIME_STEP)
        self.obstacle.update(self.TIME_STEP)
        self.check_collision()

    def draw(self):
        self.bird.draw()
        self.obstacle.draw()
        self.draw_score()

        font = py.font.Font(None, 36)
        text = font.render(str(datetime.timedelta(
            seconds=self.elapsed_seconds)), True, (255, 255, 255))
        self.window.blit(text, (self.WIDTH - 100, 50))

        py.display.flip()

    def check_collision(self):
        # Check for collisions with obstacles
        if self.bird.rect.colliderect(self.obstacle.rect1) or self.bird.rect.colliderect(self.obstacle.rect2):
            self.game_over = True

        # Check if the bird hits the ground or goes out of bounds
        if self.bird.rect.y >= self.HEIGHT - self.bird.height:
            self.game_over = True

    def draw_score(self):
        font = py.font.Font(None, 36)
        text = font.render(str(math.ceil(self.score)), True, (255, 255, 255))
        self.window.blit(text, (self.WIDTH // 2, 50))

    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game_over = True
                kill = input("Kill? (y/n):")
                if kill == "y":
                    self.kill = True
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.bird.jump()
