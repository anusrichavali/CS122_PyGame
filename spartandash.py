#space invaders game
import pygame
import os
import time
import random

pygame.init()

font = pygame.font.Font("resources/Grand9KPixel.ttf", 25)

#load sprite (main player)
with open('Starting_Page/selected_character.txt', 'r') as file:
    # Read the first line
    character = file.readline().strip()
if(character == "Neha"):
    sprite = pygame.image.load("resources/Neha_Sprite.png")
elif(character == "Anusri"):
    sprite = pygame.image.load("resources/Anusri_Sprite.png")
elif(character == "Erica"):
    sprite = pygame.image.load("resources/Erica_Sprite.png")

#create the screen and configure the screen size and caption
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill("#87CEEB")
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

#load and scale background. update enemies based on location
with open('Starting_Page/selected_location.txt', 'r') as file:
    location = file.readline().strip()

if(location == "SRAC"): #CHANGE THIS TO TOWER LAWN!!!
    background = pygame.image.load("resources/tower_lawn.jpeg")
    #load enemies --> these are the things that will shoot at sprite 
    enemy_1 = pygame.image.load("resources/Bee.png")
    enemy_2 = pygame.image.load("resources/Fly.png")
elif(location == "SRAC"):
    background = pygame.image.load("resources/srac.png")
    #load enemies --> these are the things that will shoot at sprite 
    enemy_1 = pygame.image.load("resources/dumbell.png")
    enemy_2 = pygame.image.load("resources/basketball.png")
elif(location == "MLK"):
    background = pygame.image.load("resources/mlk.png")
    #load enemies --> these are the things that will shoot at sprite 
    enemy_1 = pygame.image.load("resources/books.png")
    enemy_2 = pygame.image.load("resources/laptop.png")

#scale background to fit screen
DEFAULT_SIZE = (350, 245)
original_width, original_height = background.get_size()
new_height = int((screen_info.current_w / original_width) * original_height)
background = pygame.transform.scale(background, (screen_info.current_w, new_height))

#load shooters --> this is what comes out of the enemies and sprite
enemy_1_shooter = pygame.image.load("resources/shooter-blue.png")
enemy_2_shooter = pygame.image.load("resources/shooter-red.png")
sprite_shooter = pygame.image.load("resources/shooter-sprite.png")


class Asset:
    def __init__(self, xPos, yPos, health = 100):
        self.xPos = xPos
        self.yPos = yPos
        self.health = health
        self.sprite_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.xPos, self.yPos, 50, 50))

#main loop
def run():
    running = True
    timer = pygame.time.Clock()
    FPS = 60 #frames per second for speed
    level = 1
    lives = 5

    asset = Asset(300, 650)

    while running:
        timer.tick(FPS)
        set_background(level, lives, asset)

        for event in pygame.event.get():
            #exit the loop and close the screen in player quits
            if event.type == pygame.QUIT:
                running = False

def set_background(level, lives, asset):
    #draw background to screen
    screen.blit(background, (0,0)) 
    pygame.display.update()

    levels_text = font.render(f"Level: {level}", True, "#ebfbfc")
    lives_text = font.render(f"Lives: {lives}", True, "#ebfbfc")

    screen.blit(levels_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    asset.draw(screen)

    pygame.display.update()

run()     
