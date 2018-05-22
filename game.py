#!/home python
# -*- coding: utf-8 -*-
import sys,pygame,random
import threading, time ,cv2
import numpy as np
from pygame.locals import *


class GameState:
    def __init__(self):
        pygame.init()
        global screen,FPS
        
        self.score = 0
        self.traintime = 0
        self.gametime = 1
        self.windowWidth1 = 800
        self.windowHeight1 = 500
        self.windowWidth = 500
        self.windowHeight = 500
        self.cellSize = 20
        self.head = 0
        
        
        
        self.action = np.zeros(5)  #控制参数
        
        screen=pygame.display.set_mode((self.windowWidth1,self.windowHeight1))
        pygame.display.set_caption("Greedy Snake")
        screen.fill((0, 150, 0))
        self.drawgrid()
        image_start = pygame.surfarray.array3d(pygame.display.get_surface())
        reimg = cv2.cvtColor(cv2.resize(image_start[0:500,0:500], (80, 80)), cv2.COLOR_BGR2GRAY)
        ret,reimg = cv2.threshold(reimg,150,255,cv2.THRESH_BINARY)
        self.setimg(reimg)
        self.show()
        self.main()
        pygame.display.update()
        self.FPS=pygame.time.Clock()
        
    def main(self):
        #初始化
        self.startX=self.cellSize*random.randint(8,self.windowWidth/self.cellSize-8)
        self.startY=self.cellSize*random.randint(8,self.windowHeight/self.cellSize-8)
        self.snake=[{'x': self.startX , 'y': self.startY},
               {'x': self.startX - 1 * self.cellSize, 'y': self.startY},
               {'x': self.startX - 2 * self.cellSize, 'y': self.startY},
               {'x': self.startX - 3 * self.cellSize, 'y': self.startY}]
        self.appleX = self.cellSize * random.randint(0, (self.windowWidth / self.cellSize)-1)
        self.appleY = self.cellSize * random.randint(0, (self.windowHeight / self.cellSize)-1)
        
        '''
        while(True):
            if self.flag:
                break
        '''
        
    def frame_step(self,input):
        terminal = False
        
        #self.FPS.tick(15)
        #oldreward = np.sqrt(np.square((self.snake[self.head]['x'] - self.appleX) / self.cellSize) + np.square((self.snake[self.head]['y']-self.appleY) / self.cellSize)) / (np.sqrt(2) * self.cellSize)
        self.action = input
        flag = self.turn()
        if flag:
            self.move()
        #newreward = np.sqrt(np.square((self.snake[self.head]['x'] - self.appleX) / self.cellSize) + np.square((self.snake[self.head]['y']-self.appleY) / self.cellSize)) / (np.sqrt(2) * self.cellSize)
        #reward = oldreward-newreward
        reward = -0.1
        if self.snake[self.head]['x']==self.appleX and self.snake[self.head]['y']==self.appleY:
            self.appleX = self.cellSize * random.randint(0, (self.windowWidth / self.cellSize)-1)
            self.appleY = self.cellSize * random.randint(0, (self.windowHeight / self.cellSize)-1)
            self.eat()
            self.score += 10
            reward = 2
            
        if self.snake[self.head]['x']<0 or self.snake[self.head]['x']>=self.windowWidth or self.snake[self.head]['y']<0 or self.snake[self.head]['y']>=self.windowHeight:
            self.gameOver()
            terminal = True
            reward = -1
        for body in self.snake[1:]:
            if body==self.snake[self.head]:
                self.gameOver()
                terminal = True
                reward = -1    
        self.show()
        self.drawSnake()
            
        pygame.draw.rect(screen, (255,255,0), (self.appleX, self.appleY, self.cellSize, self.cellSize))
        pygame.display.update()
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return image_data ,reward,terminal

    #绘制网格
    def drawgrid(self):
        pygame.draw.line(screen,(0,255,0),(self.windowWidth+1,0),(self.windowWidth+1,self.windowHeight),2)
        for i in xrange(self.cellSize,self.windowWidth,self.cellSize):
            pygame.draw.line(screen,(0,255,0),(i,0),(i,self.windowHeight),1)
        for j in xrange(self.cellSize,self.windowHeight,self.cellSize):
            pygame.draw.line(screen,(0,255,0),(0,j),(self.windowWidth,j),1)
    
    #绘制蛇
    def drawSnake(self):
        for cood in self.snake:
            pygame.draw.rect(screen,(120,120,255),(cood['x'],cood['y'],self.cellSize,self.cellSize))
        pygame.draw.rect(screen,(255,255,0), (self.snake[self.head]['x'], self.snake[self.head]['y'], self.cellSize, self.cellSize))

    def setimg(self,img):
        reimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        roimg = pygame.image.frombuffer(reimg,(80,80), "RGB")
        roimg = pygame.transform.rotate(roimg,90)
        self.imgmap = pygame.transform.flip(roimg,False,True)
        
    def turn(self):
        flag= True
        # 上下转向
        if self.snake[self.head]['y'] == self.snake[1]['y']:
            if self.action[1] == 1:
                del self.snake[-1]
                newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] - self.cellSize}
                self.snake.insert(0, newHead)
                flag = False

            elif self.action[2] == 1:
                del self.snake[-1]
                newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] + self.cellSize}
                self.snake.insert(0, newHead)
                flag = False

        # 左右转向
        if self.snake[self.head]['x'] == self.snake[1]['x']:
            if self.action[3] == 1:
                del self.snake[-1]
                newHead = {'x': self.snake[self.head]['x'] - self.cellSize, 'y': self.snake[self.head]['y']}
                self.snake.insert(0, newHead)
                flag = False

            elif self.action[4] == 1:
                del self.snake[-1]
                newHead = {'x': self.snake[self.head]['x'] + self.cellSize, 'y': self.snake[self.head]['y']}
                self.snake.insert(0, newHead)
                flag = False
        return flag


    def move(self):
        # 向左运动
        if self.snake[self.head]['x'] < self.snake[1]['x']:
            del self.snake[-1]
            newHead = {'x': self.snake[self.head]['x'] - self.cellSize, 'y': self.snake[self.head]['y']}
            self.snake.insert(0, newHead)
        # 向右运动
        elif self.snake[self.head]['x'] > self.snake[1]['x']:
            del self.snake[-1]
            newHead = {'x': self.snake[self.head]['x'] + self.cellSize, 'y': self.snake[self.head]['y']}
            self.snake.insert(0, newHead)
        # 向上运动
        elif self.snake[self.head]['y'] < self.snake[1]['y']:
            del self.snake[-1]
            newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] - self.cellSize}
            self.snake.insert(0, newHead)
        # 向下运动
        elif self.snake[self.head]['y'] > self.snake[1]['y']:
            del self.snake[-1]
            newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] + self.cellSize}
            self.snake.insert(0, newHead)

    def eat(self):
        # 向左运动
        if self.snake[self.head]['x'] < self.snake[1]['x']:
            newHead = {'x': self.snake[self.head]['x'] - self.cellSize, 'y': self.snake[self.head]['y']}
            self.snake.insert(0, newHead)
        # 向右运动
        elif self.snake[self.head]['x'] > self.snake[1]['x']:
            newHead = {'x': self.snake[self.head]['x'] + self.cellSize, 'y': self.snake[self.head]['y']}
            self.snake.insert(0, newHead)
        # 向上运动
        elif self.snake[self.head]['y'] < self.snake[1]['y']:
            newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] - self.cellSize}
            self.snake.insert(0, newHead)
        # 向下运动
        elif self.snake[self.head]['y'] > self.snake[1]['y']:
            newHead = {'x': self.snake[self.head]['x'], 'y': self.snake[self.head]['y'] + self.cellSize}
            self.snake.insert(0, newHead)

    def show(self):
        screen.fill((0, 150, 0))
        self.drawgrid()
        fontObj = pygame.font.Font('font.ttf', 24)
        textSurfaceObj1 = fontObj.render(u'深度Q网络(贪吃蛇)程序', True, (255,255,255))
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (self.windowWidth+150, 50)
        screen.blit(textSurfaceObj1,textRectObj1)
        fontObj1 = pygame.font.Font('font.ttf', 20)
        textSurfaceObj2 = fontObj1.render(u'开发者: 韦行志 ', True,(255,255,255))
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.windowWidth+150, 100)
        screen.blit(textSurfaceObj2,textRectObj2)
        
        textSurfaceObj3 = fontObj1.render(u'训练步数：%s' % self.traintime, True,(255,255,255))
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj3.center = (self.windowWidth+150, 140)
        screen.blit(textSurfaceObj3,textRectObj3)
        
        textSurfaceObj4 = fontObj1.render(u'游戏次数：%s' % self.gametime, True,(255,255,255))
        textRectObj4 = textSurfaceObj4.get_rect()
        textRectObj4.center = (self.windowWidth+150, 180)
        screen.blit(textSurfaceObj4,textRectObj4)
        
        textSurfaceObj5 = fontObj1.render(u'当前得分：%s' % self.score, True,(255,255,255))
        textRectObj5 = textSurfaceObj5.get_rect()
        textRectObj5.center = (self.windowWidth+150, 220)
        screen.blit(textSurfaceObj5,textRectObj5)
        
        textSurfaceObj6 = fontObj.render(u'网络映射', True,(255,255,255))
        textRectObj6 = textSurfaceObj6.get_rect()
        textRectObj6.center = (self.windowWidth+150, 280)
        screen.blit(textSurfaceObj6,textRectObj6)
        
        screen.blit(self.imgmap,(self.windowWidth+40, 350))
        if self.action[0] != 1:
            pygame.draw.rect(screen,(255, 0, 0),(self.windowWidth+140,385,10,10))
        else:
            pygame.draw.rect(screen,(120,120,255),(self.windowWidth+140,385,10,10))    
        if self.action[1] == 1:
            pygame.draw.line(screen,(255, 0, 0),(self.windowWidth+145,390),(self.windowWidth+225,345),1)
            pygame.draw.rect(screen,(255, 0, 0),(self.windowWidth+220,340,10,10))
        else:
            pygame.draw.rect(screen,(120,120,255),(self.windowWidth+220,340,10,10))        
        if self.action[2] == 1:
            pygame.draw.line(screen,(255, 0, 0),(self.windowWidth+145,390),(self.windowWidth+225,375),1)
            pygame.draw.rect(screen,(255, 0, 0),(self.windowWidth+220,370,10,10))
        else:
            pygame.draw.rect(screen,(120,120,255),(self.windowWidth+220,370,10,10))        
        if self.action[3] == 1:
            pygame.draw.line(screen,(255, 0, 0),(self.windowWidth+145,390),(self.windowWidth+225,405),1)
            pygame.draw.rect(screen,(255, 0, 0),(self.windowWidth+220,400,10,10))
        else:
            pygame.draw.rect(screen,(120,120,255),(self.windowWidth+220,400,10,10))
        if self.action[4] == 1:
            pygame.draw.line(screen,(255, 0, 0),(self.windowWidth+145,390),(self.windowWidth+225,435),1)
            pygame.draw.rect(screen,(255, 0, 0),(self.windowWidth+220,430,10,10))
        else:
            pygame.draw.rect(screen,(120,120,255),(self.windowWidth+220,430,10,10))
            
        textSurfaceObj7 = fontObj1.render(u'上', True,(255,255,255))
        textRectObj7 = textSurfaceObj7.get_rect()
        textRectObj7.center = (self.windowWidth+260, 345)
        screen.blit(textSurfaceObj7,textRectObj7)
        
        textSurfaceObj8 = fontObj1.render(u'下', True,(255,255,255))
        textRectObj8 = textSurfaceObj8.get_rect()
        textRectObj8.center = (self.windowWidth+260, 375)
        screen.blit(textSurfaceObj8,textRectObj8)
        
        textSurfaceObj9 = fontObj1.render(u'左', True,(255,255,255))
        textRectObj9 = textSurfaceObj9.get_rect()
        textRectObj9.center = (self.windowWidth+260, 405)
        screen.blit(textSurfaceObj9,textRectObj9)
        
        textSurfaceObj10 = fontObj1.render(u'右', True,(255,255,255))
        textRectObj10 = textSurfaceObj10.get_rect()
        textRectObj10.center = (self.windowWidth+260, 435)
        screen.blit(textSurfaceObj10,textRectObj10)
        
    def trainTime(self,time):
        self.traintime=time #False


    def gameOver(self):
        '''
        screen.fill((0, 150, 0))
        self.drawgrid()
        self.show()
        fontObj = pygame.font.Font('freesansbold.ttf', 60)
        textSurfaceObj1 = fontObj.render('Game over!', True, (255,0,0))
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (self.windowWidth/3, self.windowHeight/3)
        screen.blit(textSurfaceObj1,textRectObj1)
        textSurfaceObj2 = fontObj.render('Score: %s' % (len(self.snake)-4), True, (255, 0, 0))
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.windowWidth*2/3, self.windowHeight*2/3)
        screen.blit(textSurfaceObj2,textRectObj2)
        pygame.display.update()

        while(True):
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
        '''
        self.score = 0
        self.gametime += 1
        self.head = 0
        
        screen.fill((0, 150, 0))
        self.drawgrid()
        image_start = pygame.surfarray.array3d(pygame.display.get_surface())
        reimg = cv2.cvtColor(cv2.resize(image_start[0:500,0:500], (80, 80)), cv2.COLOR_BGR2GRAY)
        ret,reimg = cv2.threshold(reimg,150,255,cv2.THRESH_BINARY)
        self.setimg(reimg)
        self.show()
        self.main()
        pygame.display.update()

