# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame as pg
import socket, struct, select, sys, gc
import numpy as np 

pg.font.init()
gc.collect()
clock = pg.time.Clock()

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
        self.data = struct.unpack("20f3b", self.data) # unpack data
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
        #self.cockpit_pic = pg.image.load("pic/fcr_picb.png")

    def cockpit(self):
        self._x = 0
        self._y = 0
        #self.screen.blit(self.cockpit_pic,(self._x, self._y))
        self.screen.fill([0, 0, 0])
        pg.draw.rect(self.screen, colorGrey0, [0, 0,600,600], 75)
        pg.draw.rect(self.screen, colorGrey1, [70,70,460,460], 6, border_radius=10)
        
    
    # Czerwnone kółko po kliknięciu
    def circle(self, pos):
        self.pos = pos
        self.circle_c = 'red' # color
        self.circle_r = 10 # size
        pg.draw.circle(self.screen, self.circle_c, event.pos, self.circle_r)


# class Object:

#     def __init__(self, xpawn, ypawn, zpawn, xpradar, ypradar, zpradar, x, y, z, index, scanEle, scanAzi):
#         self.xpawn = xpawn
#         self.ypawn = ypawn
#         self.zpawn = zpawn
#         self.xpradar = xpradar
#         self.ypradar = ypradar
#         self.zpradar = zpradar
#         self.x = x
#         self.y = y
#         self.z = z
#         self.index = index
#         self.scanEle = scanEle
#         self.scanAzi = scanAzi

#     def calculate(self):
#         # Azimuth Angle from vectors
#         self.aVectAB = [self.xpradar - self.xpawn, self.ypradar - self.ypawn]
#         self.aVectAC = [self.x - self.xpawn, self.y - self.ypawn]
#         self.aVectDot = np.dot(self.aVectAB, self.aVectAC)
#         self.aLenVectAB = np.sqrt(self.aVectAB[0]**2 + self.aVectAB[1]**2)
#         self.aLenVectAC = np.sqrt(self.aVectAC[0]**2 + self.aVectAC[1]**2)
#         self.dist = np.sqrt((self.x-self.xpawn)**2 + (self.y-self.ypawn)**2 + (self.z-self.zpawn)**2)
#         self.angleAzi = np.degrees(np.arccos(self.aVectDot/(self.aLenVectAB*self.aLenVectAC)))
#         self.DotABC = (self.xpawn*self.ypradar + self.xpradar*self.y + self.x*self.ypawn
#                         - self.x*self.ypradar - self.xpawn*self.y - self.xpradar*self.ypawn)
#         if self.DotABC <= 0:  # Check on which side of the plane longitudinal axis vector
#             self.angleAzi*=-1 # if above *-1

#         ##Elevation Angle from vectors
#         # self.eVectAC = [self.x - self.xpawn, self.y - self.ypawn, self.z - self.zpawn]
#         # self.eVectAC_ = [self.xpradar - self.xpawn, self.ypradar - self.ypawn, self.zpradar - self.zpradar]
#         # self.eVectDot = np.dot(self.eVectAC, self.eVectAC_)
#         # self.eLenVectAC = np.sqrt(self.eVectAC[0]**2 + self.eVectAC[1]**2 + self.eVectAC[2]**2)
#         # self.eLenVectAC_ = np.sqrt(self.eVectAC_[0]**2 + self.eVectAC_[1]**2 + self.eVectAC_[2]**2)

#         # self.angleEle = np.degrees(np.arccos(self.eVectDot/(self.eLenVectAC*self.eLenVectAC_)))
#         self.eVectAC = [self.x - self.xpawn, self.y - self.ypawn, self.z - self.zpawn]
#         self.eVectAB = [self.xpradar - self.xpawn, self.ypradar - self.ypawn, self.zpradar - self.zpawn]
#         self.eVectCB = [self.xpradar - self.x, self.ypradar- self.y, self.zpradar - self.z]
#         self.eLenVectAC = np.sqrt(self.eVectAC[0]**2 + self.eVectAC[1]**2 + self.eVectAC[2]**2)
#         self.eLenVectAB = np.sqrt(self.eVectAB[0]**2 + self.eVectAB[1]**2 + self.eVectAB[2]**2)
#         self.eLenVectCB = np.sqrt(self.eVectCB[0]**2 + self.eVectCB[1]**2 + self.eVectCB[2]**2)
#         self.licznik = self.eLenVectCB**2 - self.eLenVectAC**2 - self.eLenVectAB**2
#         self.mianownik = -2 * self.eLenVectAC * self.eLenVectAB
#         self.angleEle = np.degrees(np.arccos(self.licznik/self.mianownik))

