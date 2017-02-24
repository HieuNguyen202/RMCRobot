import pygame
import math
from Utility import *
class Dashboard():
    'Communication between two devices using python'
    def __init__(self, x,y, r,numIncrement):
        self.x = x
        self.y = y
        self.r = r
        self.numIncrement = numIncrement
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.darkBlue = (0,0,128)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.pink = (255,200,200)
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.update()
        pygame.display.set_caption('Monkey Fever')
        pygame.mouse.set_visible(1)
        self.background = pygame.Surface(self.screen.get_size())
        #self.f1=pygame.font.SysFont("comicsansms",24)                        
        self.screen.fill(self.black)
        pygame.display.update()
        self.scale=Scale(0,255)


    def __str__(self):
        return "Nothing so toString"
    def getTheta(self, n):
        return -(math.pi-(math.pi/self.numIncrement)*n)
    def getX(self, n):
        return self.r*math.cos(self.getTheta(n))
    def getY(self, n):
        return self.r*math.sin(self.getTheta(n))
    def dist(self, p1,p2):
        return math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2))
    def incenter(self, vertices):
        AB=dist(vertices[0],vertices[0])
        BC=dist(vertices[1],vertices[1])
        AC=dist(vertices[2],vertices[2])
        xA=vertices[0][0]
        xB=vertices[2][0]
        xC=vertices[3][0]
        yA=vertices[0][1]
        yB=vertices[2][1]
        yC=vertices[3][1]
        sumSide=AB+BC+AC
        return ((AB*xC+BC*xA+AC*xB)/(sumSide),(AB*yC+BC*yA+AC*yB)/(sumSide))

    def drawTri(self,n):
        vertices=((self.x,self.y),(self.getX(n)+self.x,self.getY(n)+self.y),(self.getX(n+1)+self.x,self.getY(n+1)+self.y))
        color=(200,self.scale.scale(math.fabs(n),0,127),0)
        pygame.draw.polygon(self.screen, color, vertices)
        
    def update(self):
        pygame.display.update()



