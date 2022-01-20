# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame, sys


# Definiowanie okna gry
pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("RADAR Air to Air")

# Czarne tło pod belką
background_x = 0
background_y = 400
background_width = 1280
background_height = 400
background__color = (0, 0, 0)

def black(x, y, w, h):
    pygame.draw.rect(screen, background__color, (x, y, w, h))

# Dodawanie kokpitu
cockpit_pic = pygame.image.load("pic/cockpit_new.bmp")
cockpit_x = 0
cockpit_y = 0

def cockpit(x, y):
    screen.blit(cockpit_pic,(x, y))

# Sky
sky_pic = pygame.image.load("pic/sky.jpg") 
sky_x = -255 # Wyśrodkowanie horyzontu
sky_y = -420
sky_step = 5
sky_angle = 0

def sky(x, y, pic, a):
    orig_rect = pic.get_rect()
    rot_image = pygame.transform.rotate(pic, a)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    sky_pic = rot_image
    screen.blit(sky_pic, (x, y))
    return sky_pic

# Czerwnone kółko po kliknięciu
circle_c = (255,0,0)
circle_r = 10

def circle(pos):
    pygame.draw.circle(screen, circle_c, event.pos, circle_r)

# Macierz przycisków FCR
FCR_x_left = 450
FCR_x_right = 805
FCR_y_down = 780
FCR_y_up = 425
FCR_y_matrix = [690, 690-43, 690-2*43, 690-3*43, 690-4*43]
FCR_x_matrix = [530, 530+48, 530+2*48, 530+3*48, 530+4*48]
FCR_button = 18.0

run = True
# Pętla główna
while run:
    # opóźnienie w grze
    pygame.time.delay(20)
    
    sky(sky_x, sky_y, sky_pic, sky_angle)
    black(background_x, background_y, background_width, background_height)
    cockpit(cockpit_x, cockpit_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # obsługa zdarzeń 
    keys = pygame.key.get_pressed()
    # warunki do zmiany pozycji obiektu
    if keys[pygame.K_RIGHT]:
        sky_x -= sky_step
    if keys[pygame.K_LEFT]:
        sky_x += sky_step
    if keys[pygame.K_UP]:
        sky_y -= sky_step
    if keys[pygame.K_DOWN]:
        sky_y += sky_step
    if keys[pygame.K_d]:
        sky_angle += sky_step/5
    if keys[pygame.K_a]:
        sky_angle -= sky_step/5
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