# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame, sys
#import udp

# Definiowanie okna 
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("RADAR Air to Air")
cockpit_pic = pygame.image.load("pic/fcr_pic.png")
cockpit_x = 0
cockpit_y = 0

def cockpit(x, y):
    screen.blit(cockpit_pic,(x, y))

# Czerwnone kółko po kliknięciu
circle_c = (255,0,0)
circle_r = 10

def circle(pos):
    pygame.draw.circle(screen, circle_c, event.pos, circle_r)

# Macierz przycisków FCR
FCR_x_left = 34
FCR_x_right = 562
FCR_y_down = 569
FCR_y_up = 33
FCR_y_matrix = [435, 435-66, 435-2*66, 435-3*66, 435-4*66]
FCR_x_matrix = [151, 151+73, 151+2*73, 151+3*73, 151+4*73]
FCR_button = 20.0

run = True
# Pętla główna
while run:
    # opóźnienie w grze
    pygame.time.delay(20)
    # Inicjalizacja grafiki
    cockpit(cockpit_x, cockpit_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # obsługa zdarzeń 
    keys = pygame.key.get_pressed()
    # warunki do zmiany pozycji obiektu
    # if keys[pygame.K_RIGHT]:
    #     sky_x -= sky_step
    # if keys[pygame.K_LEFT]:
    #     sky_x += sky_step
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        print('x', mouse_pos[0], 'y', mouse_pos[1])

        # Lewa kolumna button FCR
        if  ((mouse_pos[0]-FCR_button)<FCR_x_left<(mouse_pos[0]+FCR_button)):
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[0]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[1]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[2]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[3]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[4]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
        # Prawa kolumna button FCR
        if  ((mouse_pos[0]-FCR_button)<FCR_x_right<(mouse_pos[0]+FCR_button)):
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[0]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[1]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[2]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[3]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[4]<(mouse_pos[1]+FCR_button)):
                circle(mouse_pos)
        # Dolny wiersz button FCR
        if  ((mouse_pos[1]-FCR_button)<FCR_y_down<(mouse_pos[1]+FCR_button)):
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[0]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[1]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[2]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[3]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[4]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
        # Górny wiersz button FCR
        if  ((mouse_pos[1]-FCR_button)<FCR_y_up<(mouse_pos[1]+FCR_button)):
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[0]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[1]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[2]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[3]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)
            if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[4]<(mouse_pos[0]+FCR_button)):
                circle(mouse_pos)

    pygame.display.update()