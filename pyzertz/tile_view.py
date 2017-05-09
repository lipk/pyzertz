from button import  *
from table import *
import math

class TileView(Button):
    GREY  = (100,100,100)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    COLORS = (WHITE, GREY, BLACK)
    # color: fill color
    # pointlist: vertices
    # center: (int, int) pixel koords
    # col: int column ind
    # row: int row ind
    def __init__(self , tile: Tile, start_x: int, start_y: int, size: int,\
            color: (int,int,int), action : 'function' = None):
        self.col = tile.col
        self.row = tile.row
        self.color = color
        self.size = size
        self.center = hex_to_pixel((tile.col,tile.row),size)
        height = 2*size
        width = math.sqrt(3)*size
        
        self.center = (self.center[0] + start_x + 3*width, self.center[1]\
                + start_y + 0.75 * 3 * height)

        self.pointlist = [0]*6
        for i in range(6):
            self.pointlist[i] = hex_corner(self.center, self.size, i)
        
        self.handle = action if action else default_handler
    
    def draw_button(self, surface: pygame.Surface, tile: Tile) -> pygame.Surface: 
        if tile.type == -1:
            pass
        pygame.draw.polygon(surface, self.color, self.pointlist, 0)
        pygame.draw.polygon(surface, (0,0,0), self.pointlist, 1)
        if tile.type == 0:
            return surface
        color = TileView.COLORS[tile.type-1]
        pygame.draw.circle(surface, color, self.center, self.size, 0)
        return surface

    def pressed(self, mouse:'mouse pos') -> bool:
        x = mouse[0]-self.center[0]
        y = mouse[1]-self.center[1]
        if x*x+y*y<(self.size)**2:
            self.action();
            return True
        else: return False


def hex_corner(center:(int, int), size: int, i:(0-5)) -> (int,int):
    angle_deg = 60 * i   + 30
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + size * math.cos(angle_rad),\
            center[1] + size * math.sin(angle_rad))

def hex_to_pixel(hex_coord:(int, int), size: int) -> (int, int):
    x = size * math.sqrt(3) * (hex_coord[0] + hex_coord[1]/2)
    y = size * 3/2 * hex_coord[1]
    return (x, y)
