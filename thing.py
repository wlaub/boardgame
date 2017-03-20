import pygame
from pygame.locals import *

from game import object as gobj
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
        self.clicks = [self.left_click, self.middle_click, self.right_click]

    def get_hit(self, loc):
        for i in range(len(loc)):
            if abs(self.pos[i] - loc[i]) > self.size:
                return False
        return True

    def left_click(self, event):
        if self.fixed:
            temp = copy.copy(self)
            self.things.append(temp)
            self.fixed = False
        self.offset = (self.pos[0] - event.pos[0], self.pos[1] - event.pos[1])
        self.moving = True
        return True

    def middle_click(self, event):
        self.roll()
        return True    
 
    def right_click(self, event):
        return False

    def event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.get_hit(event.pos):
                if self.clicks[event.button-1](event):
                    return True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.moving = False

        return False

    def update(self):
        if self.moving:
            mpos = pygame.mouse.get_pos()
            self.pos = (mpos[0] + self.offset[0], mpos[1]+ self.offset[1])
        pass


class Token(gobj.Movable):

    colors =[ (255,0,0)
            , (0,255,0)
            , (0,0,255)
            , (0,128,0)
            , (128,0,128)
            , (0,0,128)
            ]

    size = 8

    layer = 10

    def __init__(self, things, pos = None, fixed = False, color = 0):
        gobj.Movable.__init__(self, things, pos, fixed)
        self.color = color 

    def draw(self, screen):
        pygame.draw.circle(screen, self.colors[self.color]
            , self.pos, self.size
            ) 


class Part(gobj.Rollable):
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
    valmap = {0:0, 1:4, 2:1}

    size = 20
    grid = size*2+2

    def __init__(self, things, pos = None, fixed=False, t = 0, q = 2):
        gobj.Rollable.__init__(self, things, pos, fixed)
        self.type = t


    def snap(self):
        x = snap(self.pos[0], self.grid)
        y = snap(self.pos[1], self.grid)
        self.pos = (x,y)

    def right_click(self, event):
        self.val += 1
        if self.val > 2: self.val = 0
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors[self.type]
            , (self.pos[0]-self.size, self.pos[1] - self.size, self.size*2, self.size*2)
            )
        for x,y in circle(self.size/2., self.val+1):
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
        self.color = (192,192,192)
        self.kinds = [Part]

    def add(self, thing):
        for k in self.kinds:
            if isinstance(thing, k) and not thing.fixed:      
                self.stuff.append(thing)
                return True
        return False

    def roll(self):
        for i, t in enumerate(self.stuff):
            off = wrap(i,4)
            off = [off[0]*t.grid + self.size+t.size*2, off[1]*t.grid - self.size+t.size]
            t.pos = (self.pos[0]+off[0], self.pos[1]+off[1])
            t.roll()
        self.things.extend(self.stuff)
        self.stuff = []

    def event(self, event):
        if Thing.event(self,event):
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
 







