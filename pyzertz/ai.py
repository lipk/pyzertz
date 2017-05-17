import game_state
import functools

def think(init, succ, score, minim : bool, thres=None):
    better = int.__lt__ if minim else int.__gt__
    init_score = score(init)
    if init_score != None:
        return (init_score, [])
    next_states = succ(init)
    if next_states == []:
        raise ValueError
    (best_score, best_path) = think(next_states[0], succ, score, not minim, None)
    best_path = [next_states[0]] + best_path
    if thres != None and better(best_score, thres):
        return (thres, [])
    for state in next_states[1:]:
        (next_score, path) = think(state, succ, score, not minim, best_score)
        if thres != None and better(next_score, thres):
            return (thres, [])
        elif better(next_score, best_score):
            (best_score, best_path) = (next_score, [state] + path)
    return (best_score, best_path)


def balls_to_win(balls : list):
    balls = list(balls)
    return max(0,min(4-balls[0], 5-balls[1], 6-balls[2], sum(map(lambda b: max(0, 3-b), balls))))

def score_state(player1 : list, player2 : list):
    return balls_to_win(player1) - balls_to_win(player2)

def max_gain(player : list, on_board : list):
    print(player, on_board)
    return balls_to_win(map(sum, zip(player, on_board))) - balls_to_win(player)

def get_on_board(state):
    [w1, g1, b1] = state.pl1.marbles
    [w2, g2, b2] = state.pl2.marbles
    [w3, g3, b3] = state.t.marbles
    return [6-w1-w2-w3, 8-g1-g2-g3, 10-b1-b2-b3]

def create_score_func(init : GameState, player_no : int):
    def score_func(state : GameState):
        if (state.act is state.pl2):
            print('my turn')
            return None
        print('not my turn')
        print(game_state.isThereAValidCaptureFromAnyTile(state.t))
        me_init = init.pl1.marbles if player_no == 1 else init.pl2.marbles
        me = state.pl1.marbles if player_no == 1 else state.pl2.marbles
        other_init = init.pl2.marbles if player_no == 1 else init.pl1.marbles
        other = state.plr2.marbles if player_no == 1 else state.pl1.marbles
        current_gain = score_state(me, other) - score_state(me_init, other_init)
        if current_gain > 0 or max_gain(me, get_on_board(state)) < -current_gain:
            return score_state(me, other)
        else:
            return None
    return score_func

def flatten(xs):
    return functools.reduce(lambda x, y: x + y, xs)

def get_possible_captures_from_tile(state, col, row):
    result = []
    if game_state.isThereAValidCaptureFromOneTile((col, row), state.t):
        for dst_tile in flatten(state.t.tiles):
            dst_col, dst_row = dst_tile.col, dst_tile.row
            if game_state.isValidJump((col, row, dst_col, dst_row), state.t):
                state2 = game_state.jump((col, row, dst_col, dst_row), state)
                if game_state.isThereAValidCaptureFromOneTile((dst_col, dst_row), state2.t):
                    result += get_possible_captures_from_tile(state2, dst_col, dst_row)
                else:
                    result.append(state2)
                    result[-1].next_player()
    return result


def get_possible_moves(state):
    result = []
    if game_state.isThereAValidCaptureFromAnyTile(state.t):
        for tile in flatten(state.t.tiles):
            result += get_possible_captures_from_tile(state, tile.col, tile.row)
    else:
        for marble in [0, 1, 2]:
            for tile in flatten(state.t.tiles):
                col, row = tile.col, tile.row
                if game_state.isValidPlace((col, row, marble), state.t):
                    state2 = game_state.place((col, row, marble), state)
                    for tile2 in flatten(state2.t.tiles):
                        col2, row2 = tile2.col, tile2.row
                        if game_state.isValidRemove((col2, row2), state2.t):
                            result.append(game_state.remove((col2, row2), state2))
                            result[-1].next_player()
    return result

def make_move(state):
    score_func = create_score_func(state, 2)
    (score, path) = think(state, get_possible_moves, score_func, True)
    print(score)
    return path[0]
