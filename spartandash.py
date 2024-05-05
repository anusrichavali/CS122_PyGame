import pygame
import random
import sounds

pygame.init()

font = pygame.font.Font("resources/Grand9KPixel.ttf", 25)
message_font = pygame.font.Font("resources/Grand9KPixel.ttf", 60)
smaller_font = pygame.font.Font("resources/Grand9KPixel.ttf", 20)
game_over_sound = False

pygame.mixer.music.load('sound/background_music2.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

#create buttons with specified sizes, fontsize, and color
def button_creation(fontSize, text, x, y, sizeW, sizeH, color):
    font = pygame.font.Font("resources/Grand9KPixel.ttf", fontSize)
    button = pygame.Surface((sizeW,sizeH))
    button.fill(color)
    message = font.render(text, True, "#ebfbfc")
    message_rect = message.get_rect(center=(button.get_width()/2, button.get_height()/2))
    button_rect = pygame.Rect(x, y, sizeW, sizeH)
    return [button, message, message_rect, button_rect]

#writes the high score to high_score.txt
def write_high_score(high_score, score):
    if score > int(high_score):
        with open("saved_states/high_score.txt", "w") as file:
            file.write(str(score))

#load sprite (main player)
#chooses random if selected_character.txt does not exist
try: 
    with open('saved_states/selected_character.txt', 'r') as file:
        # Read the first line
        character = file.readline().strip()
except:
    character = random.choice(["Neha", "Anusri", "Erica"])

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
#chooses random if selected_location.txt does not exist
try: 
    with open('saved_states/selected_location.txt', 'r') as file:
        location = file.readline().strip()
except:
    location = random.choice(["TOWER LAWN", "SRAC", "MLK"])
#load background and props based on the selected location
if(location == "TOWER LAWN"):
    background = pygame.image.load("resources/tower_lawn.jpeg")
    prop_1 = "resources/Bee.png"
    prop_2 = "resources/Fly.png"
    bonus_prop = "resources/energy.png"
elif(location == "SRAC"):
    background = pygame.image.load("resources/srac.png")
    prop_1 = "resources/dumbbell.png"
    prop_2 = "resources/basketball.png"
    bonus_prop = "resources/energy.png"
elif(location == "MLK"):
    background = pygame.image.load("resources/mlk.png")
    prop_1 = "resources/books.png"
    prop_2 = "resources/laptop.png"
    bonus_prop = "resources/energy.png"


#scale background to fit screen
DEFAULT_SIZE = (350, 245)
original_width, original_height = background.get_size()
new_height = int((screen_info.current_w / original_width) * original_height)
background = pygame.transform.scale(background, (screen_info.current_w, new_height))

#asset class that is used to generate players and props
class Asset:
    def __init__(self, xPos, yPos, lives = 5, sprite_img = None):
        self.xPos = xPos
        self.yPos = yPos
        self.lives = lives
        if sprite_img:
            self.sprite_img_path = sprite_img
            self.sprite_img = pygame.image.load(sprite_img)
            self.sprite_img = pygame.transform.scale(self.sprite_img, (100, 100))
            self.mask = pygame.mask.from_surface(self.sprite_img)
        else:
            self.sprite_img = None
            self.mask = None
        self.lasers = []
        self.cool_down_counter = 0
        self.visible = True

    #draw the character on the screen
    def draw(self, screen):
        if self.sprite_img:
            screen.blit(self.sprite_img, (self.xPos, self.yPos))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.xPos, self.yPos, 50, 50))

    #move character horizontally
    def move_x(self, value):
        self.xPos += value
    
    #move character vertically
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
    #read the high score into the variable
    with open("saved_states/high_score.txt", "r") as file:
        high_score = file.readline().strip()

    global game_over_sound
    #initalizes variables when the game starts
    running = True
    timer = pygame.time.Clock()
    FPS = 85 #frames per second for speed
    
    level = 0
    score = 0

    props = []
    prop_num = 5
    prop_speed = 1
    player_speed = 7

    player_size_timer = None
    player_original_size = (100, 100)

    lost_status = False
    pause_message = "Pause"
    pause_color = "#f2461f"
    paused = False

    #creates the player asset
    player = Asset(300, 650, sprite_img = sprite)

    #initiates variables to handle the set of props, number of props in each wave, and prop/player's speed

    #creates restart and quit buttons to display on screen at relevant times
    restart_button = button_creation(30, "Restart", screen_info.current_w/2 - 150, screen_info.current_h/2 + 15, 150, 50, "#f2461f")
    quit_button = button_creation(30, "Quit", screen_info.current_w/2 + 25, screen_info.current_h/2 + 15, 150, 50, "#f2461f")

    while running:
        #creates updated pause button based on pause status
        pause_button = button_creation(20, pause_message, 10, 10, 100, 30, pause_color)
        #sets the background based on all updated variables
        set_background(level, player, props, lost_status, score, pause_button, restart_button, quit_button, paused, high_score)
        timer.tick(FPS)

        #sets lost status when player has no lives
        if player.lives <= 0:
            lost_status = True

        #generates a new wave of props and updates level when all props in previous wave are eliminated
        if len(props) == 0:
            pygame.mixer.Sound.play(sounds.level_up)
            level += 1
            prop_num += 1
            prop_speed += 0.5
            player_speed += 1
            for num in range(prop_num):
                if random.random() < 0.1:
                    prop = Asset(random.randrange(50, screen_info.current_w - 100), random.randrange(-2000, -100), 100, bonus_prop)
                else:
                    prop = Asset(random.randrange(50, screen_info.current_w - 100), random.randrange(-2000, -100), 100, random.choice([prop_1, prop_2]))
                props.append(prop)

        #handles button clicks 
        for event in pygame.event.get():
            #exit the loop and close the screen in player quits
            if event.type == pygame.QUIT:
                write_high_score(high_score, score)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button[3].collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(sounds.click)
                    paused = not paused
                    if paused:
                        pause_message = "Resume"
                        pause_color = "#f77a5e"
                    else:
                        pause_message = "Pause"
                        pause_color = "#f2461f"
                if restart_button[3].collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(sounds.click)
                    pygame.mixer.music.play(-1)
                    game_over_sound = False
                    #runs the game again and resets all the variables
                    write_high_score(high_score, score)
                    with open("saved_states/high_score.txt", "r") as file:
                        high_score = file.readline().strip()
                    level = 0
                    score = 0

                    props = []
                    prop_num = 5
                    prop_speed = 1
                    player_speed = 7
                    player.lives = 5

                    lost_status = False
                    pause_message = "Pause"
                    pause_color = "#f2461f"
                    paused = False
                    #once the variables are reset, the game loop continues in the same window

                if quit_button[3].collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(sounds.click)
                    #quits the game
                    write_high_score(high_score, score)
                    running = False

        #skips all the movement while the game is paused or character has lost
        if paused == True:
            continue
        
        if lost_status == True:
            continue
  
        #handles key presses to move the player
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] == True and player.xPos + player.sprite_img.get_width() <= screen_info.current_w:
            player.move_x(player_speed)
        if pressed[pygame.K_LEFT] == True and player.xPos >= 0:
            player.move_x(-player_speed)
        if pressed[pygame.K_UP] == True and player.yPos >= 0:
            player.move_y(-player_speed)
        if pressed[pygame.K_DOWN] == True and player.yPos + player.sprite_img.get_height() + 50 <= screen_info.current_h: 
            player.move_y(player_speed)

        #moves the props, handles score, deletes prop if it reaches bottom or collides with player
        for prop in props:
            prop.move_y(prop_speed)
            if prop.yPos + 100 > screen_info.current_h:
                pygame.mixer.Sound.play(sounds.prop_drop)
                player.lives -= 1
                score -= 125
                props.remove(prop)
            # if collision, remove prop from screen
            if player.collide(player, prop):
                pygame.mixer.Sound.play(sounds.collide_prop)
                props.remove(prop)
                # if collision with bonus prop
                if prop.sprite_img_path == bonus_prop:  
                    pygame.mixer.Sound.play(sounds.bonus_prop)
                    score += 115
                    # sets 5 second timer
                    player_size_timer = pygame.time.get_ticks() + 6000
                    # grow triple player size
                    player.sprite_img = pygame.transform.scale(player.sprite_img, (player_original_size[0] * 3, player_original_size[1] * 3))
                    player.mask = pygame.mask.from_surface(player.sprite_img)
                else:
                    score += 100

        # Check if it's time to revert player size
        if player_size_timer and pygame.time.get_ticks() > player_size_timer:
            player.sprite_img = pygame.transform.scale(player.sprite_img, player_original_size)
            player.mask = pygame.mask.from_surface(player.sprite_img)
            player_size_timer = None

    #game is done
    return "Done"

