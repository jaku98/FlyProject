# Model programowy systemu zobrazowania sytuacji powietrznej w radarze pokładowym
import pygame as pg
from pygame.locals import *
import socket, struct, select, sys, gc
import numpy as np 

pg.font.init()
gc.collect()

class UDPConnection:

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def connect(self):
        self.sock.bind((self.udp_ip, self.udp_port))
        print("UDP connection: OK!")

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

    def cockpit(self):
        self._x1 = 40
        self._y1 = 40
        self._x2 = 560
        self._y2 = 40
        self._x3 = 40
        self._y3 = 560
        self._x4 = 560
        self._y4 = 560

        # Frames
        self.screen.fill([0, 0, 0])
        pg.draw.rect(self.screen, colorGrey1, [0, 0,600,600], 75)
        pg.draw.rect(self.screen, colorGrey2, [70,70,460,460], 6, border_radius=10)
        # Screws
        pg.draw.rect(self.screen, colorGrey0, [-10,-10,75,75], border_radius=15)
        pg.draw.circle(self.screen, colorGrey3, [self._x1,self._y1], 10)
        pg.draw.circle(self.screen, fontColorBlack, [self._x1,self._y1], 10, 2)
        pg.draw.line(self.screen, fontColorBlack, [self._x1-10,self._y1],[self._x1+10,self._y1],2) 
        pg.draw.line(self.screen, fontColorBlack, [self._x1,self._y1-10],[self._x1,self._y1+10],2)
        
        pg.draw.rect(self.screen, colorGrey0, [535,-10,75,75], border_radius=15)
        pg.draw.circle(self.screen, colorGrey3, [self._x2,self._y2], 10)
        pg.draw.circle(self.screen, fontColorBlack, [self._x2,self._y2], 10, 2)
        pg.draw.line(self.screen, fontColorBlack, [self._x2-10,self._y2],[self._x2+10,self._y2],2) 
        pg.draw.line(self.screen, fontColorBlack, [self._x2,self._y2-10],[self._x2,self._y2+10],2)

        pg.draw.rect(self.screen, colorGrey0, [-10, 535,75,75], border_radius=15)
        pg.draw.circle(self.screen, colorGrey3, [self._x3,self._y3], 10)
        pg.draw.circle(self.screen, fontColorBlack, [self._x3,self._y3], 10, 2)
        pg.draw.line(self.screen, fontColorBlack, [self._x3-10,self._y3],[self._x3+10,self._y3],2) 
        pg.draw.line(self.screen, fontColorBlack, [self._x3,self._y3-10],[self._x3,self._y3+10],2)

        pg.draw.rect(self.screen, colorGrey0, [535, 535,75,75], border_radius=15)
        pg.draw.circle(self.screen, colorGrey3, [self._x4,self._y4], 10)
        pg.draw.circle(self.screen, fontColorBlack, [self._x4,self._y4], 10, 2)
        pg.draw.line(self.screen, fontColorBlack, [self._x4-10,self._y4],[self._x4+10,self._y4],2) 
        pg.draw.line(self.screen, fontColorBlack, [self._x4,self._y4-10],[self._x4,self._y4+10],2)
    
    # Red circle after click
    def circle(self, pos):
        self.pos = pos
        self.circle_c = 'red' # color
        self.circle_r = 10 # size
        pg.draw.circle(self.screen, self.circle_c, event.pos, self.circle_r)


class Button:

    colorHvr = [130, 130, 130]
    colorClick = [250, 200, 0]
    colorButton = [150, 150, 150]
    widthButton = 50
    heightButton = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        global clicked
        action = False

        pos = pg.mouse.get_pos()
    
        buttonRect = pg.Rect(self.x, self.y, self.widthButton, self.heightButton)

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

        pg.draw.line(wGame.screen, [0,0,0], (self.x,self.y),(self.x + self.widthButton,self.y),2)
        pg.draw.line(wGame.screen, [0,0,0], (self.x,self.y),(self.x, self.y + self.heightButton),2)
        pg.draw.line(wGame.screen, [255,255,255],(self.x, self.y + self.heightButton), (self.x + self.widthButton, self.y + self.heightButton),2)
        pg.draw.line(wGame.screen, [255,255,255],(self.x + self.widthButton, self.y), (self.x + self.widthButton, self.y + self.heightButton),2)

        return action



# Radar search parametr and data
scanElevation = 26.2*2
scanAzimuth = 60
scanDistance = 296

