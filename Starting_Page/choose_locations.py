import pygame
pygame.init()

#input: the button's text, x coordinate, y coordinate
#returns the list of the 4 components that need to be separately blit on the screen to create a button
#returns button surface, button text, text rectangle, and button rectangle
def button_creation(text, x, y):
    font = pygame.font.Font("resources/Grand9KPixel.ttf", 25)
    choose_loc = pygame.Surface((200,50))
    choose_loc.fill("#f2461f")
    loc_text = font.render(text, True, "#ebfbfc")
    loc_text_rect = loc_text.get_rect(center=(choose_loc.get_width()/2, choose_loc.get_height()/2))
    button_rect = pygame.Rect(x, y, 200, 50)
    return [choose_loc, loc_text, loc_text_rect, button_rect]

#create the screen and configure the screen size, background color, and caption
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill("#32a0a8")
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

#load custom font from ttf file and set size for different types of text
title_font = pygame.font.Font("resources/Grand9KPixel.ttf", 60)
subtitle_font = pygame.font.Font("resources/Grand9KPixel.ttf", 40)

segment_width = screen_info.current_w/4 #number of buttons + one segment
#use button_creation function to create selecot buttons for both characters and next button
choose_srac = button_creation("Choose SRAC", (segment_width - 150/2), 2 * (screen_info.current_h/3))
choose_su = button_creation("Choose SU", 2 * segment_width - 150/2, 2 * (screen_info.current_h/3))
choose_mlk = button_creation("Choose MLK", 3 * segment_width - 150/2, 2 * (screen_info.current_h/3))
start_button = button_creation("Start", screen_info.current_w - 300, screen_info.current_h - 200)

#load sprite images and resize them
DEFAULT_SIZE = (350, 245)
temp_img = pygame.image.load("resources/tower_lawn.png")
temp_img = pygame.transform.scale(temp_img, DEFAULT_SIZE)

#initialize variables before running the choose_locations page
def run():
    running = True
    location_selected = ""
    #whie the page is running
    while running:
        #register interactions with the screen
        for event in pygame.event.get():
            #exit the loop and close the screen in player quits
            if event.type == pygame.QUIT:
                running = False
            #if player clicks on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                #store "srac" as selected location and configure button colors to show selection
                if choose_srac[3].collidepoint(mouse_position):
                    choose_srac[0].fill("#f77a5e")
                    choose_su[0].fill("#f2461f")
                    choose_mlk[0].fill("#f2461f")
                    location_selected = "SRAC"
                    print("SRAC")
                #store "su" as selected location and configure button colors to show selection
                elif choose_su[3].collidepoint(mouse_position):
                    choose_su[0].fill("#f77a5e")
                    choose_srac[0].fill("#f2461f")
                    choose_mlk[0].fill("#f2461f")
                    location_selected = "SU"
                    print("Student Union")
                #store "mlk" as selected location and configure button colors to show selection
                elif choose_mlk[3].collidepoint(mouse_position):
                    choose_mlk[0].fill("#f77a5e")
                    choose_su[0].fill("#f2461f")
                    choose_srac[0].fill("#f2461f")
                    location_selected = "MLK"
                    print("MLK")
                #create or open the existing "selected_location.txt" file and write the finally selected character to the file
                #move to the next page
                elif start_button[3].collidepoint(mouse_position) and location_selected != "":
                    start_button[0].fill("#f77a5e")
                    with open("selected_location.txt", "w") as file:
                        file.write(location_selected)
                    running = False
        
        #while the program is running, display the title and subtitle on the screen
        title = title_font.render("SpartanDash: Campus Run", True, "#FFD700")
        screen.blit(title, ((screen_info.current_w / 2 - title.get_width() / 2), 50))
        instruction = subtitle_font.render("Choose your location.", True, "#ebfbfc")
        screen.blit(instruction, ((screen_info.current_w/2 - instruction.get_width()/2), 150))

        # while the program is running, display the Select Location buttons
        choose_srac[0].blit(choose_srac[1], choose_srac[2])
        choose_su[0].blit(choose_su[1], choose_su[2])
        choose_mlk[0].blit(choose_mlk[1], choose_mlk[2])
        screen.blit(choose_srac[0], (choose_srac[3].x, choose_srac[3].y))
        screen.blit(choose_su[0], (choose_su[3].x, choose_su[3].y))
        screen.blit(choose_mlk[0], (choose_mlk[3].x, choose_mlk[3].y))

        #while the program is running, display the location images on the screen
        screen.blit(temp_img, (choose_srac[3].x - 50, choose_srac[3].y - temp_img.get_height() - 50))
        screen.blit(temp_img, (choose_su[3].x - 50, choose_su[3].y - temp_img.get_height() - 50))
        screen.blit(temp_img, (choose_mlk[3].x - 50, choose_mlk[3].y - temp_img.get_height() - 50))


        #screen.blit(background_img, (0, screen_info.current_h/2))

        #display the next button only after one of the location has been selected
        if location_selected != "":
            start_button[0].blit(start_button[1], start_button[2])
            screen.blit(start_button[0], (start_button[3].x, start_button[3].y))

        #update all the changes while the screen is running
        pygame.display.update()
