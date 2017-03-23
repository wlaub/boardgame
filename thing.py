import pygame
from pygame.locals import *

from game import object as gobj
from game import handler as handler
import math, random
import copy

def circle(r, n):
    return [(r*math.cos(6.28*x/n), r*math.sin(6.28*x/n)) for x in range(n)]

def wrap(i, w):
    return (i%int(w), i/int(w))


def snap(val, grid):
    return int(round((float(val)/grid)))*grid

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

    def __init__(self, handler, pos = None, fixed = False, color = 0):
        gobj.Movable.__init__(self, handler, pos, fixed)
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
    valmap = {0:1, 1:4, 2:1}

    size = 20
    grid = size*2+2

    def __init__(self, handler, pos = None, fixed=False, t = 0, q = 2):
        gobj.Rollable.__init__(self, handler, pos, fixed)
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


class Cup(gobj.Rollable):
   
    layer = 1
 
    def __init__(self, handler, pos = None):
        gobj.Rollable.__init__(self, handler, pos, val=0)
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

        self.handler.things.extend(self.stuff)
        self.stuff = []

    def update(self):
        gobj.Rollable.update(self)
        for t in self.handler.things:
            if t.pos == None: 
                import pdb; pdb.set_trace()
 
            if not t.moving and self.get_hit(t.pos):
                if self.add(t):
                    self.handler.things.remove(t)

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


class PlayerBoard(gobj.Board):

    layer = 0
    
    def __init__(self, handler, pos=None, fixed=False):
        gobj.Board.__init__(self, handler, pos, fixed)
        self.gsize = Part.size*2+2
        tg = gobj.Grid((0,32))
        tg.make_grid(-3, 3, -3, 3, self.gsize)
        tg.kinds.append(Part)
        self.grids.append(tg)

        #TODO: Lock coupling is happening again...

        self.size = self.gsize*3.5+40
        
        tg = gobj.Grid((0, -int(self.size)+20))
        tg.locations = [(20*x, 0) for x in range(-5,6)]
        tg.kinds.append(Token)
        self.grids.append(tg)


    def draw(self, screen):
        gobj.Board.draw(self, screen)
        rect = (self.pos[0]-self.size, self.pos[1]-self.size, self.size*2, self.size*2)
        pygame.draw.rect(screen, (0,0,0), rect, 2)


