#########################################################
## File Name: inputs.py                                ##
## Description: Classes that make different inputs     ##
#########################################################

# Inputs
import pygame, buttons
pygame.init()
from tkinter import *
from tkinter import filedialog

# Parent input class created
class Input(object):
    # Initializes variables
    def __init__(self,question):
        self.question = question

    # Displays the title
    def title(self,win,coords,size=20,font='yugothicyugothicuilight'):
        txtFont = pygame.font.SysFont(font,size)
        txtSurface = txtFont.render(self.question, True, (0,0,0))
        win.blit(txtSurface,coords)

# Child input class created
class Inputbox(Input):
    # Initializes variables
    def __init__(self,question,bkgC,colour):
        super().__init__(question)
        self.bkg = bkgC
        self.colour = colour
        self.valid = 'abcdefghijklmnopqrstuvwxyz 0123456789'
        self.capsOn = False
        self.key = -1
        self.current_string = []

    # Draws the inputbox on the screen
    def display_box(self,screen,message):
      if len(message) != 0:
        fontobject = pygame.font.SysFont("yugothicyugothicuilight", 20)
        message_surface = fontobject.render(message, 1, self.colour)
        recWidth = message_surface.get_width() + 10
        if recWidth < 200:
          recWidth = 200
      else:
        recWidth = 200  
      pygame.draw.rect(screen, self.bkg,((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 100,recWidth,30), 0)
      pygame.draw.rect(screen, self.colour,((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 100,recWidth,30), 1)
      if len(message) != 0:
        screen.blit(message_surface,((screen.get_width() / 2) - 95, (screen.get_height() / 2) - 96))

    # Lets the user input using the keyboard
    def ask(self,screen):
        pygame.font.init()
        self.display_box(screen, self.question + ": " + ''.join(self.current_string))
        if self.key == pygame.K_LSHIFT or self.key == pygame.K_RSHIFT:
          self.capsOn = not self.capsOn
        if self.key == pygame.K_BACKSPACE:
          self.current_string = self.current_string[0:-1]
        if self.key == pygame.K_RETURN:
          return ''.join(self.current_string)
        if self.key == pygame.K_MINUS:
          self.current_string.append("_")
        if self.key > -1 and chr(self.key) in self.valid:
            inkeyLtr = chr(self.key)
            if self.capsOn:
                inkeyLtr = inkeyLtr.upper()
            self.current_string.append(inkeyLtr)
            self.display_box(screen, self.question + ''.join(self.current_string))
            self.key = -1

    # Gets the key that has been pressed and assigns self.key to it
    def getKey(self,key):
        self.key = key

# Child input class created
class Slider(Input):
    # Initializes variables
    def __init__(self,question,x1,x2,y,cx):
        super().__init__(question)
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.cx = cx
        self.points = []
        self.mouseDown = False
        self.cRect = ((self.cx - 10, self.y-10), (self.cx + 10, self.y + 10))

    # Draws the sliders
    def draw(self,win,colour=(0,0,0),font='yugothicyugothicuilight'):
        pygame.draw.line(win, colour, (self.x1,self.y),(self.x2,self.y))
        pygame.draw.circle(win, colour,(self.cx,self.y), 10)
        fontobject = pygame.font.SysFont(font, 20)
        count = 0
        for x in range(self.x1,self.x2+50,50):
            pygame.draw.line(win, colour, (x,self.y-10), (x,self.y+10))
            if x not in self.points:
                self.points.append(x)
            txtSurface = fontobject.render(str(count), True, colour)
            win.blit(txtSurface,(x-5,self.y+15))
            count += 1
        
    # Displays the title
    def title(self,win,coords,size=20,font='yugothicyugothicuilight'):
        super().title(win,coords,size,font)

    # Moves the scale when clicked
    def moveCirc(self,mousePos):
        if pygame.Rect(self.cRect).collidepoint(mousePos) and self.mouseDown:
            self.cx = mousePos[0]
            self.cRect = ((self.cx - 10,self.cRect[0][1]),self.cRect[1])
            if self.cx < self.x1:
                self.cx = self.x1
            elif self.cx > self.x2:
                self.cx = self.x2
        # Places the slider at a value
        elif not self.mouseDown:
            xPos = str(self.cx)
            if int(xPos[1:]) <= 25:
                self.cx = int(xPos[0]) * 100
            elif int(xPos[1:]) >= 75:
                self.cx = (int(xPos[0]) + 1) * 100
            else:
                self.cx = int(xPos[0]) * 100 + 50

    # Returns the value of the slider
    def returnValue(self):
        return self.points.index(self.cx)

# Child input class
class Filepicker(Input):
    # Initializes variables
    def __init__(self,question,rect,fontSize=30):
        super().__init__(question)
        self.rect = rect
        self.fontSize = fontSize
        self.btn = buttons.Button(self.rect)
        self.btntxt = buttons.Label(self.question,self.fontSize)

    # Draws the button
    def draw(self,win):
        self.btn.draw(win)
        self.btntxt.draw(win,self.rect)

    # Returns the selected file
    def returnFile(self):
        root = Tk()
        root.withdraw()
        root.fileName = filedialog.askopenfilename(filetypes = (('JPG','*.jpg'),('PNG','*.png')))
        fileToOpen = root.fileName
        root.destroy()
        return fileToOpen
