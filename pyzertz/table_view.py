from tile_view import *
from table import *
from game_state import *
from circ_button import *

class TableView:
    GREY  = (100,100,100)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    BGCOLOR = (60,60,100)
    TILE_COLOR = (90, 255, 90)
    TILE_RADIUS = 30
    TABLE_POS = (245, 90)

    # table : Table
    # pl1, pl2: Player
    # game_board: list(TileView)
    # pl1_view pl2_view
    # marble_stack: the available marbles
    def __init__(self, state: State, surface: pygame.Surface): 
        pl1 = state.pl1
        pl2 = state.pl2
        table = state.t
        self.game_board = []
        r = TableView.TILE_RADIUS
        for i in range(-3,4):
            for j in range(-3,4):
                if math.fabs(i+j)<=3:
                    self.game_board.append(TileView(table.get(i,j),\
                            TableView.TABLE_POS[0], TableView.TABLE_POS[1],\
                            r, TableView.TILE_COLOR))#, lambda btn : print(btn.col, btn.row)))
        W = surface.get_width()
        H = surface.get_height()
        self.pl1_view = PlayerView(pl1, (0,0))
        self.pl2_view = PlayerView(pl2, (W-TableView.TILE_RADIUS*2,0))
        self.marble_stack = []
        self.marble_stack.append(CircleButton(int(W/2-r*3), H-r*2, r, \
                TableView.WHITE, str(table.marbles[0])))
        self.marble_stack.append(CircleButton(int(W/2), H-r*2, r, \
                TableView.GREY, str(table.marbles[1])))
        self.marble_stack.append(CircleButton(int(W/2+r*3), H-r*2, r, \
                TableView.BLACK, str(table.marbles[2])))


    def draw(self, surface: pygame.Surface, state: State):
        surface.fill(TableView.BGCOLOR)
        for tile in self.game_board:
            tile.draw_button(surface,state.t.get(tile.col, tile.row))
        self.pl1_view.draw(surface, state.pl1)
        self.pl2_view.draw(surface, state.pl2)
        for i in range(len(state.t.marbles)):
            btn = self.marble_stack[i]
            btn.text = str(state.t.marbles[i])
            btn.draw_button(surface)

    def get_pressed_tile(self, pos):
        for tile in self.game_board:
            if tile.pressed(pos):
                return (tile.col, tile.row)
        return None

    def get_pressed_marble(self, pos):
        for (i,marble) in enumerate(self.marble_stack):
            if marble.pressed(pos):
                return i
        return None


class PlayerView:

    def __init__(self, pl: Player, pos: (int, int)):
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
    
    def draw(self, surface: pygame.Surface, player: Player):
        for i in range(len(self.buttons)):
            btn = self.buttons[i]
            btn.text = str(player.marbles[i])
            btn.draw_button(surface)

        font_size = int(TableView.TILE_RADIUS*3//len(player.name))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(player.name, 1, (0,0,0))
        surface.blit(myText, (self.pos[0]+TableView.TILE_RADIUS/2,\
                self.pos[1] + TableView.TILE_RADIUS/2))


         
        
