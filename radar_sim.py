# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame, sys

# Definiowanie okna gry
pygame.init()
screen = pygame.display.set_mode((1280, 1024))
pygame.display.set_caption("RADAR Air to Air")

# Czarne tło pod belką
background_x = 0
background_y = 570
background_width = 1280
background_height = 454
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
#h = (sky_pic.get_height())
#w = (sky_pic.get_width())
#sky_pic = pygame.transform.scale(sky_pic, h*2, w*2)
sky_x = -255 # Wyśrodkowanie horyzontu
sky_y = -420
sky_step = 5
sky_angle = 0

def sky(x, y, pic, a):
    #screen.blit(sky_pic, (x, y))
    orig_rect = pic.get_rect()
    rot_image = pygame.transform.rotate(pic, a)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    sky_pic = rot_image
    screen.blit(sky_pic, (x, y))
    return sky_pic

run = True
# Pętla główna
while run:
    # opóźnienie w grze
    pygame.time.delay(20)
    
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
    
    sky(sky_x, sky_y, sky_pic, sky_angle)
    black(background_x, background_y, background_width, background_height)
    cockpit(cockpit_x, cockpit_y)

    pygame.display.update()