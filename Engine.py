import random
import time
from Point import *
from Edge import *
from Circle import *

class Engine():

    def __init__(self):
        self.points = []
        self.edges = []
        self.circles = []
        self.log = []
        self.soonestCollisionCircle = None
        self.soonestCollisionObject = None
        self.soonestCollisionType = -1
        self.soonestCollisionTime = 999999
        self.deltaTime = 0
        self.stopWatch = -1
        self.isPaused = True
    
    def pause(self):
        self.isPaused = True
        
    def unPause(self):
        self.isPaused = False
        self.stopWatch = time.time()
        
    def determineNextCollision(self):
        
        self.soonestCollisionTime = 99999
        
        for i in range(0, len(self.circles)):
            for j in range(i+1, len(self.circles)):
            
                t = min(self.circles[i].timeToCollideWithCircle(self.circles[j]))
                
                if ((t < self.soonestCollisionTime) and (t > 0.00001)):
                
                    self.soonestCollisionTime = t
                    self.soonestCollisionCircle = self.circles[i]
                    self.soonestCollisionObject = self.circles[j]
                    self.collisionType = 1
                    
        for i in range(0, len(self.circles)):
            for j in range(0, len(self.edges)):
            
                t = min(self.circles[i].timeToCollideWithEdge(self.edges[j]))
                
                if ((t < self.soonestCollisionTime) and (t > 0.00001)):
                
                    self.soonestCollisionTime = t
                    self.soonestCollisionCircle = self.circles[i]
                    self.soonestCollisionObject = self.edges[j]
                    self.collisionType = 2
                    
    def updateState(self):
    
        if (self.isPaused == False):
            self.deltaTime = time.time() - self.stopWatch
            deltaTime = self.deltaTime
        else:
            self.deltaTime = 0
            deltaTime = 0
        
        self.stopWatch = time.time()
        
        self.determineNextCollision()
        
        while (self.soonestCollisionTime < deltaTime):

            for c in self.circles:
                c.move(self.soonestCollisionTime)
                
            if (self.collisionType == 1):
                self.soonestCollisionCircle.collideWithCircle(self.soonestCollisionObject)
            else:
                self.soonestCollisionCircle.deflectFromEdge(self.soonestCollisionObject)
            
            deltaTime -= self.soonestCollisionTime
            self.determineNextCollision()
            
        for c in self.circles:
            c.move(deltaTime)                

        