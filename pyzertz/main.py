#!/usr/bin/python3
import table_view
import game_state
import pygame

SELECT_MARBLE_TYPE = 1
SELECT_TILE_FOR_PLACEMENT = 2
SELECT_TILE_TO_REMOVE = 3
SELECT_MARBLE_TO_CAPTURE_WITH = 4
SELECT_TILE_FOR_CAPTURE = 5
WAITING_FOR_AI = 6
WAITING_FOR_RESTART = 7

class GameController:
    def __init__(self):
        self.game_state = game_state.State()
        self.state = SELECT_MARBLE_TYPE
        self.selected_marble = None
        self.capture_from = None

    def should_restart(self):
        if self.state == WAITING_FOR_RESTART:
            self.game_state = game_state.State()
            return True
        return False

    def tile_clicked(self, col: int, row: int):
        if self.should_restart():
            return True
        elif self.state == SELECT_TILE_FOR_PLACEMENT:
            move = (col, row, self.selected_marble)
            ok = game_state.isValidPlace(move, self.game_state.t)
            if ok:
                self.game_state = game_state.place(move, self.game_state)
                self.state = SELECT_TILE_TO_REMOVE
                return True
            else:
                return False
        elif self.state == SELECT_TILE_TO_REMOVE:
            move = (col, row)
            if game_state.isValidRemove(move, self.game_state.t):
                self.game_state = game_state.remove(move, self.game_state)
                self.game_state.next_player()
                if game_state.isThereAValidCaptureFromAnyTile(self.game_state.t):
                    self.state = SELECT_MARBLE_TO_CAPTURE_WITH
                else:
                    self.state = SELECT_MARBLE_TYPE
                return True
            else:
                return False
        elif self.state == SELECT_MARBLE_TO_CAPTURE_WITH:
            tile = (col, row)
            if game_state.isThereAValidCaptureFromOneTile(tile, self.game_state.t):
                self.capture_from = tile
                self.state = SELECT_TILE_FOR_CAPTURE
            return False
        elif self.state == SELECT_TILE_FOR_CAPTURE:
            src_x, src_y = self.capture_from
            jump = (src_x, src_y, col, row)
            if game_state.isValidJump(jump, self.game_state.t):
                self.game_state = game_state.jump(jump, self.game_state)
                if not game_state.isThereAValidCaptureFromOneTile((col, row), self.game_state.t):
                    self.game_state.next_player()
                if game_state.isThereAValidCaptureFromAnyTile(self.game_state.t):
                    self.state = SELECT_MARBLE_TO_CAPTURE_WITH
                else:
                    self.state = SELECT_MARBLE_TYPE
                return True
            else:
                return False

    def marble_clicked(self, marble: int):
        if self.should_restart():
            return True
        elif self.state == SELECT_MARBLE_TYPE:
            self.selected_marble = marble
            self.state = SELECT_TILE_FOR_PLACEMENT
        return False

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PyZertz')
pygame.display.flip()

controller = GameController()
table = table_view.TableView(controller.game_state, window)

redraw = True
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse1, _, _ = pygame.mouse.get_pressed()
        if mouse1:
            tile_coords = table.get_pressed_tile(pygame.mouse.get_pos())
            if tile_coords != None:
                tile_x, tile_y = tile_coords
                redraw = controller.tile_clicked(tile_x, tile_y)
            else:
                marble = table.get_pressed_marble(pygame.mouse.get_pos())
                if marble != None:
                    redraw = controller.marble_clicked(marble)

    if redraw:
        table.draw(window, controller.game_state)
        pygame.display.flip()
        redraw = False
