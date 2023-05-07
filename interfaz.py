import pygame, sys, os
#from pygame_gui.elements.ui_label import UILabel
import pygame_gui
from pygame.locals import *
from button import Button
from dropdown import DropDown
import spritesheet
import time

import tkinter as tk
from tkinter import filedialog, messagebox
from bni_Depth_Search import Depth_Search
from bni_Breadth_Search import Breadth_Search
from bni_Uniform_Cost_Search import Uniform_Cost_Search
from bi_Greedy_Search import Greedy_Search
from bi_A_Star_Search import A_Star_Search
pygame.init()

#Load resource
SCREEN = pygame.display.set_mode((1280,720))
BG=pygame.image.load("source\imagenes\original.jpg")
dragon=pygame.transform.scale(pygame.image.load("source\imagenes\dragon_resize.png"), (int(250), int(200)))
ball=pygame.transform.scale(pygame.image.load("source\imagenes\dragon_ball.png"), (int(62), int(62)))

sound_mixer = pygame.mixer.Channel(5)
sound = pygame.mixer.Sound("source\sounds\menu.ogg")
sound.set_volume(0.1)

sound2 = pygame.mixer.music
sound2.load("source\sounds\play.mp3")
sound2.set_volume(0.1)

width=1200
height=700
window_=pygame.display.set_mode((width,height))

#Frieza sprite
sprite_sheet_image = pygame.image.load("source/imagenes/frieza.png")
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
animation_frames = []
animation_steps = 4
for i in range(animation_steps):
    frame = sprite_sheet.get_image(i, 45, 45, 1.2, (255, 255, 255))
    animation_frames.append(frame)

#Cell sprite
cell_sprite_sheet_image = pygame.image.load("source/imagenes/cell.png")
cell_sprite_sheet = spritesheet.SpriteSheet(cell_sprite_sheet_image)
cell_animation_frames = []
cell_animation_steps = 4
for i in range(cell_animation_steps):
    cell_frame = cell_sprite_sheet.get_image(i, 40, 65, 1, (255, 255, 255))
    cell_animation_frames.append(cell_frame)

# Goku sprite
goku_sprite_sheet_image = pygame.image.load("source/imagenes/goku.png")
goku_sprite_sheet = spritesheet.SpriteSheet(goku_sprite_sheet_image)
goku_animation_frames = []
goku_animation_steps = 5
for i in range(goku_animation_steps):
    goku_frame = goku_sprite_sheet.get_image(i, 62, 62, 1, (255, 255, 255))
    goku_animation_frames.append(goku_frame)

# Obstaculos
obstacle = pygame.transform.scale(
    pygame.image.load("source\imagenes\obstacle.png"), (int(62), int(62))
)

# Semilla
bean = pygame.transform.scale(
    pygame.image.load("source\imagenes\seed.png"), (int(62), int(62))
)

# Cloud
cloud = pygame.transform.scale(
    pygame.image.load("source\imagenes/nube.png"), (int(62), int(62))
)

def get_font(size, number): # Returns Press-Start-2P in the desired size
    if(number==1):
        return pygame.font.Font("source\saiyan-sans_font\Saiyan-Sans.ttf", size)
    if(number==2):
        return pygame.font.Font("source\saiyan-sans_font\ChicagoFLF.ttf", size)

def read_map(file_name):
    map = []
    with open("source\map\{}".format(file_name), "r") as file:
        for line in file:
            str = line.strip().split(" ")
            str = [int(i) for i in str]
            map.append(str)
    return map

