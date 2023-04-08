import pygame, sys 
from button import Button

pygame.init()

#Load resource
SCREEN = pygame.display.set_mode((1280,720))
BG=pygame.image.load("source\imagenes\original.jpg")
dragon=pygame.transform.scale(pygame.image.load("source\imagenes\dragon_resize.png"), (int(250), int(200)))
ball=pygame.image.load("source\imagenes\dragon_ball.png")
sound = pygame.mixer.Sound("source\sounds\menu.ogg")
sound.set_volume(0.1)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("source\saiyan-sans_font\Saiyan-Sans.ttf", size)

def play():
    sound.stop()
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def credits():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0)) 

        CREDIT_TEXT = get_font(150).render("CREDITS.", True, "White")
        OPTIONS_RECT = CREDIT_TEXT.get_rect(center=(640, 120))
        SCREEN.blit(CREDIT_TEXT, OPTIONS_RECT)

        NAMES_TEXT = get_font(80).render("Valery Molina \n \n Camila Jaramillo ", True, "White")
        NAMES_RECT = NAMES_TEXT.get_rect(center=(645, 300))
        SCREEN.blit(NAMES_TEXT, NAMES_RECT)

        OPTIONS_BACK = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(900, 600), 
                            text_input="BACK", font=get_font(60), base_color="#FFFFFF", hovering_color="#87CEEB")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
     
     sound.play()  
     while True:
        SCREEN.blit(BG, (0, 0)) 

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(150).render("Dragon Ball Maze", True, "#FFFFFF")
        
        
        MENU_RECT = MENU_TEXT.get_rect(center=(700, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(350, 600), 
                            text_input="PLAY", font=get_font(60), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        CREDIT_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(900, 600), 
                            text_input="CREDITS", font=get_font(60), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(dragon, (5,30))

        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for button in [CREDIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
 


main_menu()


