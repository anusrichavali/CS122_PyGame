import pygame
import os

pygame.mixer.init()
s = 'sound'
click = pygame.mixer.Sound(os.path.join(s, 'click.mp3'))
collide_prop = pygame.mixer.Sound(os.path.join(s, 'collide_prop.wav'))
game_over = pygame.mixer.Sound(os.path.join(s, 'game_over.wav'))
level_up = pygame.mixer.Sound(os.path.join(s, 'level_up.wav'))
prop_drop = pygame.mixer.Sound(os.path.join(s, 'prop_drop.wav'))
background_music = pygame.mixer.Sound(os.path.join(s, 'background_music.wav'))
background_music.set_volume(0.5)