colorFriend = (0,255,0) # Green
colorFoe = (255,0,0) # Red
colorRoam = (255,255,0) # Yellow
fontColorWhite = [255,255,255] 
fontColorBlack = [0,0,0]
colorGrey0 = [30, 30, 30]
colorGrey1 = [40, 40, 40]
colorGrey2 = [70, 70, 70]
colorGrey3 = [100, 100, 100]
colorDBlue = [0, 125, 240]

objectsFriend = np.zeros((10,6))
objectsFoe = np.zeros((10,6))
objectsRoam = np.zeros((10,6))
imageFriend = pg.transform.scale(pg.image.load('pic/friend.png'),[25,25])
imageFoe = pg.transform.scale(pg.image.load('pic/foe.png'),[25,25])
imageRoam = pg.transform.scale(pg.image.load('pic/unknow.png'),[25,25])
arrayFriendImg = [imageFriend]*10
arrayFoeImg = [imageFoe]*10
arrayRoamImg = [imageRoam]*10
indexDel = 0


# ///GUI///
# Window settings
wWindow = 600
hWindow = 600
wFrame = 100
center = 300
pxScaleAzi = (wWindow-wFrame*4)/scanAzimuth
pxScaleEle = (hWindow-wFrame*4)/scanElevation
pxScaleDis = (hWindow-wFrame*2)/scanDistance

# Buttons implementation
Button1 = Button(10,140)
Button2 = Button(10,210)
Button3 = Button(10,280)
Button4 = Button(10,350)
Button5 = Button(10,420)

Button6 = Button(540,140)
Button7 = Button(540,210)
Button8 = Button(540,280)
Button9 = Button(540,350)
Button10 = Button(540,420)

Button11 = Button(140,10)
Button12 = Button(210,10)
Button13 = Button(280,10)
Button14 = Button(350,10)
Button15 = Button(420,10)

Button16 = Button(140,540)
Button17 = Button(210,540)
Button18 = Button(280,540)
Button19 = Button(350,540)
Button20 = Button(420,540)

#Button variables
clicked = False
FCR = False
clickDis = 3
scanDistanceCalc = scanDistance

scanAzi = 6
clicksScanAzi = 0
scanAziStep = 1
scanAziLeft = -scanAzimuth
scanAziRight = scanAzimuth
xSearchAzi = center
xSearchAziStep = 4
xSearchAziStep_ = xSearchAziStep

scanEle = 4
clicksScanEle = 0
scanEleUp = scanElevation/2
scanEleUp_ = scanEleUp/2
scanEleDown = -scanElevation/2
scanEleDown_ = scanEleDown
scanEleStep = 1
ySearchEle = center

xScanAim = center
yScanAim = center
yScanAim_ = yScanAim
scanAimStep = 3
searchAimUp = wFrame
searchAimDown = hWindow-wFrame
aimUpRange = 0
aimDownRange = 0
aimDist = center

# Font settings
fontSet = pg.font.SysFont("Arial", 18, bold=False)
fontDistSet = pg.font.SysFont("Arial", 16, bold=False)

# Render text
# Open menu
#LEFT
textFCR = fontSet.render("FCR", False, fontColorWhite)
textTGP = fontSet.render("TGP", False, fontColorWhite)
textWPN = fontSet.render("WPN", False, fontColorWhite)
textTFR = fontSet.render("TFR", False, fontColorWhite)
textFLIR = fontSet.render("FLIR", False, fontColorWhite)
#RIGHT
textSMS = fontSet.render("SMS", False, fontColorWhite)
textHSD = fontSet.render("HSD", False, fontColorWhite)
textDTE = fontSet.render("DTE", False, fontColorWhite)
textTEST = fontSet.render("TEST", False, fontColorWhite)
textFLCS = fontSet.render("FLCS", False, fontColorWhite)
#UP
textBLANK = fontSet.render("BLANK", False, fontColorBlack, fontColorWhite)
textHAD = fontSet.render("HAD", False, fontColorWhite)
textRCCE = fontSet.render("RCCE", False, fontColorWhite)
textRESET = fontSet.render("RESET", False, fontColorWhite)
#DOWN
textSWAP = fontSet.render("SWAP", False, fontColorWhite)
textLABEL = fontSet.render("--------", False, fontColorWhite, fontColorWhite)
textDTE = fontSet.render("DTE", False, fontColorWhite)

