###########################################################
## File Name: buttons.py                                 ##
## Description: Classes that make buttons and labels     ##
###########################################################

import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 207, 62)
YELLOW = (255, 251, 143)
class Button(object):

    # Initializes the button class
    def __init__(self,rect,outline=BLACK,fill=YELLOW,outlineLen=2):
        self.rect = rect
        self.outline = outline
        self.fill = fill
        self.outlineLen = outlineLen

    # Draws the button
    def draw(self,win):
        pygame.draw.rect(win, self.fill, self.rect, 0)
        pygame.draw.rect(win, self.outline, self.rect, self.outlineLen)

    # Returns the button if it collides with a point
    def collide(self,point):
        if pygame.Rect(self.rect).collidepoint(point):
            return self.rect
        else:
            return -1

class Label(object):

    # Initializes the Label class
    def __init__(self,txt,size=15,align="center",font="yugothicyugothicuilight",colour=BLACK):
        self.txt = txt
        self.size = size
        self.font = font
        self.colour = colour
        self.align = align

    # Draws the labels
    def draw(self,win,rect):
        font =  pygame.font.SysFont(self.font,self.size)
        txtSurface = font.render(self.txt, True, self.colour)
        if self.align == "center":
            x = rect[0] + ((rect[2] / 2) - (txtSurface.get_width() / 2))
            y = rect[1] + ((rect[3] / 2) - (txtSurface.get_height() / 2))
        elif self.align == "left":
            x = rect[0]
            y = rect[1]
        elif self.align == "right":
            x = rect[0] + (rect[2] - txtSurface.get_width())
            y = rect[1]
        win.blit(txtSurface,(x,y))
