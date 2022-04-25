# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame as pg
import socket, struct, select, sys
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

    def __init__(self, x, y):
        pg.init()
        self.screen = pg.display.set_mode((x, y))
        pg.display.set_caption("RADAR Air to Air")
        self.cockpit_pic = pg.image.load("pic/fcr_picb.png")


    def cockpit(self):
        self._x = 0
        self._y = 0
        self.screen.blit(self.cockpit_pic,(self._x, self._y))

    # Czerwnone kółko po kliknięciu
    def circle(self, pos):
        self.pos = pos
        self.circle_c = 'red' # color
        self.circle_r = 10 # size
        pg.draw.circle(self.screen, self.circle_c, event.pos, self.circle_r)


class Object:
    
    def __init__(self, xpawn, ypawn, zpawn, xpradar, ypradar, zpradar, x, y, z, index, scanEle, scanAzi):
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
        self.scanEle = scanEle
        self.scanAzi = scanAzi

    def calculate(self):
        # Azimuth Angle from vectors
        self.VectAB = [self.xpradar - self.xpawn, self.ypradar - self.ypawn]
        self.VectAC = [self.x - self.xpawn, self.y - self.ypawn]
        self.VectDot = np.dot(self.VectAB, self.VectAC)
        self.LenVectAB = np.sqrt(self.VectAB[0]**2 + self.VectAB[1]**2)
        self.LenVectAC = np.sqrt(self.VectAC[0]**2 + self.VectAC[1]**2)
        self.dist = np.sqrt((self.x-self.xpawn)**2 + (self.y-self.ypawn)**2 + (self.z-self.zpawn)**2)
        self.angleAzi = np.degrees(np.arccos(self.VectDot/(self.LenVectAB*self.LenVectAC)))
        self.DotABC = self.xpawn*self.ypradar + self.xpradar*self.y + self.x*self.ypawn - self.x*self.ypradar - self.xpawn*self.y - self.xpradar*self.ypawn
        #index = self.index
        if self.DotABC <= 0:  # Check on which side of the plane longitudinal axis vector
            self.angleAzi*=-1 # if above *-1

        # Elevation Angle from vectors
        self.VectAD = [self.xpradar - self.xpawn, self.zpradar - self.zpawn] #
        self.VectAE = [self.x - self.xpawn, self.z - self.zpawn]
        self.VectDotD = np.dot(self.VectAD, self.VectAE)
        self.LenVectAD = np.sqrt(self.VectAD[0]**2 + self.VectAD[1]**2)
        self.LenVectAE = np.sqrt(self.VectAE[0]**2 + self.VectAE[1]**2)
        self.angleEle = np.degrees(np.arccos(self.VectDotD/(self.LenVectAD*self.LenVectAE)))
        self.DotABD = self.xpawn*self.zpradar + self.xpradar*self.z + self.z*self.zpawn - self.z*self.zpradar - self.xpawn*self.z - self.xpradar*self.zpawn
        if self.DotABD >= 0: # Check on which side of the plane longitudinal axis vector
            self.angleEle*=-1 # if under *-1
       
        # if -self.scanAzi<=self.angleAzi<=self.scanAzi and -self.scanEle<=self.angleEle<=self.scanEle and self.index != 0:
        #     pg.draw.rect(wGame.screen, self.color,
        #                 [wWindow/2+self.angleAzi*pxScale, hWindow/2+self.angleEle*pxScale, 20, 20], 2)            

        return self.dist, self.angleAzi, self.angleEle, self.index

# Matrix of FCR buttons
FCR_x_left = 34
FCR_x_right = 562
FCR_y_down = 569
FCR_y_up = 33
FCR_y_matrix = [435, 435-66, 435-2*66, 435-3*66, 435-4*66]
FCR_x_matrix = [151, 151+73, 151+2*73, 151+3*73, 151+4*73]
FCR_button = 20.0


# Radar search parametr and data
scanElevation = 30
scanAzimuth = 30
colorFriend = (0,255,0)
colorFoe = (255,0,0)
colorRoam = (0,0,255)
zeros = np.zeros((10,4))