map=[
[0, 5, 3, 1, 1, 1, 1, 1, 1, 1],
[0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
[0, 1, 1, 0, 3, 5, 1, 0, 2, 0],
[0, 1, 1, 1, 3, 1, 1, 1, 1, 0],
[6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 4, 1, 1, 1, 1, 1, 1, 0],
[1, 1, 0, 4, 4, 0, 0, 1, 1, 5],
[1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
[0, 0, 0, 0, 1, 1, 5, 0, 0, 0],
[1, 1, 1, 0, 1, 1, 6, 1, 1, 1]]

def play():
    # sound.stop()
    # sound.play()
    #Animation variables
    frame = 0
    cell_frame = 0
    frame_rate = 3
    last_update = pygame.time.get_ticks()
   
    COLOR_INACTIVE = (135, 206, 235)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (135, 206, 235)
    COLOR_LIST_ACTIVE = (255, 150, 150)
    
    file_names = [f for f in os.listdir("source\map") if f.endswith(".txt")]
    DROPDOWN = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 50, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Map", file_names)

    DROPDOWN_SEARCH = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 130, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Search", ["Informada", "No Informada"])
    
    DROPDOWN_ALG = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        950, 210, 200, 50, 
        pygame.font.SysFont(None, 30), 
        "Select Algorithm", ["None", "None"])
    
    INFORMADA = ['Avara', 'A*']
    NO_INFORMADA = ['Amplitud', 'Costo Uniforme', 'Profundidad']

    map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    

    solution = []
    maps = []
    traveled = []

    enlapsed_time = ""
    tree_depth = ""
    expanded_nodes = ""
    total_cost = ""
    count = 0

    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0)) 

        PLAY_TEXT = get_font(38,2).render("Maps:", True, "White")
        PLAY_TEXT2 = get_font(38,2).render("Search:", True, "White")
        PLAY_TEXT3 = get_font(38,2).render("Algoritm:", True, "White")
        PLAY_TEXT4 = get_font(29,2).render("Expanded nodes:", True, "White")
        PLAY_TEXT5 = get_font(29,2).render("Tree depth:", True, "White")
        PLAY_TEXT6 = get_font(29,2).render("Computing time:", True, "White")
        PLAY_TEXT7 = get_font(29,2).render("Solution cost:", True, "White")
        PLAY_TEXT8 = get_font(38,2).render("REPORT", True, "White")
        PLAY_TEXT9 = get_font(29,2).render(enlapsed_time, True, "White")
        PLAY_TEXT10 = get_font(29,2).render(expanded_nodes, True, "White")
        PLAY_TEXT11 = get_font(29,2).render(tree_depth, True, "White")
        PLAY_TEXT12 = get_font(29,2).render(total_cost, True, "White")
        #RECT=pygame.draw.rect(window_,"White",(80,50,620,620) )
        #RECT_2=pygame.draw.rect(window_,"White",(750,50,350,530) )

        PLAY_RECT = PLAY_TEXT.get_rect(center=(815, 70))
        PLAY_RECT2 = PLAY_TEXT.get_rect(center=(815, 150))
        PLAY_RECT3 = PLAY_TEXT.get_rect(center=(815, 230))
        PLAY_RECT4 = PLAY_TEXT.get_rect(center=(815, 430))
        PLAY_RECT5 = PLAY_TEXT.get_rect(center=(815, 480))
        PLAY_RECT6 = PLAY_TEXT.get_rect(center=(815, 530))
        PLAY_RECT7 = PLAY_TEXT.get_rect(center=(815, 580))
        PLAY_RECT8 = PLAY_TEXT.get_rect(center=(950, 380))
        PLAY_RECT9 = PLAY_TEXT.get_rect(center=(1090, 532))
        PLAY_RECT10 = PLAY_TEXT.get_rect(center=(1090, 432))
        PLAY_RECT11 = PLAY_TEXT.get_rect(center=(1090, 482))
        PLAY_RECT12 = PLAY_TEXT.get_rect(center=(1090, 582))

        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        SCREEN.blit(PLAY_TEXT2, PLAY_RECT2)
        SCREEN.blit(PLAY_TEXT3, PLAY_RECT3)
        SCREEN.blit(PLAY_TEXT4, PLAY_RECT4)
        SCREEN.blit(PLAY_TEXT5, PLAY_RECT5)
        SCREEN.blit(PLAY_TEXT6, PLAY_RECT6)
        SCREEN.blit(PLAY_TEXT7, PLAY_RECT7)
        SCREEN.blit(PLAY_TEXT8, PLAY_RECT8)
        SCREEN.blit(PLAY_TEXT9, PLAY_RECT9)
        SCREEN.blit(PLAY_TEXT10, PLAY_RECT10)
        SCREEN.blit(PLAY_TEXT11, PLAY_RECT11)
        SCREEN.blit(PLAY_TEXT12, PLAY_RECT12)


        PLAY_BACK = Button(pygame.transform.scale(pygame.image.load("source\imagenes\Play_Rect_4.png"), (int(200), int(150))), pos=(1090, 650), 
                            text_input="BACK", font=get_font(40,1), base_color="#FFFFFF", hovering_color="#87CEEB")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        PLAY_SOLVE = Button(pygame.transform.scale(pygame.image.load("source\imagenes\Play_Rect_3.png"), (int(200), int(150))), pos=(900, 310), 
                            text_input="SOLVE", font=get_font(40,1), base_color="#FFFFFF", hovering_color="#87CEEB")

        PLAY_SOLVE.changeColor(PLAY_MOUSE_POS)
        PLAY_SOLVE.update(SCREEN)

        PLAY_RESTART = Button(pygame.transform.scale(pygame.image.load("source/imagenes/restart.png"), (int(180), int(170))), pos=(1100, 313), 
                             text_input="", font=get_font(32,1), base_color="#FFFFFF", hovering_color="#87CEEB")

        PLAY_RESTART.changeColor(PLAY_MOUSE_POS)
        PLAY_RESTART.update(SCREEN)
        
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
                if PLAY_SOLVE.checkForInput(PLAY_MOUSE_POS):
                    
                    #sound_mixer.play(sound2)
                    if DROPDOWN_ALG.main == "Amplitud" and count==0:
                        print('Amplitud')
                        start=time.time()
                        path, nodes, maps, cost = Breadth_Search(map).solve()
                        print("Path: ", path)
                        print("Nodos expandidos: ", nodes)
                        finish=time.time()
                        total_time = finish-start
                        print(total_time)
                        ##PLAY_TEXT9 = get_font(38,2).render(str(total_time), True, "White")
                        enlapsed_time = str(round(total_time, 4)) + " s"
                        expanded_nodes = str(nodes)
                        tree_depth=str(len(path))
                        total_cost=str(cost)
                        count += 1

                        solution += path

                    elif DROPDOWN_ALG.main == "Costo Uniforme" and count==0:
                        print('Costo Uniforme')
                        start=time.time()
                        path, nodes, maps, cost = Uniform_Cost_Search(map).solve()
                        print("Path: ", path)
                        print("Nodos expandidos: ", nodes)
                        print("Costo", cost)
                        finish=time.time()
                        total_time = finish-start
                        print(total_time)
                        enlapsed_time = str(round(total_time, 4)) + " s"
                        expanded_nodes = str(nodes)
                        tree_depth=str(len(path))
                        total_cost=str(cost)
                        count += 1

                        solution += path
                        
                    elif DROPDOWN_ALG.main == "Profundidad" and count==0:
                        print('Profundidad')
                        start=time.time()
                        path, nodes, maps, cost = Depth_Search(map).solve()
                        print("Path: ", path)
                        print("Nodos expandidos: ", nodes)
                        finish=time.time()
                        total_time = finish-start
                        print(total_time)
                        enlapsed_time = str(round(total_time, 4)) + " s"
                        expanded_nodes = str(nodes)
                        tree_depth=str(len(path))
                        total_cost=str(cost)
                        count += 1

                        solution += path
                        
                    elif DROPDOWN_ALG.main == "A*" and count==0:
                        print('A*')
                        start=time.time()
                        path, nodes, maps, cost = A_Star_Search(map).solve()
                        print("Path: ", path)
                        print("Nodos expandidos: ", nodes)
                        print("Costo", cost)
                        finish=time.time()
                        total_time = finish-start
                        print(total_time)
                        enlapsed_time = str(round(total_time, 4)) + " s"
                        expanded_nodes = str(nodes)
                        tree_depth=str(len(path))
                        total_cost=str(cost)
                        count += 1

                        solution += path

                    elif DROPDOWN_ALG.main == "Avara" and count==0:
                        print('Avara')
                        start=time.time()
                        path, nodes, maps, cost = Greedy_Search(map).solve()
                        print("Path: ", path)
                        print("Nodos expandidos: ", nodes)
                        print("Costo", cost)
                        finish=time.time()
                        total_time = finish-start
                        print(total_time)
                        enlapsed_time = str(round(total_time, 4)) + " s"
                        expanded_nodes = str(nodes)
                        tree_depth=str(len(path))
                        total_cost=str(cost)
                        count += 1

                        solution += path
                        
                    if len(solution) > 0 and count == 1:
                        count += 1
                        sound_mixer.stop()
                        sound2.play(start=10.1)

                if PLAY_RESTART.checkForInput(PLAY_MOUSE_POS):
                    
                    if DROPDOWN.main != 'Select Map':
                        solution = []
                        traveled = []
                        enlapsed_time = ""
                        tree_depth = ""
                        expanded_nodes = ""
                        total_cost = ""
                        count = 0
                        map = read_map(DROPDOWN.main)

            
        selected_option = DROPDOWN.update(event_list)
        if selected_option >= 0:
            DROPDOWN.main = DROPDOWN.options[selected_option]
            map = read_map(DROPDOWN.main)
            count = 0

        selected_search = DROPDOWN_SEARCH.update(event_list)
        if selected_search >= 0:
            DROPDOWN_SEARCH.main = DROPDOWN_SEARCH.options[selected_search]
            if selected_search == 0:
                DROPDOWN_ALG.update_options(INFORMADA)
                
            elif selected_search == 1:
                DROPDOWN_ALG.update_options(NO_INFORMADA)

        selected_alg = DROPDOWN_ALG.update(event_list)
        if selected_alg >= 0:
            count=0
            DROPDOWN_ALG.main = DROPDOWN_ALG.options[selected_alg]
       
        

            

        if len(solution) > 0:
            pos = solution[0]
            
            map = maps[0]

            for i in range(len(map)):
                for j in range(len(map)):
                    if map[i][j] == 2:
                        map[i][j] = 0
            
            #print(pos)
            map[pos[0]][pos[1]] = 2
            
            # print(map)
            # print()
            time.sleep(0.3)

            for tile in traveled:
                if map[tile[0]][tile[1]] == 0:
                    map[tile[0]][tile[1]] = 7

            traveled.append(pos)
            solution = solution[1:]

            maps = maps[1:]
        
        else:
            if sound2.get_busy():
                sound2.fadeout(1500)
                #sound_mixer.play(sound)
            elif sound_mixer.get_sound() == None:
                sound_mixer.play(sound)
            

  
        #update the animation frames
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= 1000 // frame_rate:
            last_update = current_time
            frame = (frame + 1) % len(animation_frames)
            cell_frame = (cell_frame + 1) % len(cell_animation_frames)
        
        CELL_WIDTH = 620 // len(map[0])
        CELL_HEIGHT = 620 // len(map)
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                POS_X = x*CELL_WIDTH
                POS_Y = y*CELL_HEIGHT
                rect = pygame.Rect(POS_X+80, POS_Y+50, CELL_WIDTH, CELL_HEIGHT)
                if cell == 0: #casilla libre
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect) # Dibuja el cuadro blanco

                elif cell == 1: #muro
                    pygame.draw.rect(SCREEN, (255, 255, 255), rect) # Dibuja el muro
                    SCREEN.blit(obstacle, (POS_X + 80, POS_Y + 50))

                elif cell == 2: #goku
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect)
                    SCREEN.blit(
                        goku_animation_frames[cell_frame], (POS_X + 80, POS_Y + 50)
                    )

                elif cell == 3: #freezer
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect) # Anima a freezer
                    SCREEN.blit(animation_frames[frame], (POS_X+85, POS_Y+55))

                elif cell == 4: #cell
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect) # Anima a cell
                    SCREEN.blit(cell_animation_frames[cell_frame], (POS_X+85, POS_Y+50))

                elif cell == 5: #semilla
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect)
                    SCREEN.blit(bean, (POS_X + 80, POS_Y + 50))

                elif cell == 6: #esfera
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect)
                    SCREEN.blit(ball, (POS_X+80, POS_Y+50))

                elif cell == 7: #esfera
                    pygame.draw.rect(SCREEN, (135, 206, 250), rect)
                    SCREEN.blit(cloud, (POS_X+80, POS_Y+50))
                
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1) # Dibuja el borde negro


        

        
        pygame.display.update()

def credits():
    # sound.stop()
    # sound.play()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0)) 

        CREDIT_TEXT = get_font(150,1).render("CREDITS.", True, "White")
        OPTIONS_RECT = CREDIT_TEXT.get_rect(center=(640, 120))
        SCREEN.blit(CREDIT_TEXT, OPTIONS_RECT)

        NAMES_TEXT = get_font(80,1).render("nombres", True, "White")
        NAMES_RECT = NAMES_TEXT.get_rect(center=(645, 300))
        SCREEN.blit(NAMES_TEXT, NAMES_RECT)

        OPTIONS_BACK = Button(image=pygame.image.load("source\imagenes\Play_Rect_4.png"), pos=(900, 600), 
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
    # sound.stop()
    # sound.play()

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
        
        OPTIONS_BACK = Button(image=pygame.image.load("source\imagenes\Play_Rect_4.png"), pos=(900, 600), 
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
     #sound.stop()
     sound_mixer.play(sound)  
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


