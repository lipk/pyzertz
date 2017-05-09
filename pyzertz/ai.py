def think(init, succ, score, minim : bool, thres=None):
    better = int.__lt__ if minim else int.__gt__
    init_score = score(init)
    if init_score != None:
        return (init_score, [])
    next_states = succ(init)
    if next_states == []:
        raise ValueError
    (best_score, best_path) = think(next_states[0][0], succ, score, not minim, None)
    best_path = [next_states[0][1]] + best_path
    if thres != None and better(best_score, thres):
        return (thres, [])
    for (state, action) in next_states[1:]:
        (next_score, path) = think(state, succ, score, not minim, best_score)
        if thres != None and better(next_score, thres):
            return (thres, [])
        elif better(next_score, best_score):
            (best_score, best_path) = (next_score, [action] + path)
    return (best_score, best_path)

#TODO: replace with real impl
class GameState:
    def __init__(self):
        self.player1 = [0, 0, 0]
        self.player2 = [0, 0, 0]
        self.on_board = [0, 0, 0]

    def must_jump():
        pass


def balls_to_win(balls : list):
    return max(0,min(4-balls[0], 5-balls[1], 6-balls[2], sum(map(lambda b: max(0, 3-b), balls))))

def score_state(player1 : list, player2 : list):
    return balls_to_win(player1) - balls_to_win(player2)

def max_gain(player : list, on_board : list):
    return balls_to_win(map(sum(zip(player, on_board)))) - balls_to_win(player)

def create_score_func(init : GameState, player_no : int):
    def score_func(state : GameState):
        me_init = init.player1 if player_no == 1 else init.player2
        me = state.player1 if player_no == 1 else state.player2
        other_init = init.player2 if player_no == 1 else init.player1
        other = state.player2 if player_no == 1 else state.player1
        current_gain = score_state(me, other) - score_state(me_init, other_init)
        if current_gain > 0 or max_gain(me, state.on_board) < -current_gain:
            return score_state(me, other)
        else:
            return None
    return score_func


