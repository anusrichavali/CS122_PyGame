import pygame
pygame.init()

screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill((73, 104, 65))
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

font = pygame.font.Font("Grand9KPixel.ttf", 60)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    text = font.render("SpartanDash: Campus Run", True, (255, 255, 255))
    screen.blit(text, ((screen_info.current_w / 2 - text.get_width() / 2), 200))
    pygame.display.update()
