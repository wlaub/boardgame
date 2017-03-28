import pygame
from pygame.locals import *
import ui
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

        self.wsize = (1280,720)
        self.screen = pygame.Surface(self.size)

        self.drawscreen = pygame.display.set_mode(self.wsize)
        self.pos = (640,360)

        self.things = []

        self.done = False

        self.bgcolor = (255,255,255)

        self.mpos = (0,0)
        self.update_areas()
        self.panning = False
        self.poff = (0,0)

        msize = 200
        self.minimap = ui.Minimap(self, (self.wsize[0]-msize, self.wsize[1]-msize), (msize, msize) )

    def render(self):
        """
        Render the display area to the display screen
        """
        ul= ( max(0,int(self.pos[0]-self.wsize[0]/2.))
            , max(0,int(self.pos[1]-self.wsize[1]/2.))
            )


        self.drawscreen.fill(self.bgcolor)
 
        self.drawscreen.blit(self.screen, (0,0), area = pygame.Rect(ul,self.wsize))
        self.minimap.draw(self.screen, self.drawscreen)

    """
    def minimap(self, area):
        ratx = area[2]/float(self.size[0])
        raty = area[3]/float(self.size[1])
        pos = ((self.pos[0]-self.wsize[0]/2)*ratx, (self.pos[1]-self.wsize[1]/2)*raty)
        mini = pygame.transform.smoothscale(self.screen, (area[2], area[3]))

        self.drawscreen.blit(mini, (area[0], area[1]))
        pygame.draw.rect(self.drawscreen, (0,0,0), area, 1)
        pygame.draw.rect(self.drawscreen, (0,0,0)
                        , (area[0]+pos[0], area[1]+pos[1], self.wsize[0]*ratx, self.wsize[1]*raty), 1)
    """

    def update_areas(self):
        ul= ( min(0, self.pos[0]-self.wsize[0]/2.)
            , min(0, self.pos[1]-self.wsize[1]/2.)
            )
        self.draw_off = (self.pos[0] + ul[0], self.pos[1] + ul[1])

    def get_mouse(self):
        return self.relmpos

    def translate_mouse(self, pos):

        val = [int(pos[i]+self.pos[i]-self.wsize[i]/2.) for i in range(2)]
        self.relmpos = tuple(val)

    def pan(self, rel):
        self.pos = (max(self.wsize[0]/2,self.pos[0] - rel[0]), max(self.wsize[1]/2,self.pos[1] - rel[1]))
#        self.update_areas()

    def event(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            self.wsize = event.size
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.panning =True
                self.poff = self.mpos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.panning = False
        return False

    def draw_pre(self):
        pass
    def draw_post(self):
        pass

    def update(self):
        if self.panning:
            self.pan((self.mpos[0] - self.poff[0], self.mpos[1]-self.poff[1]))
            self.poff = self.mpos
        pass

    def run(self):
        while not self.done:
            time.sleep(.01667)
            self.mpos = pygame.mouse.get_pos()
            self.translate_mouse(self.mpos)
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

            self.render()
            pygame.display.flip()
                

