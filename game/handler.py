import pygame
from pygame.locals import *
import sys, time, math


class Handler():
    """
    Primary handler class for all the stuff.
    Should be subclassed for the main application
    """

    def __init__(self, size):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 18)

        self.size = size
        self.center = (size[0]/2, size[1]/2)
        self.screen = pygame.display.set_mode(size)

        self.things = []

        self.done = False

        self.bgcolor = (255,255,255)

    def event(self, event):
        if event.type == pygame.QUIT:
            exit()
        return False

    def draw_pre(self):
        pass
    def draw_post(self):
        pass

    def update(self):
        pass

    def run(self):
        while not self.done:
            time.sleep(.01667)
            mpos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                caught= False
                for t in self.things[::-1]:
                    if t.event(event):
                        caught=True
                        break
                if not caught:
                    self.event(event)

            for t in self.things:
                t.update()

            self.update()

            self.things.sort(key=lambda x: x.sort())

            self.screen.fill(self.bgcolor)

            self.draw_pre()

            for t in self.things:
                t.draw(self.screen)

            self.draw_post()

            pygame.display.flip()
                

