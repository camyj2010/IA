import pygame, sys 
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280,720))
BG=pygame.image.load("source\imagenes\original.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("source\saiyan-sans_font\Saiyan-Sans.ttf", size)

def play(): 
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

def main_menu():
     
     while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(150).render("Dragon Ball Maze", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(300, 600), 
                            text_input="PLAY", font=get_font(60), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        CREDIT_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(900, 600), 
                            text_input="CREDITS", font=get_font(60), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

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
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
 


main_menu()


