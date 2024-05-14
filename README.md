# Flappy Bird AI Model Using Q-Learning

## Overview 

This project implements an AI agent using Q-Learning to play the classic game Flappy Bird. 
The agent learns to navigate through obstacles by adjusting its actions based on rewards received from the environment.

<p align="center">
  <img src="https://github.com/egegures/flappyBird/assets/87149006/178662bd-c5aa-40fc-90b1-808fc1a109e9" width="300">
</p>
It has two modes of learning, one of which has fixed gaps at the middle of the screen and the other one is randomized. Pre trained models are present and can be loaded for testing purposes.
<p align="center">
  <img src="https://github.com/egegures/flappyBird/assets/87149006/aabfd5e0-54e6-4d4e-9e66-4a47266e4504" width="400">
  <img src="https://github.com/egegures/flappyBird/assets/87149006/65bc8ddb-e2c1-4b74-803c-70cc6616a535" width="400">
</p>
The "learning curve" for the fixed gap model is plotted above. At one point, the agent learns the game enough and reaches 10,000 points in episode 226, right after reaching only 80. Episode 226 is not plotted on the left for better visualization. 
<p align="center">
  <img src="https://github.com/egegures/flappyBird/assets/87149006/ba1c80d0-24ca-4fde-85f0-425ba12c5837" width="400">
  <img src="https://github.com/egegures/flappyBird/assets/87149006/867ae8f1-b97e-4fe4-9368-ad4092514310" width="400">
</p>
Random gap game mode has a similar curve but it takes around 25% more iterations to "learn" and pass the 1000 score mark. Last 10 episodes are not plotted on the left for better visualization.
<br> 
<br>
Web version will be available in the future. 
