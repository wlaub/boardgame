import pygame
from pygame.locals import *
import sys, time, math

class Clickable():
    """
    A thing that catches clicks
    """
    size = 10
    is_ui = False

    def __init__(self, handler, pos):
        self.handler = handler
        self.make_box()
        self.locked = False
        self.moving = False
        if pos == None:
            self.pos = (0,0)
        else:
            self.pos = pos
        self.set_clicks()

    def set_clicks(self):
        self.clicks = [self.left_click, self.middle_click, self.right_click]
    
    def make_box(self):
        self.box = pygame.Rect(-self.size, -self.size, self.size*2, self.size*2)

    def left_click(self, event):
        return False

    def middle_click(self, event):
        return False
 
    def right_click(self, event):
        return False

    def get_move_hit(self, loc):
        return self.box.move(self.pos).collidepoint(loc)

    def update(self):
        pass

    def sort(self):
        pass

    def event(self, event):
        self.mpos = self.handler.get_mouse() if not self.is_ui else self.handler.mpos
        if self.locked: return
        if event.type == MOUSEBUTTONDOWN and event.button < len(self.clicks):
            if self.get_move_hit(self.mpos):
                if self.clicks[event.button-1](event):
                    return True

        return False

    def draw(self, screen):
        pass

    def draw_ui(self, screen):
        pass



class Modal(Clickable):
    """
    Modal dialog that floats on top of everything until dismissed.
    """
    is_ui = True
    size = 200    

    def __init__(self, handler, pos):
        Clickable.__init__(self, handler, pos)
        self.closed = False
        self.escapable = True
        self.handler.add_modal(self)

    def out_click(self, event):
        if self.escapable:
            self.closed = True
 
    def event(self, event):
        self.mpos = self.handler.get_mouse() if not self.is_ui else self.handler.mpos
        if self.locked: return
        if event.type == MOUSEBUTTONDOWN and event.button < len(self.clicks):
            if self.get_move_hit(self.mpos):
                if self.clicks[event.button-1](event):
                    return True
            else:
                if self.out_click(event): return True

        return False

    def draw_ui(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.box.move(self.pos))
        pygame.draw.rect(screen, (0,0,0), self.box.move(self.pos), 2)
        screen.blit( self.handler.font.render("Test", True, (0,0,0))
                    , self.pos)

        pass



class Minimap(Clickable):
    """
    A minimap. Exactly what it sounds like
    """

    def __init__(self, handler, pos, size):        
        self.locked = False
        self.pos = pos
        self.size = size
        self.handler = handler
        self.area = (self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.box = pygame.Rect((0,0), self.area[2:])
        self.set_clicks() 
        self.ratx = self.area[2]/float(handler.size[0])
        self.raty = self.area[3]/float(handler.size[1])
        self.moving = False
 

    def left_click(self, event):
        self.moving = True


    def update(self):
        if self.moving:
            relpos =( self.handler.pos[0] - (self.handler.mpos[0] - self.area[0])/self.ratx
                    , self.handler.pos[1] - (self.handler.mpos[1] - self.area[1])/self.raty
                    )
            self.handler.pan(relpos)

    def event(self, event):
        if Clickable.event(self, event): return True
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.moving = False

        return False


    def draw(self, source, dest):
        handler = self.handler
        pos =   ( (handler.pos[0]-handler.wsize[0]/2)*self.ratx
                , (handler.pos[1]-handler.wsize[1]/2)*self.raty)
        mini = pygame.transform.smoothscale(source, (self.area[2], self.area[3]))

        dest.blit(mini, (self.area[0], self.area[1]))
        pygame.draw.rect(dest, (0,0,0), self.box.move(self.pos), 1)
        pygame.draw.rect(dest, (0,0,0)
                    ,   ( self.area[0]+pos[0], self.area[1]+pos[1]
                        , handler.wsize[0]*self.ratx, handler.wsize[1]*self.raty), 1)

       