#         print(self.angleEle)
#         return self.dist, self.angleAzi, self.angleEle, self.index

class Button:

    colorHvr = [130, 130, 130]
    colorClick = [250, 200, 0]
    colorButton = [150, 150, 150]
    widthButton = 40
    heightButton = 40

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        global clicked
        action = False

        pos = pg.mouse.get_pos()

        buttonRect = pg.rect(self.x, self.y, self.widthButton, self.heightButton)

        if buttonRect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                clicked = True
                pg.draw.rect(wGame.screen, self.colorClick, buttonRect)
            elif pg.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pg.draw.rect(wGame.screen, self.colorHvr, buttonRect)
        else:
            pg.draw.rect(wGame.screen, self.colorButton, buttonRect)

        pg.draw.line(wGame, [0,0,0], (self.x,self.y),(self.x+self.widthButton,self.y),2)
        pg.draw.line(wGame, [0,0,0], (self.x,self.y),(self.x+self.y,self.heightButton),2)
        pg.draw.line(wGame)

# Matrix of FCR buttons https://www.youtube.com/watch?v=jyrP0dDGqgY
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

objectsFriend = np.zeros((10,6))
objectsFoe = np.zeros((10,6))
objectsRoam = np.zeros((10,6))
indexDel = 0

# GUI
clicked = False
fontSet = pg.font.SysFont("Arial", 18, bold=False)
fontColorWhite = [255,255,255]
fontColorBlack = [0,0,0]
colorGrey0 = [40, 40, 40]
colorGrey1 = [70, 70, 70]
colorGrey2 = [100, 100, 100]

textFCR = fontSet.render("FCR", False, fontColorWhite)
textTGP = fontSet.render("TGP", False, fontColorWhite)
textWPN = fontSet.render("WPN", False, fontColorWhite)
textTFR = fontSet.render("TFR", False, fontColorWhite)
textFLIR = fontSet.render("FLIR", False, fontColorWhite)

textSMS = fontSet.render("SMS", False, fontColorWhite)
textHSD = fontSet.render("HSD", False, fontColorWhite)
textDTE = fontSet.render("DTE", False, fontColorWhite)
textTEST = fontSet.render("TEST", False, fontColorWhite)
textFLCS = fontSet.render("FLCS", False, fontColorWhite)

textBLANK = fontSet.render("BLANK", False, fontColorBlack, fontColorWhite)
textHAD = fontSet.render("HAD", False, fontColorWhite)
textRCCE = fontSet.render("RCCE", False, fontColorWhite)
textRESET = fontSet.render("RESET", False, fontColorWhite)

textSWAP = fontSet.render("SWAP", False, fontColorWhite)
textLABEL = fontSet.render("--------", False, fontColorWhite, fontColorWhite)
textDTE = fontSet.render("DTE", False, fontColorWhite)

buttonFCR = False

def OpenMenu():
    wGame.screen.blit(textFCR, [85, 160])
    wGame.screen.blit(textTGP, [85, 230])
    wGame.screen.blit(textTGP, [85, 295])
    wGame.screen.blit(textWPN, [85, 360])
    wGame.screen.blit(textFLIR, [85, 425])
    
    wGame.screen.blit(textSMS, [480, 160])
    wGame.screen.blit(textHSD, [480, 230])
    wGame.screen.blit(textDTE, [480, 295])
    wGame.screen.blit(textTEST, [470, 360])
    wGame.screen.blit(textFLCS, [470, 425])

    wGame.screen.blit(textBLANK, [125, 80])
    wGame.screen.blit(textHAD, [210, 80])
    wGame.screen.blit(textRCCE, [350, 80])
    wGame.screen.blit(textRESET, [415, 80])

    wGame.screen.blit(textSWAP, [125, 500])
    wGame.screen.blit(textLABEL, [210, 500])
    wGame.screen.blit(textDTE, [350, 500])

def FCRMenu():
    pg.draw.rect(wGame.screen, fontColorWhite,[85, 85, 430, 430], 2)
    i = 0




def drawFriend(i):
    pg.draw.circle(wGame.screen, colorFriend,
                [wWindow/2+objectsFriend[i][1]*pxScale, hWindow/2+objectsFriend[i][2]*pxScale], 10, 2)
def drawFoe(i):
    pg.draw.rect(wGame.screen, colorFoe,
                [wWindow/2+objectsFoe[i][1]*pxScale, hWindow/2+objectsFoe[i][2]*pxScale, 20, 20], 2)
