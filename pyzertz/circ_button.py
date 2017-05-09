from button import *

class CircleButton(Button):
    # center: (int,int)
    # text: ""
    # size: radius
    # action : func
    # color: (int, int, int)

    def __init__(self , x : int, y : int, r: int,
            color: (int,int,int), text : str, action : 'function' = None):
        self.center = (x,y)
        self.size = r
        self.color = color
        self.text = text
       
        self.handle = action if action else default_handler
       

    def draw_button(self, surface: pygame.Surface) -> pygame.Surface: 
        pygame.draw.circle(surface, self.color, self.center, self.size, 0)
        return self.write_text(surface)
    
    def write_text(self, surface: pygame.Surface) -> pygame.Surface:
        font_size = int(self.size//len(self.text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(self.text, 1, (0,255,0))
        surface.blit(myText, ((self.center[0]) \
                - myText.get_width()/2, (self.center[1]) \
                - myText.get_height()/2))
        return surface

    def pressed(self, mouse:'mouse pos') -> bool:
        x = mouse[0]-self.center[0]
        y = mouse[1]-self.center[1]
        if x*x+y*y<(self.size)**2:
            self.action();
            return True
        else: return False

