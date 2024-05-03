#space invaders game
import pygame
import os
import time
import random

pygame.init()

font = pygame.font.Font("resources/Grand9KPixel.ttf", 25)
message_font = pygame.font.Font("resources/Grand9KPixel.ttf", 60)

#load sprite (main player)
with open('selected_character.txt', 'r') as file:
    # Read the first line
    character = file.readline().strip()
if(character == "Neha"):
    sprite = "resources/Neha_Sprite.png"
elif(character == "Anusri"):
    sprite = "resources/Anusri_Sprite.png"
elif(character == "Erica"):
    sprite = "resources/Erica_Sprite.png"

#create the screen and configure the screen size and caption
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill("#87CEEB")
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

#load and scale background. update enemies based on location
with open('selected_location.txt', 'r') as file:
    location = file.readline().strip()

if(location == "TOWER LAWN"): #CHANGE THIS TO TOWER LAWN!!!
    background = pygame.image.load("resources/tower_lawn.jpeg")
    #load enemies --> these are the things that will shoot at sprite 
    obs_1 = "resources/Bee.png"
    obs_2 = "resources/Fly.png"
elif(location == "SRAC"):
    background = pygame.image.load("resources/srac.png")
    #load enemies --> these are the things that will shoot at sprite 
    obs_1 = "resources/dumbbell.png"
    obs_2 = "resources/basketball.png"
elif(location == "MLK"):
    background = pygame.image.load("resources/mlk.png")
    #load enemies --> these are the things that will shoot at sprite 
    obs_1 = "resources/books.png"
    obs_2 = "resources/laptop.png"

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
    def __init__(self, xPos, yPos, lives = 5, sprite_img = None):
        self.xPos = xPos
        self.yPos = yPos
        self.lives = lives
        if sprite_img:
            self.sprite_img = pygame.image.load(sprite_img)
            self.sprite_img = pygame.transform.scale(self.sprite_img, (100, 100))
            self.mask = pygame.mask.from_surface(self.sprite_img)
        else:
            self.sprite_img = None
            self.mask = None
        self.lasers = []
        self.cool_down_counter = 0
        self.visible = True

    def draw(self, screen):
        if self.sprite_img:
            screen.blit(self.sprite_img, (self.xPos, self.yPos))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.xPos, self.yPos, 50, 50))

    def move_x(self, value):
        self.xPos += value
    
    def move_y(self, value):
        self.yPos += value
    
    # checks if the player and prop collide
    def collide(self, player, prop):
        offset_x = prop.xPos - player.xPos
        offset_y = prop.yPos - player.yPos
        if player.mask and prop.mask:
            return player.mask.overlap(prop.mask, (offset_x, offset_y))
        return False

#main loop
def run():
    running = True
    timer = pygame.time.Clock()
    FPS = 85 #frames per second for speed
    level = 0
    score = 0

    player = Asset(300, 650, sprite_img = sprite)

    props = []
    prop_num = 5
    lost_status = False
    lost_message_time = 0

    while running:
        set_background(level, player, props, lost_status, score)
        timer.tick(FPS)

        if player.lives <= 0:
            lost_status = True
            lost_message_time += 1

        if lost_status == True:
            if lost_message_time >= FPS * 3:
                running = False
            else:
                continue
        else:
            if len(props) == 0:
                level += 1
                prop_num += 1
                for num in range(prop_num):
                    prop = Asset(random.randrange(50, screen_info.current_w - 100), random.randrange(-2000, -100), 100, random.choice([obs_1, obs_2]))
                    props.append(prop)

            for event in pygame.event.get():
                #exit the loop and close the screen in player quits
                if event.type == pygame.QUIT:
                    running = False

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT] == True and player.xPos + 50 <= screen_info.current_w:
                player.move_x(7)
            if pressed[pygame.K_LEFT] == True and player.xPos >= 0:
                player.move_x(-7)
            if pressed[pygame.K_UP] == True and player.yPos >= 0:
                player.move_y(-7)
            if pressed[pygame.K_DOWN] == True and player.yPos + 50 <= screen_info.current_h: 
                player.move_y(7)

            for prop in props:
                prop.move_y(1)
                if prop.yPos + 100 > screen_info.current_h:
                    player.lives -= 1
                    score -= 125
                    props.remove(prop)
                # if collision, remove prop from screen
                if player.collide(player, prop):
                    prop.visible = False
                    score += 100
                    props.remove(prop)

    return "Done"

def set_background(level, player, props, lost_status, score):
    #draw background to screen
    screen.blit(background, (0,0)) 

    levels_text = font.render(f"Level: {level}", True, "black")
    lives_text = font.render(f"Lives: {player.lives}", True, "black")
    score_text = font.render(f"Score: {score}", True, "black")

    screen.blit(levels_text, (screen_info.current_w - 165, 10))
    screen.blit(lives_text, (screen_info.current_w - 165, 50))
    screen.blit(score_text, (screen_info.current_w - 165, 90))

    player.draw(screen)
    for prop in props:
        prop.draw(screen)

    if lost_status == True:
        lost_text = message_font.render("You Lost!", 1, "black")
        screen.blit(lost_text, ((screen_info.current_w - lost_text.get_width())/2, (screen_info.current_h - lost_text.get_height())/2))

    pygame.display.update()