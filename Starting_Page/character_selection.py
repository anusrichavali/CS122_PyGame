import pygame
pygame.init()

def selectButtons(text, font, x, y):
    choose_char = pygame.Surface((200,50))
    choose_char.fill("#f2461f")
    char_text = font.render(text, True, "#ebfbfc")
    char_text_rect = char_text.get_rect(center=(choose_char.get_width()/2, choose_char.get_height()/2))
    button_rect = pygame.Rect(x, y, 150, 50)
    return [choose_char, char_text, char_text_rect, x, y]


screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill("#32a0a8")
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

title_font = pygame.font.Font("Grand9KPixel.ttf", 60)
subtitle_font = pygame.font.Font("Grand9KPixel.ttf", 40)
button_font = pygame.font.Font("Grand9KPixel.ttf", 25)

choose_neha = selectButtons("Choose Neha", button_font, (screen_info.current_w/3 - 100), 2 * (screen_info.current_h/3))
choose_anusri = selectButtons("Choose Anusri", button_font, 2* (screen_info.current_w/3) - 100, 2 * (screen_info.current_h/3))

DEFAULT_SIZE = (300, 300)
anusri_img = pygame.image.load("sprite_images/Anusri_Sprite.png")
anusri_img = pygame.transform.scale(anusri_img, DEFAULT_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    title = title_font.render("SpartanDash: Campus Run", True, "#FFD700")
    screen.blit(title, ((screen_info.current_w / 2 - title.get_width() / 2), 50))
    instruction = subtitle_font.render("Choose your character.", True, "#ebfbfc")
    screen.blit(instruction, ((screen_info.current_w/2 - instruction.get_width()/2), 150))
    choose_neha[0].blit(choose_neha[1], choose_neha[2])
    choose_anusri[0].blit(choose_anusri[1], choose_anusri[2])

    # Draw the button on the screen
    screen.blit(choose_neha[0], (choose_neha[3], choose_neha[4]))
    screen.blit(choose_anusri[0], (choose_anusri[3], choose_anusri[4]))
    screen.blit(anusri_img, (choose_anusri[3] - 50, choose_anusri[4] - anusri_img.get_height() - 50))
    pygame.display.update()
