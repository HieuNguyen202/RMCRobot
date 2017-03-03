import pygame
import math
import threading
import time
import os
from Utility import *
class DashBoard(object):
    'The frame'
    def __init__(self, width,height):
        self.edge=20
        self.width=width
        self.height=height
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.darkBlue = (0,0,128)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.pink = (255,200,200)
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.bgColor=self.white
        pygame.mouse.set_visible(1)
        self.f1=pygame.font.SysFont("comicsansms",24)                        
    def put(self, image,loCode, offset=None):
        if offset!=None: self.screen.blit(image,self.locate(loCode,offset,image))
        else: self.screen.blit(image,self.locate(loCode,(0,0),image))
    def locate(self, loCode,offset=None,image=None):
        x1=self.edge
        x2=(self.width/2)
        x3=self.width-self.edge
        y1=self.height-self.edge
        y2=(self.height/2)
        y3=self.edge
        center=(self.width/2,self.height/2)
        if image!=None:
            x2=x2-image.get_rect().centerx
            x3=x3-image.get_rect().width
            y1=y1-image.get_rect().height
            y2=y2-image.get_rect().centery
            center=(center[0]-image.get_rect().centerx,center[1]-image.get_rect().centery)
        if loCode==1: location=(x1,y1)
        elif loCode==2: location=(x2,y1)
        elif loCode==3: location=(x3,y1)
        elif loCode==4: location=(x1,y2)
        elif loCode==5: location=center
        elif loCode==6: location=(x3,y2)
        elif loCode==7: location=(x1,y3)
        elif loCode==8: location=(x2,y3)
        elif loCode==9: location=(x3,y3)
        else: location=(0,0)
        if offset!=None: return (location[0]+offset[0],location[1]+offset[1])
        else: return location
    def rectLocate(self, loCode,offset=None,image=None):
        if offset!=None: location=self.locate(loCode,(0,0),image)
        else: location = self.locate(loCode,offset,image)      
        return (location[0],location[1],image.get_rect().width,image.get_rect().height)



class RMCDashBoard(DashBoard):
    'Communication between two devices using python'
    def __init__(self, width,height):
        super().__init__(width,height)
        pygame.display.set_caption('IIT RMC Team')
        pygame.mouse.set_visible(1)
        
        self.iConnected = pygame.image.load(os.path.join('images', 'wifi.png'))
        self.iConnected =pygame.transform.scale(self.iConnected , (144, 124))
        self.iDisconnected = pygame.image.load(os.path.join('images', 'iitoff.png'))
        self.iMotor = pygame.image.load(os.path.join('images', 'motor.png'))
        self.iMotor = pygame.transform.scale(self.iMotor , (100, 100))
        self.iArm = pygame.image.load(os.path.join('images', 'arm.png'))
        self.iArm = pygame.transform.scale(self.iArm , (100, 100))
        self.iXbox = pygame.image.load(os.path.join('images', 'xbox.png'))
        self.iLogo = pygame.image.load(os.path.join('images', 'iitlogo.png'))
        self.screen.fill(self.bgColor)
        self.logo()
        self.motor(2)
        self.arm(2)
        self.mb=MessageBox(self.screen,(500,500),self.f1)

    def display(self,message):
        self.mb.display(message)
    def connected(self):
        self.put(self.iConnected,6,(0,100))
        pygame.display.update()
    def disconnected(self):
        pygame.draw.rect(self.screen,self.bgColor,self.rectLocate(6,(0,100),self.iConnected,))
        pygame.display.update()
    def motor(self,level):
        dist=100
        if level>=1:
            self.put(self.iMotor,2,(-dist,0))
            if level>=2:
                self.put(self.iMotor,2,(0,0))
                if level>=3:
                    self.put(self.iMotor,2,(dist,0))
        pygame.display.update()
    def arm(self,level):
        dist=100
        if level>=1:
            self.put(self.iArm,2,(-dist,-100))
            if level>=2:
                self.put(self.iArm,2,(0,-100))
                if level>=3:
                    self.put(self.iArm,2,(dist,-100))
        pygame.display.update()
    def xboxConnected(self):
        self.put(self.iXbox,6,(0,0))
        pygame.display.update()
    def xboxDisconnected(self):
        pygame.draw.rect(self.screen,self.bgColor,self.rectLocate(6,(0,0)+self.iXbox))
        pygame.display.update()
    def logo(self):
        self.put(self.iLogo,8,(0,0))
        pygame.display.update()
    def __str__(self):
        return "Nothing so toString"

