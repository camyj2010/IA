import pygame, sys, os
from pygame_gui.elements.ui_label import UILabel
import pygame_gui
from pygame.locals import *
from button import Button
from dropdown import DropDown

import tkinter as tk
from tkinter import filedialog, messagebox

pygame.init()

#Load resource
SCREEN = pygame.display.set_mode((1280,720))
BG=pygame.image.load("source\imagenes\original.jpg")
dragon=pygame.transform.scale(pygame.image.load("source\imagenes\dragon_resize.png"), (int(250), int(200)))
ball=pygame.transform.scale(pygame.image.load("source\imagenes\dragon_ball.png"), (int(62), int(62)))
sound = pygame.mixer.Sound("source\sounds\menu.ogg")
sound.set_volume(0.1)
width=1200
height=700
window_=pygame.display.set_mode((width,height))

def get_font(size, number): # Returns Press-Start-2P in the desired size
    if(number==1):
        return pygame.font.Font("source\saiyan-sans_font\Saiyan-Sans.ttf", size)
    if(number==2):
        return pygame.font.Font("source\saiyan-sans_font\ChicagoFLF.ttf", size)




def play():
    sound.stop()
   
    COLOR_INACTIVE = (135, 206, 235)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (135, 206, 235)
    COLOR_LIST_ACTIVE = (255, 150, 150)
    
    file_names = [f for f in os.listdir("source\map") if f.endswith(".txt")]
    DROPDOWN = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 80, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Map", file_names)

    DROPDOWN_SEARCH = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 160, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Search", ["Informada", "No Informada"])
    
    DROPDOWN_ALG = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 240, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Algorithm", ["None", "None"])
    
    INFORMADA = ['Avara', 'A*']
    NO_INFORMADA = ['Amplitud', 'Costo Uniforme', 'Profundidad']

    while True:
    

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0)) 

        PLAY_TEXT = get_font(38,2).render("Maps:", True, "White")
        PLAY_TEXT2 = get_font(38,2).render("Search:", True, "White")
        PLAY_TEXT3 = get_font(38,2).render("Algoritm:", True, "White")
        PLAY_TEXT4 = get_font(32,2).render("Expanded nodes:", True, "White")
        PLAY_TEXT5 = get_font(32,2).render("Tree depth:", True, "White")
        PLAY_TEXT6 = get_font(32,2).render("Computing time:", True, "White")
        PLAY_TEXT7 = get_font(32,2).render("Solution cost:", True, "White")
        PLAY_TEXT8 = get_font(38,2).render("REPORT", True, "White")

        #RECT=pygame.draw.rect(window_,"White",(80,50,620,620) )
        #RECT_2=pygame.draw.rect(window_,"White",(750,50,350,530) )

        PLAY_RECT = PLAY_TEXT.get_rect(center=(815, 100))
        PLAY_RECT2 = PLAY_TEXT.get_rect(center=(815, 180))
        PLAY_RECT3 = PLAY_TEXT.get_rect(center=(815, 260))
        PLAY_RECT4 = PLAY_TEXT.get_rect(center=(815, 400))
        PLAY_RECT5 = PLAY_TEXT.get_rect(center=(815, 450))
        PLAY_RECT6 = PLAY_TEXT.get_rect(center=(815, 500))
        PLAY_RECT7 = PLAY_TEXT.get_rect(center=(815, 550))
        PLAY_RECT8 = PLAY_TEXT.get_rect(center=(950, 350))

        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        SCREEN.blit(PLAY_TEXT2, PLAY_RECT2)
        SCREEN.blit(PLAY_TEXT3, PLAY_RECT3)
        SCREEN.blit(PLAY_TEXT4, PLAY_RECT4)
        SCREEN.blit(PLAY_TEXT5, PLAY_RECT5)
        SCREEN.blit(PLAY_TEXT6, PLAY_RECT6)
        SCREEN.blit(PLAY_TEXT7, PLAY_RECT7)
        SCREEN.blit(PLAY_TEXT8, PLAY_RECT8)
        

        PLAY_BACK = Button(pygame.transform.scale(pygame.image.load("source\imagenes\Play_Rect_3.png"), (int(200), int(150))), pos=(990, 650), 
                            text_input="BACK", font=get_font(40,1), base_color="#FFFFFF", hovering_color="#87CEEB")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        DROPDOWN_ALG.draw(SCREEN)
        DROPDOWN_SEARCH.draw(SCREEN)
        DROPDOWN.draw(SCREEN)

        

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            
        selected_option = DROPDOWN.update(event_list)
        if selected_option >= 0:
            DROPDOWN.main = DROPDOWN.options[selected_option]

        selected_search = DROPDOWN_SEARCH.update(event_list)
        if selected_search >= 0:
            DROPDOWN_SEARCH.main = DROPDOWN_SEARCH.options[selected_search]
            if selected_search == 0:
                DROPDOWN_ALG.update_options(INFORMADA)
            elif selected_search == 1:
                DROPDOWN_ALG.update_options(NO_INFORMADA)

        selected_alg = DROPDOWN_ALG.update(event_list)
        if selected_alg >= 0:
            DROPDOWN_ALG.main = DROPDOWN_ALG.options[selected_alg]

        mapa=[[1,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [0,0,0,6,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,6,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0,0]]
        
        CELL_WIDTH = 620 // len(mapa[0])
        CELL_HEIGHT = 620 // len(mapa)
        for y, row in enumerate(mapa):
            for x, cell in enumerate(row):
                POS_X = x*CELL_WIDTH
                POS_Y = y*CELL_HEIGHT
                rect = pygame.Rect(POS_X+80, POS_Y+50, CELL_WIDTH, CELL_HEIGHT)
                #pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1) # Dibuja el borde negro
                if cell==0: 
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro blanco
                elif cell == 1:
                    pygame.draw.rect(SCREEN, (0, 0, 0), rect) # Dibuja el cuadro piedra
                    #screen.blit(imagenP, (x * CELL_WIDTH, y * CELL_HEIGHT))
                elif cell == 2:
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro queso
                    #SCREEN.blit(RECT, (x * CELL_WIDTH, y * CELL_HEIGHT))
                elif cell == 3:
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro del raton
                    #SCREEN.blit(RECT, (x * CELL_WIDTH, y * CELL_HEIGHT))
                elif cell == 4:
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro del raton
                    #SCREEN.blit(RECT, (x * CELL_WIDTH, y * CELL_HEIGHT))
                elif cell == 5:
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro del raton
                    #SCREEN.blit(RECT, (x * CELL_WIDTH, y * CELL_HEIGHT))
                elif cell == 6: 
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el cuadro blanco
                    SCREEN.blit(ball, (POS_X+80, POS_Y+50))
                
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1) # Dibuja el borde negro


        pygame.display.update()

