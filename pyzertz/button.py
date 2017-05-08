import pygame
from pygame.locals import *
pygame.init()

class Button:
    # rect: (int,int,int,int) : (x,y,length,height)
    # text: ""
    # action : func
    # color: (int, int, int)

    def __init__(self , x : int, y : int, length : int, height : int, color: (int,int,int), text : str, action : 'function' = None):
        self.rect = (x,y,length,height)
        self.color = color
        self.text = text
        if action : 
            self.handle = action
        else :
            self.handle = default_handler
        

    def action(self, *args, **kwargs):
        self.handle(self, *args, **kwargs)

    def draw_button(self, surface: pygame.Surface):           
        pygame.draw.rect(surface, self.color, self.rect, 0)
        self.write_text(surface)
        print(surface.__class__)
        return surface
    
    def write_text(self, surface: pygame.Surface):
        font_size = int(self.rect[2]//len(self.text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(self.text, 1, (0,0,0))
        surface.blit(myText, ((self.rect[0]+self.rect[2]/2) - myText.get_width()/2, (self.rect[1]+self.rect[3]/2) - myText.get_height()/2))
        return surface

    def pressed(self, mouse:'mouse pos') -> bool:
        if mouse[0] > self.rect[0]:
            if mouse[1] > self.rect[1]:
                if mouse[0] < self.rect[0]+self.rect[2]:
                    if mouse[1] < self.rect[1]+self.rect[3]:
                        self.action();
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

def default_handler(btn : Button, *args, **kwargs):
    print("No action added to this button " + btn.text)

