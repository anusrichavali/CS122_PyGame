import pygame
import os

pygame.mixer.init()
s = 'sound'
#sound for button click
click = pygame.mixer.Sound(os.path.join(s, 'click.mp3'))
#sound for collisions with prop
collide_prop = pygame.mixer.Sound(os.path.join(s, 'collide_prop.wav'))
#sound for game over
game_over = pygame.mixer.Sound(os.path.join(s, 'game_over.wav'))
#sound for level up
level_up = pygame.mixer.Sound(os.path.join(s, 'level_up.wav'))
#sound for when prop hits the ground
prop_drop = pygame.mixer.Sound(os.path.join(s, 'prop_drop.wav'))
#sound for bonus prop
bonus_prop = pygame.mixer.Sound(os.path.join(s, 'bonus_prop.wav'))
#sound for background music
background_music = pygame.mixer.Sound(os.path.join(s, 'background_music.wav'))
background_music.set_volume(0.5)