class MessageBox:
    ''
    def __init__(self,screen,location,front,bg=None):
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.pink = (255,200,200)
        self.red = (255,0,0)
        self.bgColor=self.white

        self.front=front
        self.screen=screen
        self.location=location
        if bg!=None:self.bg=bg
        else:
            self.bg=pygame.draw.rect(self.screen,self.bgColor,pygame.Rect(self.location,(800,200)))       
        
        self.l1=""
        self.l2=""
        self.l3=""
        self.text=self.front.render("",True,self.red)
        self.gap=30


    def display(self,message):
        try:
            self.screen.blit(self.bg,self.location)
        except:
            pygame.draw.rect(self.screen,self.bgColor,pygame.Rect(self.location,(800,200)))

        self.l3=self.l2
        self.text=self.front.render(self.l3,True,self.red)
        self.screen.blit(self.text,(self.location[0],self.location[1]))

        self.l2=self.l1
        self.text=self.front.render(self.l2,True,self.red)
        self.screen.blit(self.text,(self.location[0],self.location[1]+self.gap))

        self.l1=message
        self.text=self.front.render(self.l1,True,self.red)
        self.screen.blit(self.text,(self.location[0],self.location[1]+2*self.gap))
        
        pygame.display.update() 
#class SpeedRMCDashBoard(DashBoard):
#    'Communication between two devices using python'
#    def __init__(self, width,height):
#        super().__init__(width,height)
#        #self.x = x
#        #self.y = y
#        #self.r = r
#        #self.numIncrement = numIncrement
#        self.edge=20
#        self.width=width
#        self.height=height
#        self.red = (255,0,0)
#        self.green = (0,255,0)
#        self.blue = (0,0,255)
#        self.darkBlue = (0,0,128)
#        self.white = (255,255,255)
#        self.black = (0,0,0)
#        self.pink = (255,200,200)
#        self.screen = pygame.display.set_mode((self.width,self.height))
#        self.bgColor=self.white
#        pygame.display.update()
#        pygame.display.set_caption('Monkey Fever')
#        pygame.mouse.set_visible(1)
#        self.background = pygame.Surface(self.screen.get_size())
#        self.f1=pygame.font.SysFont("comicsansms",24)                        
#        self.screen.fill(self.bgColor)
#        pygame.display.update()
#        self.scale=Scale(0,255)
#        self.currentSpeed=0
#        self.preSpeed=self.currentSpeed
#        self.iConnected = pygame.image.load(os.path.join('images', 'wifi.png'))
#        self.iConnected =pygame.transform.scale(self.iConnected , (144, 124))
#        self.iDisconnected = pygame.image.load(os.path.join('images', 'iitoff.png'))
#        self.iMotor = pygame.image.load(os.path.join('images', 'motor.png'))
#        self.iMotor = pygame.transform.scale(self.iMotor , (100, 100))
#        self.iArm = pygame.image.load(os.path.join('images', 'arm.png'))
#        self.iArm = pygame.transform.scale(self.iArm , (100, 100))
#        self.iXbox = pygame.image.load(os.path.join('images', 'xbox.png'))
#        self.iLogo = pygame.image.load(os.path.join('images', 'iitlogo.png'))
#        #picture = pygame.transform.scale(picture, (1280, 720))
#        self.logo()
#        self.motor(2)
#        self.arm(2)
#        self.lastMessage=self.f1.render("",True,self.red)
#        self.mb=MessageBox(self.f1,self.screen,self.iLogo)
#        #print space_ship_rect.x, space_ship_rect.y, 
#        #print space_ship_rect.centerx, space_ship_rect.centery, 
#        #print space_ship_rect.center
#        #print space_ship_rect.left, space_ship_rect.right
#        #print space_ship_rect.top, space_ship_rect.bottom
#        #print space_ship_rect.topleft, space_ship_rect.bottomright
#        #print space_ship_rect.width, space_ship_rect.height
    
#        #a=100
#    #if pygame.key.get_focused():
#    #    press=pygame.key.get_pressed()
#    #    for i in range(0,len(press)): 
#    #        if press[i]==1:
#    #            name=pygame.key.name(i)
#    #            text=f1.render(name,True,(0,0,0))
#    #            screen.blit(text,(100,a))
#    #            a=a+100
#    #pygame.display.update()

#    def display(self,message):
#        self.mb.display(message)

