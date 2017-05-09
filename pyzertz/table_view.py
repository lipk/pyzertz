from tile_view import *
from table import *
from game_state import *
from circ_button import *

class TableView:
    GREY  = (100,100,100)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    BGCOLOR = (60,60,100)
    TILE_COLOR = (90, 60, 90)
    TILE_RADIUS = 30
    TABLE_POS = (3*TILE_RADIUS, 3*TILE_RADIUS)

    # table : Table
    # pl1, pl2: Player
    # game_board: list(TileView)
    # pl1_view pl2_view
    # marble_stack: the available marbles
    def __init__(self, table: Table, pl1: Player, pl2: Player, surface: pygame.Surface): 
        self.table = table
        self.pl1 = pl1
        self.pl2 = pl2
        self.game_board = []
        r = TableView.TILE_RADIUS
        for i in range(-4,4):
            for j in range(-4,4):
                if math.fabs(i+j)<=3:
                    self.game_board.append(TileView(self.table.get(i,j),\
                            TableView.TABLE_POS[0], TableView.TABLE_POS[1],\
                            r, TableView.TILE_COLOR))
        self.pl1_view = PlayerView(pl1, (0,0)*3)
        self.pl2_view = PlayerView(pl2, (520-TableView.TILE_RADIUS*2,0))
        self.marble_stack = []
        W = surface.get_width()
        H = surface.get_height()
        self.marble_stack.append(CircleButton(int(W/2-r*3), H-r*2, r, \
                TableView.WHITE, str(table.marbles[0])))
        self.marble_stack.append(CircleButton(int(W/2), H-r*2, r, \
                TableView.GREY, str(table.marbles[1])))
        self.marble_stack.append(CircleButton(int(W/2+r*3), H-r*2, r, \
                TableView.BLACK, str(table.marbles[2])))


    def draw(self, surface: pygame.Surface) -> pygame.Surface:
        surface.fill(TableView.BGCOLOR)
        for tile in self.game_board:
            tile.draw_button(surface)
        self.pl1_view.draw(surface)
        self.pl2_view.draw(surface)
        for btn in self.marble_stack:
            btn.draw_button(surface)

class PlayerView:

    def __init__(self, pl: Player, pos: (int, int)):
        self.player = pl
        self.pos = pos
        r = int(TableView.TILE_RADIUS/2)
        self.buttons = [CircleButton(pos[0]+r*2, \
                r*3, r, \
                TableView.WHITE, str(pl.marbles[0]))]
        self.buttons.append(CircleButton(pos[0]+r*2, \
                r*6, r, \
                TableView.GREY, str(pl.marbles[1])))
        self.buttons.append(CircleButton(pos[0]+r*2, \
                r*9, r, \
                TableView.BLACK, str(pl.marbles[2])))
    
    def draw(self, surface: pygame.Surface):
        for btn in self.buttons:
            btn.draw_button(surface)

        font_size = int(TableView.TILE_RADIUS*3//len(self.player.name))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(self.player.name, 1, (0,0,0))
        surface.blit(myText, (self.pos[0]+TableView.TILE_RADIUS/2,\
                self.pos[1] + TableView.TILE_RADIUS/2))


         
        