# FCR Menu
#UP
textCRM = fontSet.render(" CRM ", False, fontColorWhite, fontColorBlack)
textRWS = fontSet.render(" RWS ", False, fontColorWhite, fontColorBlack)
textNORM = fontSet.render(" NORM ", False, fontColorWhite, fontColorBlack)
textOVRD = fontSet.render(" OVRD ", False, fontColorWhite, fontColorBlack)
textCNTL = fontSet.render(" CNTL ", False, fontColorWhite, fontColorBlack)
#DOWN
textSWAP = fontSet.render(" SWAP ", False, fontColorWhite, fontColorBlack)
textFCR = fontSet.render(" FCR ", False, fontColorBlack, fontColorWhite)
textTEST = fontSet.render(" TEST ", False, fontColorWhite, fontColorBlack)
textDTE = fontSet.render(" DTE ", False, fontColorWhite, fontColorBlack)
textDCLT = fontSet.render(" DCLT ", False, fontColorWhite, fontColorBlack)
#RIGHT
textCONT = fontSet.render("CONT", False, fontColorWhite, fontColorBlack)
#LEFT
textDist = fontSet.render(str(scanDistance), False, fontColorWhite)
textAzi = fontSet.render('A', False, fontColorWhite)
textEle = fontSet.render('B', False, fontColorWhite)
textAziNum = fontSet.render(str(scanAzi), False, fontColorWhite)
textEleNum = fontSet.render(str(scanEle), False, fontColorWhite)
#AIM
textaimUpRange = fontDistSet.render(str(aimUpRange), False, fontColorWhite)
textaimDownRange = fontDistSet.render(str(aimDownRange), False, fontColorWhite)

# Show text start menu
def OpenMenu():
    wGame.screen.blit(textFCR, [85, 155])
    wGame.screen.blit(textTGP, [85, 225])
    wGame.screen.blit(textWPN, [85, 295])
    wGame.screen.blit(textTFR, [85, 365])
    wGame.screen.blit(textFLIR, [85, 435])
    
    wGame.screen.blit(textSMS, [480, 155])
    wGame.screen.blit(textHSD, [480, 225])
    wGame.screen.blit(textDTE, [480, 295])
    wGame.screen.blit(textTEST, [470, 366])
    wGame.screen.blit(textFLCS, [470, 435])

    wGame.screen.blit(textBLANK, [140, 80])
    wGame.screen.blit(textHAD, [220, 80])
    wGame.screen.blit(textRCCE, [355, 80])
    wGame.screen.blit(textRESET, [420, 80])

    wGame.screen.blit(textSWAP, [145, 500])
    wGame.screen.blit(textLABEL, [220, 500])
    wGame.screen.blit(textDTE, [360, 500])

# Fcr menu
def FCRMenu():
    pg.draw.rect(wGame.screen, fontColorWhite,[85, 85, 430, 430], 2)
    pg.draw.rect(wGame.screen, fontColorBlack,[80, 165, 15, 75])
    pg.draw.rect(wGame.screen, fontColorBlack,[80, 285, 15, 40])
    pg.draw.rect(wGame.screen, fontColorBlack,[80, 355, 15, 40])
    pg.draw.polygon(wGame.screen, fontColorWhite,[(95, 170), (110, 185), (80,185)], 2)
    pg.draw.polygon(wGame.screen, fontColorWhite,[(95, 230), (110, 215), (80,215)], 2)    
    
    wGame.screen.blit(textDist, [85, 190])
    wGame.screen.blit(textAzi, [80, 285])
    wGame.screen.blit(textAziNum, [82, 302])
    wGame.screen.blit(textEle, [80, 355])
    wGame.screen.blit(textEleNum, [82, 372])

    wGame.screen.blit(textCRM, [145, 80])
    wGame.screen.blit(textRWS, [215, 80])
    wGame.screen.blit(textNORM, [280, 80])
    wGame.screen.blit(textOVRD, [350, 80])
    wGame.screen.blit(textCNTL, [425, 80])

    wGame.screen.blit(textSWAP, [145, 500])
    wGame.screen.blit(textFCR, [220, 500])
    wGame.screen.blit(textTEST, [285, 500])
    wGame.screen.blit(textDTE, [360, 500])
    wGame.screen.blit(textDCLT, [425, 500])

    wGame.screen.blit(textCONT, [475, 190])

    for i in range(7):
        if i == 3:
            pg.draw.line(wGame.screen, fontColorWhite, (115, 195+35*i),(130, 195+35*i),2)
        else:
            pg.draw.line(wGame.screen, fontColorWhite, (115, 195+35*i),(125, 195+35*i),2)
    for i in range(7):
        if i == 3:
            pg.draw.line(wGame.screen, fontColorWhite, (200+35*i, 483),(200+35*i, 498),2)
        else:
            pg.draw.line(wGame.screen, fontColorWhite, (200+35*i, 488),(200+35*i, 498),2)

