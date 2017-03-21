import pygame
from pygame.locals import *

import math, random
import copy
import handler

def circle(r, n):
    return [(r*math.cos(6.28*x/n), r*math.sin(6.28*x/n)) for x in range(n)]

def wrap(i, w):
    return (i%int(w), i/int(w))

def snap(val, grid):
    return int(round((float(val)/grid)))*grid


class Movable():
    """
    Movable object class. For things you can click and drag
    A fixed object makes an unfixed copy of itself when moved 
    """

    size = 10
    layer = 0

    def __init__(self, handler, pos, fixed=False):
        self.handler = handler
        self.moving = False
        self.fixed = fixed
        if pos == None:
            self.pos = (0,0)
        else:
            self.pos = pos
        self.clicks = [self.left_click, self.middle_click, self.right_click]

    def get_move_hit(self, loc):
        for i in range(len(loc)):
            if abs(self.pos[i] - loc[i]) > self.size:
                return False
        return True

    def get_hit(self, loc):
        for i in range(len(loc)):
            if abs(self.pos[i] - loc[i]) > self.size:
                return False
        return True

    def left_click(self, event):
        if self.fixed:
            temp = copy.copy(self)
            self.handler.things.append(temp)
            self.fixed = False
        self.offset = (self.pos[0] - event.pos[0], self.pos[1] - event.pos[1])
        self.moving = True
        return True

    def middle_click(self, event):
        return False
 
    def right_click(self, event):
        return False

    def event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.get_move_hit(event.pos):
                if self.clicks[event.button-1](event):
                    return True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.moving = False

        return False

    def update(self):
        if self.moving:
            mpos = pygame.mouse.get_pos()
            self.pos = (mpos[0] + self.offset[0], mpos[1]+ self.offset[1])

    def draw(self):
        pygame.draw.rect(screen, (0,0,0)
            , (self.pos[0]-self.size, self.pos[1] - self.size, self.size*2, self.size*2), 1
            )
 


class Rollable(Movable):
    """
    A movable object that can be rolled
    """

    valmap = { x:x for x in range(6)}
    values = None
    layer = 1
    size=20

    def __init__(self, handler, pos=None, fixed=False, val=None):
        Movable.__init__(self, handler, pos, fixed)
        self.generate_values()
        if val != None:
            self.val = val
        else:
            self.roll()

    def generate_values(self):
        if self.values == None:
            self.values = []
            for x, q in self.valmap.iteritems():
                self.values.extend([x]*q)

    def update(self):
        Movable.update(self)

    def roll(self):
        self.val = random.sample(self.values,1)[0]   

    def middle_click(self, event):
        self.roll()
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0)
            , (self.pos[0]-self.size, self.pos[1] - self.size, self.size*2, self.size*2), 1
            )
        for x,y in circle(self.size/2., self.val+1):
            pygame.draw.circle(screen, (0,0,0)
            , (self.pos[0] - int(y), self.pos[1] + int(x))
            , 2)



