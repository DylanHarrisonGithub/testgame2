from Point import *
import math

def generateHTMLColor(r,g,b):
    rString = hex(r)[2:]
    gString = hex(g)[2:]
    bString = hex(b)[2:]
    return '#'+rString + gString + bString

class Edge():

    def __init__(self, p0, pf, color):
        self.p0 = p0
        self.pf = pf
        self.color = color
        
    def x(self):
        return self.pf.x - self.p0.x
        
    def y(self):
        return self.pf.y - self.p0.y
    
    def m(self):
        return math.sqrt(self.x()*self.x() + self.y()*self.y())
    
    def setOrigin(self, o):
        cx = self.x()
        cy = self.y()
        self.p0.x = o.x
        self.p0.y = o.y
        self.pf.x = o.x + cx
        self.pf.y = o.y + cy

    def add(self, b):
        self.pf.x = self.p0.x + self.x() + b.x()
        self.pf.y = self.p0.y + self.y() + b.y()
        
    def dot(self, b):
        return self.x()*b.x() + self.y()*b.y()
        
    def det(self, b):
        return self.x()*b.y() - self.y()*b.x()
        
    def getParametric(self, t):
        return Point(self.p0.x + self.x()*t, self.p0.y + self.y()*t)
        
    def setM(self, m):
        self.pf = self.getParametric(m/self.m())
        
    def projOnto(self, b):
        return self.dot(b)/b.m()
        
    def perpFrom(self, b):
        return self.det(b)/b.m()
        
    def getProjVec(self, b):
    
        mSquared = b.x()*b.x() + b.y()*b.y()
        p0 = Point(0.0, 0.0)
        pf = Point(b.x()*self.dot(b)/mSquared, b.y()*self.dot(b)/mSquared)
        
        return Edge(p0, pf, generateHTMLColor(0,0,255))
    
    def getPerpVec(self, b):
    
        mSquared = b.x()*b.x() + b.y()*b.y()
        p0 = Point(0.0, 0.0)
        pf = Point(b.y()*self.det(b)/mSquared, -b.x()*self.det(b)/mSquared)
        
        return Edge(p0, pf, generateHTMLColor(255,255,0))
        
    def fromJSON(self, jsonEdge):
        self.p0 = Point(jsonEdge.p0.x, jsonEdge.p0.y)
        self.pf = Point(jsonEdge.pf.x, jsonEdge.pf.y)
        self.color = jsonEdge.color
    
    def toJSON(self):
        return({"p0": self.p0.toJSON(), "pf": self.pf.toJSON(), "color": self.color})