def drawRoam(i):
    pg.draw.rect(wGame.screen, colorFoe,
                [wWindow/2+objectsRoam[i][1]*pxScale, hWindow/2+objectsRoam[i][2]*pxScale, 20, 20], 2)


# Window settings
wWindow = 600
hWindow = 600
wFrame = 100
pxScale = (wWindow-wFrame*4)/scanAzimuth # Scaling


# Init PyGame and UDP
wGame = Cockpit(wWindow, hWindow)
myUDP = UDPConnection("127.0.0.1", 8000)
myUDP.connect()

run = True
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
                print('5')
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[1]<(mouse_pos[1]+FCR_button)):
                print('4')
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[2]<(mouse_pos[1]+FCR_button)):
                print('3')
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[3]<(mouse_pos[1]+FCR_button)):
                print('2')
            if ((mouse_pos[1]-FCR_button)<FCR_y_matrix[4]<(mouse_pos[1]+FCR_button)):
                print('1')
                buttonFCR = True
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

    # Receive section / Implementation of variable
    altPawn = message[0]
    distFriend, aziFriend, eleFriend = message[1], message[2], message[3]
    angleToPawnFriend, altFriend, indexFriend = message[4], message[5], int(message[6])
    distFoe, aziFoe, eleFoe = message[7], message[8], message[9]
    angleToPawnFoe, altFoe, indexFoe = message[10], message[11], int(message[12])
    distRoam, aziRoam, eleRoam = message[13], message[14], message[15]
    angleToPawnRoam, altRoam, indexRoam = message[16], message[17], int(message[18])
    allTargets, friendsTarget, foeTarget, roamTarget = int(message[19]), message[20], message[21], message[22]

    if allTargets > 0:

        # Calculate
        if friendsTarget > 0:
            for i in range(friendsTarget):
                if indexFriend > 0:    
                    objectsFriend[indexFriend-1][0] = distFriend
                    objectsFriend[indexFriend-1][1] = aziFriend
                    objectsFriend[indexFriend-1][2] = eleFriend*-1
                    objectsFriend[indexFriend-1][3] = angleToPawnFriend
                    objectsFriend[indexFriend-1][4] = altFriend
                    objectsFriend[indexFriend-1][5] = indexFriend

        if foeTarget > 0:        
            for i in range(foeTarget):
                if indexFoe > 0: 
                    objectsFoe[indexFoe-1][0] = distFoe
                    objectsFoe[indexFoe-1][1] = aziFoe
                    objectsFoe[indexFoe-1][2] = eleFoe*-1
                    objectsFoe[indexFoe-1][3] = angleToPawnFoe
                    objectsFoe[indexFoe-1][4] = altFoe
                    objectsFoe[indexFoe-1][5] = indexFoe

        if roamTarget > 0:
            for i in range(roamTarget):
                if indexRoam > 0: 
                    objectsRoam[indexRoam-1][0] = distRoam
                    objectsRoam[indexRoam-1][1] = aziRoam
                    objectsRoam[indexRoam-1][2] = eleRoam*-1
                    objectsRoam[indexRoam-1][3] = angleToPawnRoam
                    objectsRoam[indexRoam-1][4] = altRoam
                    objectsRoam[indexRoam-1][5] = indexRoam

        if buttonFCR == True:
            FCRMenu()

            for i in range(friendsTarget):
                if ((-scanAzimuth<=objectsFriend[i][1]<=scanAzimuth) and (-scanElevation<=objectsFriend[i][2]<=scanElevation)):
                        drawFriend(i)
            for i in range(foeTarget):
                if ((-scanAzimuth<=objectsFoe[i][1]<=scanAzimuth) and (-scanElevation<=objectsFoe[i][2]<=scanElevation) ):
                        drawFoe(i)
            for i in range(roamTarget):
                if ((-scanAzimuth<=objectsRoam[i][1]<=scanAzimuth) and (-scanElevation<=objectsRoam[i][2]<=scanElevation)):
                        drawRoam(i)

        else:    
            OpenMenu()
        # Draw    




    # Delete section
    del message

    if indexDel > 100:
        if allTargets > 0:
            del allTargets   
        if friendsTarget > 0:
            del distFriend, aziFriend, eleFriend, angleToPawnFriend, altFriend, indexFriend, friendsTarget   
        if foeTarget > 0:
            del distFoe, aziFoe, eleFoe, angleToPawnFoe, altFoe, indexFoe, foeTarget
        if roamTarget > 0:  
            del distRoam, aziRoam, eleRoam, angleToPawnRoam, altRoam, indexRoam, roamTarget 
        indexDel = 0
    indexDel += 1 

    pg.display.update()
    pg.time.delay(1)