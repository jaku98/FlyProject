# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import unreal
import pygame, sys
import socket, struct, select
import numpy as np

class UDPConnection:

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip #""
        self.udp_port = udp_port #8000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def connect(self):
        self.sock.bind((self.udp_ip, self.udp_port))
        print("UDP connection with UE4: OK!")

    def receive(self): 
        self.data, self.addr = self.sock.recvfrom(512) # buffer size
        self.data = struct.unpack("20f3c", self.data) # unpack data
        return self.data
    
    def close(self):
        self.sock.close()
        print("Closed")
        exit()


class Cockpit:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("RADAR Air to Air")
        self.cockpit_pic = pygame.image.load("pic/fcr_picb.png")


    def cockpit(self):
        self._x = 0
        self._y = 0
        self.screen.blit(self.cockpit_pic,(self._x, self._y))

    # Czerwnone kółko po kliknięciu
    def circle(self, pos):
        self.pos = pos
        self.circle_c = 'red' # color
        self.circle_r = 10 # size
        pygame.draw.circle(self.screen, self.circle_c, event.pos, self.circle_r)


class Object:

    def __init__(self, xpawn, ypawn, zpawn, xpradar, ypradar, zpradar, x, y, z, index):
        self.xpawn = xpawn
        self.ypawn = ypawn
        self.zpawn = zpawn
        self.xpradar = xpradar
        self.ypradar = ypradar
        self.zpradar = zpradar
        self.x = x
        self.y = y
        self.z = z
        self.index = index


    def calculate(self):
        # Azymuth Angle
        VectAB = [self.xpradar - self.xpawn, self.ypradar - self.ypawn]
        VectAC = [self.x - self.xpawn, self.y - self.ypawn]
        VectDot = np.dot(VectAB, VectAC)
        LenVectAB = np.sqrt(VectAB[0]**2 + VectAB[1]**2)
        LenVectAC = np.sqrt(VectAC[0]**2 + VectAC[1]**2)
        dist = np.sqrt((self.x-self.xpawn)**2 + (self.y-self.ypawn)**2 + (self.z-self.zpawn)**2)
        angleAzy = np.degrees(np.arccos(VectDot/(LenVectAB*LenVectAC)))
        DotABC = self.xpawn*self.ypradar + self.xpradar*self.y + self.x*self.ypawn - self.x*self.ypradar - self.xpawn*self.y - self.xpradar*self.ypawn
        index = self.index
        if DotABC < 0:
            angleAzy*=-1

        # Elevation Angle
        VectAD = [self.xpradar - self.xpawn, self.zpradar - self.zpawn] #
        VectAE = [self.x - self.xpawn, self.z - self.zpawn]
        VectDotD = np.dot(VectAD, VectAE)
        LenVectAD = np.sqrt(VectAD[0]**2 + VectAD[1]**2)
        LenVectAE = np.sqrt(VectAE[0]**2 + VectAE[1]**2)
        angleEle = np.degrees(np.arccos(VectDotD/(LenVectAD*LenVectAE)))
        DotABD = self.xpawn*self.zpradar + self.xpradar*self.z + self.z*self.zpawn - self.z*self.zpradar - self.xpawn*self.z - self.xpradar*self.zpawn
        if DotABD < 0:
            angleEle*=-1

        return dist, angleAzy, angleEle, index      

# Matrix of FCR buttons
FCR_x_left = 34
FCR_x_right = 562
FCR_y_down = 569
FCR_y_up = 33
FCR_y_matrix = [435, 435-66, 435-2*66, 435-3*66, 435-4*66]
FCR_x_matrix = [151, 151+73, 151+2*73, 151+3*73, 151+4*73]
FCR_button = 20.0