#sets the background and draws all text and buttons based on the status of the game
def set_background(level, player, props, lost_status, score, pause_button, restart_button, quit_button, paused, high_score):
    global game_over_sound
    #draw background to screen
    screen.blit(background, (0,0)) 

    #displays text on top right corner
    levels_text = font.render(f"Level: {level}", True, "black")
    lives_text = font.render(f"Lives: {player.lives}", True, "black")
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = smaller_font.render(f"High Score: {high_score}", True, "black")
    screen.blit(levels_text, (screen_info.current_w - 215, 10))
    screen.blit(lives_text, (screen_info.current_w - 215, 50))
    screen.blit(score_text, (screen_info.current_w - 215, 90))
    screen.blit(high_score_text, (120, 10))

    #display pause/resume button on top left corner
    pause_button[0].blit(pause_button[1], pause_button[2])
    screen.blit(pause_button[0], (pause_button[3].x, pause_button[3].y))

    #Display high score on top left corner


    #draw the players and props
    player.draw(screen)
    for prop in props:
        prop.draw(screen)

    #display pause, restart, quit buttons if game is paused
    if paused:
        pause_msg = button_creation(60, "PAUSED", screen_info.current_w/2 - 15, screen_info.current_h/2, 350, 150, "#f2461f")
        pause_msg[0].blit(pause_msg[1],pause_msg[2])
        screen.blit(pause_msg[0], (pause_msg[3].x - 150, pause_msg[3].y - 150))
        restart_button[0].blit(restart_button[1], restart_button[2])
        screen.blit(restart_button[0], (restart_button[3].x, restart_button[3].y))
        quit_button[0].blit(quit_button[1], quit_button[2])
        screen.blit(quit_button[0], (quit_button[3].x, quit_button[3].y))

    #display lost message, restart, and quit buttons if you lost
    if lost_status == True:
        pygame.mixer.music.stop()
        if game_over_sound == False:
            pygame.mixer.Sound.play(sounds.game_over)
            game_over_sound = True
        lost_button = button_creation(60, "You Lost", screen_info.current_w/2 - 15, screen_info.current_h/2, 350, 150, "#f2461f")
        lost_button[0].blit(lost_button[1],lost_button[2])
        screen.blit(lost_button[0], (lost_button[3].x - 150, lost_button[3].y - 150))
        restart_button[0].blit(restart_button[1], restart_button[2])
        screen.blit(restart_button[0], (restart_button[3].x, restart_button[3].y))
        quit_button[0].blit(quit_button[1], quit_button[2])
        screen.blit(quit_button[0], (quit_button[3].x, quit_button[3].y))

    pygame.display.update()