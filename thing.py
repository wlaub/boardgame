import pygame
from pygame.locals import *

import math, random
import copy

def circle(r, n):
    return [(r*math.cos(6.28*x/n), r*math.sin(6.28*x/n)) for x in range(n)]

def wrap(i, w):
    return (i%int(w), i/int(w))


def snap(val, grid):
    return int(round((float(val)/grid)))*grid

class Thing():
    """
    A movable thing
    """
    size = 10
    layer = 0

    def __init__(self, pos, things, fixed=False):
        self.moving = False
        self.things = things
        self.fixed = fixed
        if pos == None:
            self.pos = (0,0)
        else:
            self.pos = pos

    def get_hit(self, loc):
        for i in range(len(loc)):
            if abs(self.pos[i] - loc[i]) > self.size:
                return False
        return True

    def event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.fixed:
                temp = copy.copy(self)
                self.things.append(temp)
                self.fixed = False
            if self.get_hit(event.pos):
                self.offset = (self.pos[0] - event.pos[0], self.pos[1] - event.pos[1])
                self.moving = True
                return True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.moving = False

        return False

    def update(self):
        if self.moving:
            mpos = pygame.mouse.get_pos()
            self.pos = (mpos[0] + self.offset[0], mpos[1]+ self.offset[1])
        pass


class Token(Thing):

    colors =[ (255,0,0)
            , (0,255,0)
            , (0,0,255)
            , (0,128,0)
            , (128,0,128)
            , (0,0,128)
            ]

    size = 8

    layer = 10

    def __init__(self, things, pos = None, color = 0, fixed = False):
        Thing.__init__(self, pos, things, fixed)
        self.color = color 

    def draw(self, screen):
        pygame.draw.circle(screen, self.colors[self.color]
            , self.pos, self.size
            ) 


class Part(Thing):
    """
    Movable part class with type and quality
    """

    layer = 5

    names = ['hull', 'engine', 'fission', 'fusion', 'weapon', 'shield']

    colors ={ 0: (128,128,128)  #hull
            , 1: (0,255,0)      #engine
            , 2: (0,0,255)      #reactor1
            , 3: (255,0,255)    #reactor2
            , 4: (0,0,0)        #weapon
            , 5: (255,255,0)    #shield
            }
    tmap = [0,1,1,1,1,2]

    size = 20
    grid = size*2+2

    def __init__(self, things, pos = None, t = 0, q= 2, fixed=False):
        Thing.__init__(self, pos, things, fixed)
        self.type = t
        self.quality = q
        self.snap()

    def roll(self):
        self.quality = self.tmap[random.randint(0,5)]

    def snap(self):
        x = snap(self.pos[0], self.grid)
        y = snap(self.pos[1], self.grid)
        self.pos = (x,y)

 
    def event(self, event):
        if Thing.event(self,event):
            return True
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            if self.get_hit(event.pos):
                self.quality += 1
                if self.quality > 2: self.quality = 0
                return True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.snap()
     
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors[self.type]
            , (self.pos[0]-self.size, self.pos[1] - self.size, self.size*2, self.size*2)
            )
        for x,y in circle(self.size/2., self.quality+1):
            pygame.draw.circle(screen, (255,255,255)
            , (self.pos[0] - int(y), self.pos[1] + int(x))
            , 4)

    def draw_mini(self,screen, pos, size):
        pygame.draw.rect(screen, self.colors[self.type]
            , (pos[0]-self.size, pos[1] - size, size*2, size*2)
            )

    @classmethod
    def draw_grid(cls, screen, pos):
        size = 7
        pos = (snap(pos[0], cls.grid)+cls.grid/2-1, snap(pos[1], cls.grid)+cls.grid/2-1)
        for x in range(size+1):
            x = x
            start = (pos[0]+cls.grid*x, pos[1])
            end = (pos[0]+cls.grid*x, pos[1]+cls.grid*size)
            pygame.draw.line(screen, (0,0,0), start, end, 2)
            start = (pos[0], pos[1]+cls.grid*x)
            end = (pos[0]+cls.grid*size, pos[1]+cls.grid*x)
            pygame.draw.line(screen, (0,0,0), start, end, 2)


class Cup(Thing):
   
    layer = 1
 
    def __init__(self, things, pos = None):
        Thing.__init__(self,pos, things)
        self.stuff = []
        self.size = 60
        self.roll = False
        self.color = (192,192,192)
        self.kinds = [Part]

    def add(self, thing):
        for k in self.kinds:
            if isinstance(thing, k) and not thing.fixed:      
                self.stuff.append(thing)
                return True
        return False

    def do_roll(self):
        for i, t in enumerate(self.stuff):
            off = wrap(i,4)
            off = [off[0]*t.grid + self.size+t.size*2, off[1]*t.grid - self.size+t.size]
            t.pos = (self.pos[0]+off[0], self.pos[1]+off[1])
            t.snap()
            t.roll()
        self.things.extend(self.stuff)
        self.stuff = []
        self.roll = False

    def event(self, event):
        if Thing.event(self,event):
            return True
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            if self.get_hit(event.pos):
                self.roll = True
                return True    
 
        return False


    def draw(self, screen):
        pygame.draw.rect(screen, self.color
            , (self.pos[0]-self.size, self.pos[1] - self.size, self.size*2, self.size*2)
            )
        
        for x,y in circle(self.size/2., len(self.stuff)):
            pygame.draw.circle(screen, (0,0,0)
            , (self.pos[0] - int(y), self.pos[1] + int(x))
            , 4)
        
        for i,t in enumerate(self.stuff):
            off = wrap(i,4)
            size = self.size/4.-1
            grid = 2*self.size/4.
            off = [off[0] * grid - self.size+grid/2+6, off[1] * grid -self.size+grid/2]
            pos = [self.pos[0] + off[0], self.pos[1]+off[1]]
            t.draw_mini(screen, pos, size)
 







