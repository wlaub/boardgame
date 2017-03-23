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

def dist(pos1, pos2):
    return sum([(pos1[x] - pos2[x])**2 for x in range(len(pos1))])

def add(pos1, pos2):
    return [(pos1[x] + pos2[x]) for x in range(len(pos1))]


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


class Grid():
    """
    A thing that snaps kinds of objects to a set of locations
    """

    kinds = []
    locations = []

    def __init__(self, pos = None, r = 9999999):
        if pos != None:
            self.pos = pos
        else:
            self.pos = (0,0)
        self.range = r

    def make_grid(self, xmin, xmax, ymin, ymax, size):
        """
        Makes a plain old square grid
        """
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self.locations.append((x*size, y*size))


    def add(self, thing, pos):
        if not thing.__class__ in self.kinds: return False
        if thing.fixed: return False
        best = None
        bdist = self.range
        for l in self.locations:
            relpos = add(l, pos)
            tdist = dist(thing.pos, relpos)
            if tdist < bdist:
                best = relpos
                bdist = tdist
        if best != None:
            thing.pos = tuple(best)
            return True
        return False


class Board(Movable):
    """
    A game board that different objects to different locations
    and moves them with itself without making them untargetable
    """

    def __init__(self, handler, pos=None, fixed=False):
        Movable.__init__(self, handler, pos, fixed)
        self.grids = []
        self.things = []        
        self.offsets = {}

    def left_click(self, event):
        result = Movable.left_click(self,event)
        for t in self.things:
            if t.fixed: break
            t.offset = (t.pos[0] - event.pos[0], t.pos[1] - event.pos[1])
            self.offsets[t] = t.offset
        return result


    def update(self):
        """
        Go through all the objects and try attaching them to grids
        """
        Movable.update(self)
        if not self.moving:
            self.offsets.clear()
            for t in self.handler.things:
                if not t.moving:
                    caught = False
                    if self.get_hit(t.pos):
                        for g in self.grids:
                            if g.add(t, self.pos):
                                if not t in self.things:
                                    self.things.append(t)
                                caught = True
                    if not caught and t in self.things:
                        self.things.remove(t)
        if self.moving:
            mpos = pygame.mouse.get_pos()
            for t in self.offsets.keys():
                t.pos = (mpos[0] + self.offsets[t][0], mpos[1]+ self.offsets[t][1])

           