pyGame = Cockpit()
myUDP = UDPConnection("127.0.0.1", 8000)
myUDP.connect()
i = 0
run = True
# Pętla główna
while run:
    # Ctrl + C to terminate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Delay in game
    pygame.time.delay(1)

    # receive decoded message
    message = myUDP.receive()

    # graphic init
    pyGame.cockpit()
    
    # event handling 
    keys = pygame.key.get_pressed()

    # if keys[pygame.K_RIGHT]:
    #     sky_x -= sky_step
    # if keys[pygame.K_LEFT]:
    #     sky_x += sky_step
    
    # position of mousebuttondown
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        print('x', mouse_pos[0], 'y', mouse_pos[1])
        click = pyGame.circle(mouse_pos)

        # Lewa kolumna button FCR
        if  ((mouse_pos[0]-FCR_button)<FCR_x_left<(mouse_pos[0]+FCR_button)):
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[0]<(mouse_pos[1]+FCR_button)):
                click
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[1]<(mouse_pos[1]+FCR_button)):
                click
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[2]<(mouse_pos[1]+FCR_button)):
                click
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[3]<(mouse_pos[1]+FCR_button)):
                click
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[4]<(mouse_pos[1]+FCR_button)):
                click
        # # Prawa kolumna button FCR
        # if  ((mouse_pos[0]-FCR_button)<FCR_x_right<(mouse_pos[0]+FCR_button)):
        #     if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[0]<(mouse_pos[1]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[1]<(mouse_pos[1]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[2]<(mouse_pos[1]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[3]<(mouse_pos[1]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[4]<(mouse_pos[1]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        # # Dolny wiersz button FCR
        # if  ((mouse_pos[1]-FCR_button)<FCR_y_down<(mouse_pos[1]+FCR_button)):
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[0]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[1]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[2]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[3]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[4]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        # # Górny wiersz button FCR
        # if  ((mouse_pos[1]-FCR_button)<FCR_y_up<(mouse_pos[1]+FCR_button)):
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[0]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[1]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[2]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[3]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)
        #     if ((mouse_pos[0]-FCR_button)<FCR_x_matrix[4]<(mouse_pos[0]+FCR_button)):
        #         Cockpit.circle(mouse_pos)

        
    #  Implementation of variable
    gametime = message[0]
    XPawn, YPawn, ZPawn = message[1], message[2], message[3]
    XPawnRadar, YPawnRadar, ZPawnRadar = message[4], message[5], message[6]
    XFoe, YFoe, ZFoe, IndexFoe = message[7], message[8], message[9], message[10]
    XFriend, YFriend, ZFriend, IndexFriend = message[11], message[12], message[13], message[14]
    XRoam, YRoam, ZRoam, IndexRoam = message[15], message[16], message[17], message[18]
    

    distFriend, angleAzyFriend, angleEleFriend, indexFriend = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XFriend, YFriend, ZFriend, IndexFriend).calculate()
    distFoe, angleAzyFoe, angleEleFoe, indexFoe = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XFoe, YFoe, ZFoe, IndexFoe).calculate()
    distRoam, angleAzyRoam, angleEleRoam, indexRoam = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XRoam, YRoam, ZRoam, IndexRoam).calculate()
    print('....\n')
    print('distTo', np.round((distFriend), 1), 'angleAzy', np.round((angleAzyFriend), 1), 'angleEle', np.round((angleEleFriend), 1), 'index', indexFriend)
    print('distTo', np.round((distFoe), 1), 'angleAzy', np.round((angleAzyFoe), 1), 'angleEle', np.round((angleEleFoe), 1), 'index', indexFoe)
    print('distTo', np.round((distRoam), 1), 'angleAzy', np.round((angleAzyRoam), 1), 'angleEle', np.round((angleEleRoam), 1), 'index', indexRoam)
    

    # Drawing a rect
    i+=0.5
    pygame.draw.rect(pyGame.screen, (0, 255, 0),
                 [100+i, 100+i, 50, 50], 2)

    pygame.draw.rect(pyGame.screen, (255, 000, 0),
                [275, 450-i, 50, 50], 2)

    pygame.display.update()