def credits():
    sound.stop()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0)) 

        CREDIT_TEXT = get_font(150,1).render("CREDITS.", True, "White")
        OPTIONS_RECT = CREDIT_TEXT.get_rect(center=(640, 120))
        SCREEN.blit(CREDIT_TEXT, OPTIONS_RECT)

        NAMES_TEXT = get_font(80,1).render("nombres", True, "White")
        NAMES_RECT = NAMES_TEXT.get_rect(center=(645, 300))
        SCREEN.blit(NAMES_TEXT, NAMES_RECT)

        OPTIONS_BACK = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(900, 600), 
                            text_input="BACK", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")

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

def maps():
    sound.stop()

    def upload_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(f"File path: {file_path}")
        messagebox.showinfo("","upload successful")


        with open("source/map/" + os.path.basename(file_path), "wb") as f:
            with open(file_path, "rb") as input_file:
                f.write(input_file.read())

    

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0)) 

        UPLOAD_TEXT = get_font(150,1).render("UPLOAD YOUR MAP", True, "White")
        OPTIONS_RECT = UPLOAD_TEXT.get_rect(center=(640, 120))
        SCREEN.blit(UPLOAD_TEXT, OPTIONS_RECT)
        #####
        BUTTON_UP = Button(pygame.transform.scale(pygame.image.load("source\imagenes\_button_up.png"), (int(550), int(150))), pos=(600, 350), 
                            text_input="UPLOAD A NEW MAP", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")
        BUTTON_UP.onclick = upload_file

        BUTTON_UP.changeColor(OPTIONS_MOUSE_POS)
        BUTTON_UP.update(SCREEN)
        
        OPTIONS_BACK = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(900, 600), 
                            text_input="BACK", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if BUTTON_UP.rect.collidepoint(event.pos):
                    BUTTON_UP.onclick()

       
        pygame.display.update()
        

def main_menu():
     
     #sound.play()  
     while True:
      
        SCREEN.blit(BG, (0, 0)) 

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(150,1).render("Dragon Ball Maze", True, "#FFFFFF")
        
        
        MENU_RECT = MENU_TEXT.get_rect(center=(700, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(250, 600), 
                            text_input="PLAY", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        CREDIT_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(1000, 600), 
                            text_input="CREDITS", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        MAPS_BUTTON = Button(image=pygame.image.load("source\imagenes\Play_Rect_3.png"), pos=(628, 600), 
                            text_input="MAP", font=get_font(60,1), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(dragon, (5,30))

        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for button in [CREDIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for button in [MAPS_BUTTON]:
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
                if MAPS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    maps()

        pygame.display.update()
 


main_menu()


