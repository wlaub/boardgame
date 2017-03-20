import pygame
from pygame.locals import *
import sys, time, math
import pickle

import thing
import game.object

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)

size = (1000,600)
center = (size[0]/2, size[1]/2)
screen = pygame.display.set_mode(size)

gs = thing.Part.grid*7+40
gpos = (size[0] - gs, size[1]-gs)

start = [0,0,0,1,2,4,5]

things = []

cup = thing.Cup(things, center)
things.append(cup)

trash = thing.Cup(things, (100,150))
trash.color = (255,0,0)
trash.kinds.append(thing.Token)
things.append(trash)

for i, t in enumerate(start):
    temp = thing.Part(things,(center[0] + i*40, center[1]), t)
    cup.add(temp)

for i in range(len(thing.Token.colors)):
    temp = thing.Token((32+i*16, 12), i, True)
    things.append(temp)

for i in range(len(thing.Part.colors)):
    temp = thing.Part(things, (22+i*42, 50), i, fixed = True)
    things.append(temp)


temp = game.object.Rollable(center)
things.append(temp)

while 1:

    time.sleep(.01)
    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        caught= False
        for t in things[::-1]:
            if t.event(event):
                caught=True
                break
        if not caught:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == KEYDOWN:
                if event.key >= K_1 and event.key <= K_9:
                    pass

    for t in things:
        t.update()
        if not t.moving and cup.get_hit(t.pos):
            if cup.add(t):
                things.remove(t)
        if not t.moving and trash.get_hit(t.pos):
            if trash.add(t):
                trash.stuff = []
                things.remove(t)

    things.sort(key=lambda x: x.layer)

    screen.fill((255,255,255))

    thing.Part.draw_grid(screen, gpos)

    for t in things:
        t.draw(screen)

    pygame.display.flip()
    

