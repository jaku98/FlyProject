# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym

import pygame

pygame.init()
# Definiowanie okna gry
win = pygame.display.set_mode((1280, 1024))
# Wyświetlenie okna gry
pygame.display.set_caption("RADAR Air to Air")
# Dodawanie tła



x = 0
y = 40
szerokosc = 20
wysokosc = 20
krok = 20


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
    if keys[pygame.K_LEFT]:
        x -= krok
    if keys[pygame.K_RIGHT]:
        x += krok
    if keys[pygame.K_UP]:
        y -= krok
    if keys[pygame.K_DOWN] :
        y += krok

    pygame.draw.rect(win, (0, 255, 0), (x, y, szerokosc, wysokosc))

    cockpit = pygame.image.load("pic/cockpit_new.bmp")
    win.blit(cockpit,(0, 0))

    pygame.display.update()
