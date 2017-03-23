import pygame
from pygame.locals import *
import sys, time, math
import pickle

import thing
import game.object
import game.handler

class App(game.handler.Handler):

    def __init__(self):
        game.handler.Handler.__init__(self, (1000,600))

        self.gs = thing.Part.grid*7+40
        self.gpos = (self.size[0] - self.gs, self.size[1]-self.gs)

        start = [0,0,0,1,2,4,5]

        self.cup = thing.Cup(self, self.center)
        self.things.append(self.cup)

        self.trash = thing.Cup(self, (100,150))
        self.trash.color = (255,0,0)
        self.trash.kinds.append(thing.Token)
        self.things.append(self.trash)

        for i, t in enumerate(start):
            temp = thing.Part(self, (self.center[0] + i*40, self.center[1]), False, t)
            self.cup.add(temp)

        for i in range(len(thing.Token.colors)):
            temp = thing.Token(self, (32+i*16, 12), True, i)
            self.things.append(temp)

        for i in range(len(thing.Part.colors)):
            temp = thing.Part(self, (22+i*42, 50), True, i, 2)
            self.things.append(temp)


        self.board = thing.PlayerBoard(self, self.center)
        self.things.append(self.board)


    def update(self):
        self.trash.stuff = []

    def draw_pre(self):
        thing.Part.draw_grid(self.screen, self.gpos)

app = App()

app.run()