wWindow = 600
hWindow = 600
wFrame = 100
pxScale = (wWindow-wFrame*4)/scanAzimuth # Scaling

wGame = Cockpit(wWindow, hWindow)
myUDP = UDPConnection("127.0.0.1", 8000)
myUDP.connect()




run = True
# Pętla główna
while run:
    # Ctrl + C to terminate
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # graphic init
    wGame.cockpit()
    
    # event handling 
    keys = pg.key.get_pressed()

    # if keys[pg.K_RIGHT]:
    #     sky_x -= sky_step
    # if keys[pg.K_LEFT]:
    #     sky_x += sky_step
    
    # position of mousebuttondown
    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        print('x', mouse_pos[0], 'y', mouse_pos[1])
        click = wGame.circle(mouse_pos)

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


    # Receive decoded message
    message = myUDP.receive()

    # Implementation of variable
    gametime = message[0]
    XPawn, YPawn, ZPawn = message[1], message[2], message[3]
    XPawnRadar, YPawnRadar, ZPawnRadar = message[4], message[5], message[6]
    XFoe, YFoe, ZFoe, IndexFoe = message[7], message[8], message[9], int(message[10])
    XFriend, YFriend, ZFriend, IndexFriend = message[11], message[12], message[13], int(message[14])
    XRoam, YRoam, ZRoam, IndexRoam = message[15], message[16], message[17], int(message[18])
    Targets = int(message[19])
    
    objectsFriend = zeros
    objectsFoe = zeros
    objectsRoam = zeros

    for i in range(Targets):
        dist1, angleAzi1, angleEle1, index1 = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XFriend, YFriend, ZFriend, IndexFriend, scanElevation, scanAzimuth).calculate()
        objectsFriend[index1-1][0] = dist1
        objectsFriend[index1-1][1] = angleAzi1
        objectsFriend[index1-1][2] = angleEle1
        objectsFriend[index1-1][3] = index1
        if -scanAzimuth<=objectsFriend[i][1]<=scanAzimuth and -scanElevation<=objectsFriend[i][2]<=scanElevation and index1 != 0:
                pg.draw.rect(wGame.screen, colorFriend,
                            [wWindow/2+objectsFriend[i][1]*pxScale, hWindow/2+objectsFriend[i][2]*pxScale, 20, 20], 2)

    for i in range(Targets):
        dist2, angleAzi2, angleEle2, index2 = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XFoe, YFoe, ZFoe, IndexFoe, scanElevation, scanAzimuth).calculate()
        objectsFoe[index2-1][0] = dist2
        objectsFoe[index2-1][1] = angleAzi2
        objectsFoe[index2-1][2] = angleEle2
        objectsFoe[index2-1][3] = index2
        if -scanAzimuth<=objectsFoe[i][1]<=scanAzimuth and -scanElevation<=objectsFoe[i][2]<=scanElevation and index2 != 0:
                pg.draw.rect(wGame.screen, colorFoe,
                            [wWindow/2+objectsFoe[i][1]*pxScale, hWindow/2+objectsFoe[i][2]*pxScale, 20, 20], 2)
    for i in range(Targets):
        dist3, angleAzi3, angleEle3, index3 = Object(XPawn, YPawn, ZPawn, XPawnRadar, YPawnRadar, ZPawnRadar, XRoam, YRoam, ZRoam, IndexRoam, scanElevation, scanAzimuth).calculate()
        objectsRoam[index3-1][0] = dist3
        objectsRoam[index3-1][1] = angleAzi3
        objectsRoam[index3-1][2] = angleEle3
        objectsRoam[index3-1][3] = index3
        if -scanAzimuth<=objectsRoam[i][1]<=scanAzimuth and -scanElevation<=objectsRoam[i][2]<=scanElevation and index3 != 0:
                pg.draw.rect(wGame.screen, colorRoam,
                            [wWindow/2+objectsRoam[i][1]*pxScale, hWindow/2+objectsRoam[i][2]*pxScale, 20, 20], 2)

    
    del objectsFriend 
    del objectsFoe 
    del objectsRoam 
    pg.display.update()
    pg.time.delay(1) 