#    def connected(self):
#        self.put(self.iConnected,6,(0,100))
#        pygame.display.update()
#    def disconnected(self):
#        pygame.draw.rect(self.screen,self.bgColor,self.rectLocate(self.iConnected,6,(0,100)))
#        pygame.display.update()
#    def motor(self,level):
#        dist=100
#        if level>=1:
#            self.put(self.iMotor,2,(-dist,0))
#            if level>=2:
#                self.put(self.iMotor,2)
#                if level>=3:
#                    self.put(self.iMotor,2,(dist,0))
#        pygame.display.update()
#    def arm(self,level):
#        dist=100
#        if level>=1:
#            self.put(self.iArm,2,(-dist,-100))
#            if level>=2:
#                self.put(self.iArm,2,(0,-100))
#                if level>=3:
#                    self.put(self.iArm,2,(dist,-100))
#        pygame.display.update()
#    def xboxConnected(self):
#        self.put(self.iXbox,6)
#        pygame.display.update()
#    def xboxDisconnected(self):
#        pygame.draw.rect(self.screen,self.bgColor,self.rectLocate(self.iXbox,6))
#        pygame.display.update()
#    def logo(self):
#        self.put(self.iLogo,8)
#        pygame.display.update()
#    def put(self, image,loCode, offset=None):
#        if offset!=None: self.screen.blit(image,self.locate(image,loCode,offset))
#        else: self.screen.blit(image,self.locate(image,loCode))
#    def locate(self, image,loCode,offset=None):
#        x1=self.edge
#        x2=(self.width/2)-image.get_rect().centerx
#        x3=self.width-image.get_rect().width-self.edge
#        y1=self.height-self.edge-image.get_rect().height
#        y2=(self.height/2)-image.get_rect().centery
#        y3=self.edge
#        center=(self.width/2-image.get_rect().centerx,self.height/2-image.get_rect().centery)
#        if loCode==1: location=(x1,y1)
#        elif loCode==2: location=(x2,y1)
#        elif loCode==3: location=(x3,y1)
#        elif loCode==4: location=(x1,y2)
#        elif loCode==5: location=center
#        elif loCode==6: location=(x3,y2)
#        elif loCode==7: location=(x1,y3)
#        elif loCode==8: location=(x2,y3)
#        elif loCode==9: location=(x3,y3)
#        else: location=(0,0)
#        if offset!=None: return (location[0]+offset[0],location[1]+offset[1])
#        else: return location
#    def rectLocate(self, image,loCode,offset=None):
#        if offset!=None: location=self.locate(image,loCode)
#        else: location = self.locate(image,loCode,offset)      
#        return (location[0],location[1],image.get_rect().width,image.get_rect().height)

#    def __str__(self):
#        return "Nothing so toString"
#    def run(self):
#        while True:
#            if self.currentSpeed!=self.preSpeed:
#                display()
#                self.preSpeed=self.currentSpeed
#    def Olddisplay(self,currentSpeed=None):
#        if currentSpeed==None:
#            currentSpeed=self.currentSpeed
#        pygame.draw.circle(self.screen, self.bgColor, (self.x,self.y), self.r)
#        for i in range(0,currentSpeed):
#            self.drawTri(i)
#            self.update()
#    def getTheta(self, n):
#        return -(math.pi-(math.pi/self.numIncrement)*n)
#    def getX(self, n):
#        return self.r*math.cos(self.getTheta(n))
#    def getY(self, n):
#        return self.r*math.sin(self.getTheta(n))
#    def dist(self, p1,p2):
#        return math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2))
#    def incenter(self, vertices):
#        AB=dist(vertices[0],vertices[0])
#        BC=dist(vertices[1],vertices[1])
#        AC=dist(vertices[2],vertices[2])
#        xA=vertices[0][0]
#        xB=vertices[2][0]
#        xC=vertices[3][0]
#        yA=vertices[0][1]
#        yB=vertices[2][1]
#        yC=vertices[3][1]
#        sumSide=AB+BC+AC
#        return ((AB*xC+BC*xA+AC*xB)/(sumSide),(AB*yC+BC*yA+AC*yB)/(sumSide))

#    def drawTri(self,n):
#        vertices=((self.x,self.y),(self.getX(n)+self.x,self.getY(n)+self.y),(self.getX(n+1)+self.x,self.getY(n+1)+self.y))
#        color=(200,self.scale.scale(math.fabs(n),0,127),0)
#        pygame.draw.polygon(self.screen, color, vertices)
        
#    def update(self):
#        pygame.display.update()
#    def setSpeed(self,speeds):
#        self.currentSpeed=int((math.fabs(speeds[0])+math.fabs(speeds[1]))/2)