def drawSearchAzi(xL, xP):
    pg.draw.line(wGame.screen, colorDBlue, (xL, 120), (xL, 495), 2)
    pg.draw.line(wGame.screen, colorDBlue, (xP, 120), (xP, 495), 2)

def drawSearchAziIco(x):
    i = 6 
    pg.draw.line(wGame.screen, colorDBlue, (x, 485), (x, 495), 4)
    pg.draw.line(wGame.screen, colorDBlue, (x-i, 485), (x+i, 485), 4)

def drawSearchEleIco(y):
    i = 6
    pg.draw.line(wGame.screen, colorDBlue, (117, y), (127, y), 4)
    pg.draw.line(wGame.screen, colorDBlue, (127, y-i), (127, y+i), 4)

def drawAimIco(x, y):
    i = 12
    k = 10
    j = 4
    pg.draw.line(wGame.screen, fontColorWhite, (x-k, y-i), (x-k, y+i), 2)
    pg.draw.line(wGame.screen, fontColorWhite, (x+k, y-i), (x+k, y+i), 2)
    wGame.screen.blit(textaimUpRange, [x+k+j, y-4*j])
    wGame.screen.blit(textaimDownRange, [x+k+j, y])
   
def drawFriend(i):
    x = wWindow/2+objectsFriend[i][1]*pxScaleAzi
    y = (hWindow-wFrame)-objectsFriend[i][0]*pxScaleDis
    imageRot = pg.transform.rotate(arrayFriendImg[i], objectsFriend[i][3]*-1)    
    wGame.screen.blit(imageRot, [x, y])
    textDistFriend = fontDistSet.render(str(int(objectsFriend[i][0])), False, colorFriend)
    wGame.screen.blit(textDistFriend, [x+5, y+30])

def drawFoe(i):
    x = wWindow/2+objectsFoe[i][1]*pxScaleAzi
    y = (hWindow-wFrame)-objectsFoe[i][0]*pxScaleDis    
    imageRot = pg.transform.rotate(arrayFoeImg[i], objectsFoe[i][3]*-1)    
    wGame.screen.blit(imageRot, [x, y])
    textDistFoe = fontDistSet.render(str(int(objectsFoe[i][0])), False, colorFoe)
    wGame.screen.blit(textDistFoe, [x+5, y+30])

def drawRoam(i):
    x = wWindow/2+objectsRoam[i][1]*pxScaleAzi
    y = (hWindow-wFrame)-objectsRoam[i][0]*pxScaleDis
    imageRot = pg.transform.rotate(arrayRoamImg[i], objectsRoam[i][3]*-1)    
    wGame.screen.blit(imageRot, [x, y])
    textDistRoam = fontDistSet.render(str(int(objectsRoam[i][0])), False, colorRoam)
    wGame.screen.blit(textDistRoam, [x+5, y+30])
    
# Init PyGame and UDP
#run = input('Is simulation enabled to start? y/n: \n')
run = 'y'
if run == 'y':
    run = True
    wGame = Cockpit(wWindow, hWindow)
    myUDP = UDPConnection("127.0.0.1", 8000)
    myUDP.connect()
else:
    run = False
    print('Exit')

while run:
    # Ctrl + C to terminate
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    # graphic init
    wGame.cockpit()
    
    # event handling 
    keys = pg.key.get_pressed()
    # button event
    if Button1.draw():
        print('1')
        if FCR == True and clickDis<=2:
            clickDis += 1    
            if clickDis == 3:
                scanDistance = scanDistanceCalc
            elif clickDis == 2:
                scanDistance = (scanDistanceCalc*3)/4
            elif clickDis == 1:
                scanDistance = scanDistanceCalc/2
        if FCR == False:
            FCR = True
    if Button2.draw():
        print('2')
        if FCR == True and clickDis>0:    
            if clickDis == 3:
                scanDistance = (scanDistanceCalc*3)/4
            elif clickDis == 2:
                scanDistance = scanDistanceCalc/2
            elif clickDis == 1:
                scanDistance = scanDistanceCalc/4             
            clickDis -= 1   
    if Button3.draw():
        print('3')
        if FCR == True:
            clicksScanAzi += 1              
            if clicksScanAzi == 1:
                scanAzi = 3
                scanAziLeft = -30
                scanAziRight = 30                
            elif clicksScanAzi == 2:
                scanAzi = 1
                scanAziLeft = -10
                scanAziRight = 10
            else:
                clicksScanAzi = 0
                scanAzi = 6
                scanAziLeft = -60
                scanAziRight = 60                       
    if Button4.draw():
        print('4')
        if FCR == True:
            clicksScanEle += 1              
            if clicksScanEle == 1:
                scanEle = 1
                scanEleUp = 4.9/2
                scanEleDown = -4.9/2
            elif clicksScanEle == 2:
                scanEle = 2
                scanEleUp = 12/2
                scanEleDown = -12/2
            else:
                clicksScanEle = 0
                scanEle = 4
                scanEleUp = 26.2/2
                scanEleDown = -26.2/2
            scanEleUp_ = scanEleUp
    if Button5.draw():
        print('5')
    if Button6.draw():
        print('6')
    if Button7.draw():
        print('7')    
    if Button8.draw():
        print('8')
    if Button9.draw():
        print('9')
    if Button10.draw():
        print('10')
    if Button11.draw():
        print('11')
    if Button12.draw():
        print('12')
    if Button13.draw():
        print('13')    
    if Button14.draw():
        print('14')
    if Button15.draw():
        print('15')
    if Button16.draw():
        print('16') 
    if Button17.draw():
        print('17')        
    if Button18.draw():
        print('18')
    if Button19.draw():
        print('19')
    if Button20.draw():
        print('20')
    # keyboard event
    # Azi
    if keys[pg.K_h]:
        if scanAziRight < scanAzimuth:   
            scanAziLeft += scanAziStep
            scanAziRight += scanAziStep
    if keys[pg.K_f]:
        if scanAziLeft > -scanAzimuth:
            scanAziLeft -= scanAziStep
            scanAziRight -= scanAziStep
    # Ele
    if keys[pg.K_g]:
        if scanEleUp < scanElevation:   
            scanEleUp += scanEleStep
            scanEleDown += scanEleStep
            #scanEleUp_ -= scanEleStep
            #scanEleDown_ -= scanEleStep
    if keys[pg.K_t]:
        if scanEleDown > -scanElevation:
            scanEleUp -= scanEleStep
            scanEleDown -= scanEleStep
            #scanEleUp_ += scanEleStep
            #scanEleDown_ + scanEleStep
    # Aim
    if keys[pg.K_RIGHT]:
        if xScanAim < searchAziRight:
            xScanAim += scanAimStep
    if keys[pg.K_LEFT]:
        if xScanAim > searchAziLeft:
            xScanAim -= scanAimStep
    if keys[pg.K_UP]:
        if yScanAim > searchAimUp:
            yScanAim -= scanAimStep
            #yScanAim_ += scanAimStep
            #aimDist = yScanAim_/pxScaleDis
    if keys[pg.K_DOWN]:
        if yScanAim < searchAimDown:
            yScanAim += scanAimStep
            #yScanAim_ -= scanAimStep
            #aimDist = yScanAim_/pxScaleDis

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
    allTargets, friendsTarget, foeTarget, roamTarget = int(message[19]), int(message[20]),  int(message[21]),  int(message[22])

    if allTargets > 0:

        # Calculate
        if friendsTarget > 0:
            for i in range(friendsTarget):
                if indexFriend > 0:    
                    objectsFriend[indexFriend-1][0] = distFriend/1000
                    objectsFriend[indexFriend-1][1] = aziFriend
                    objectsFriend[indexFriend-1][2] = eleFriend*-1
                    objectsFriend[indexFriend-1][3] = angleToPawnFriend
                    objectsFriend[indexFriend-1][4] = altFriend
                    objectsFriend[indexFriend-1][5] = indexFriend

        if foeTarget > 0:        
            for i in range(foeTarget):
                if indexFoe > 0: 
                    objectsFoe[indexFoe-1][0] = distFoe/1000
                    objectsFoe[indexFoe-1][1] = aziFoe
                    objectsFoe[indexFoe-1][2] = eleFoe*-1
                    objectsFoe[indexFoe-1][3] = angleToPawnFoe
                    objectsFoe[indexFoe-1][4] = altFoe
                    objectsFoe[indexFoe-1][5] = indexFoe
 
        if roamTarget > 0:
            for i in range(roamTarget):
                if indexRoam > 0: 
                    objectsRoam[indexRoam-1][0] = distRoam/1000
                    objectsRoam[indexRoam-1][1] = aziRoam
                    objectsRoam[indexRoam-1][2] = eleRoam*-1
                    objectsRoam[indexRoam-1][3] = angleToPawnRoam
                    objectsRoam[indexRoam-1][4] = altRoam
                    objectsRoam[indexRoam-1][5] = indexRoam


        # Refresh variables and text
        pxScaleDis = (hWindow-wFrame*2)/scanDistance
        searchAziLeft = wWindow/2+scanAziLeft*pxScaleAzi
        searchAziRight = wWindow/2+scanAziRight*pxScaleAzi
        searchEleDown = hWindow/2+scanEleDown*pxScaleEle/2
        searchEleUp = hWindow/2+scanEleUp*pxScaleEle/2
        #aimUpRange = altPawn/100 + np.tan(np.deg2rad(scanEleUp_))*aimDist 
        #aimDownRange = altPawn/100 + np.tan(np.deg2rad(scanEleUp_/2))*aimDist

        textDist = fontSet.render(str(round(scanDistance)), False, fontColorWhite)
        textAziNum = fontSet.render(str(round(scanAzi)), False, fontColorWhite)
        textEleNum = fontSet.render(str(round(scanEle)), False, fontColorWhite)
        textaimUpRange = fontDistSet.render(str(int(aimUpRange)), False, fontColorWhite)
        textaimDownRange = fontDistSet.render(str(int(aimDownRange)), False, fontColorWhite)


        if FCR == True:
            FCRMenu()
            # Draw targets
            for i in range(friendsTarget):
                if ((-scanAzimuth<=objectsFriend[i][1]<=scanAzimuth) and (-scanElevation<=objectsFriend[i][2]<=scanElevation)
                                                                     and (objectsFriend[i][0]<scanDistance)):
                    if scanAziLeft<objectsFriend[i][1]<scanAziRight  and scanEleDown<objectsFriend[i][2]<scanEleUp:
                        drawFriend(i)
            for i in range(foeTarget):
                if ((-scanAzimuth<=objectsFoe[i][1]<=scanAzimuth) and (-scanElevation<=objectsFoe[i][2]<=scanElevation)
                                                                  and (objectsFoe[i][0]<scanDistance)):
                    if scanAziLeft<objectsFoe[i][1]<scanAziRight and scanEleDown<objectsFoe[i][2]<scanEleUp:    
                        drawFoe(i)
            for i in range(roamTarget):
                if ((-scanAzimuth<=objectsRoam[i][1]<=scanAzimuth) and (-scanElevation<=objectsRoam[i][2]<=scanElevation)
                                                                   and (objectsRoam[i][0]<scanDistance)):
                    if scanAziLeft<objectsRoam[i][1]<scanAziRight and scanEleDown<objectsRoam[i][2]<scanEleUp:
                        drawRoam(i)
            
            # Draw search azimuth lines
            if scanAzi < 6:
                drawSearchAzi(searchAziLeft, searchAziRight)

            # Draw antenna search azi ico
            xSearchAzi += xSearchAziStep
            if xSearchAzi<=searchAziLeft:
                xSearchAziStep = xSearchAziStep_
                
            elif xSearchAzi>=searchAziRight:
                xSearchAziStep = -xSearchAziStep_
            drawSearchAziIco(xSearchAzi)

            # Draw antenna search ele ico
            if scanEle == 1:
                ySearchEle = (searchEleDown+searchEleUp)/2
            elif scanEle == 2:
                if indexDel == 50:
                    ySearchEle = searchEleUp
                elif indexDel == 100:
                    ySearchEle = searchEleDown 
            else:
                if indexDel == 33:
                    ySearchEle = searchEleUp
                elif indexDel == 66:
                    ySearchEle = searchEleDown 
                elif indexDel == 99:
                    ySearchEle = (searchEleDown+searchEleUp)/2
            drawSearchEleIco(ySearchEle)
            
            # Draw aim ico 
            drawAimIco(xScanAim, yScanAim)

        else:    
            OpenMenu()
            

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