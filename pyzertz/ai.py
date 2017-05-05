def think(init, succ, score, minim : bool, thres=None):
    better = int.__lt__ if minim else int.__gt__
    initScore = score(init)
    if initScore != None:
        return (initScore, [])
    nextStates = succ(init)
    if nextStates == []:
        raise ValueError
    (bestScore, bestPath) = think(nextStates[0][0], succ, score, not minim, None)
    bestPath = [nextStates[0][1]] + bestPath
    if thres != None and better(bestScore, thres):
        return (thres, [])
    for (state, action) in nextStates[1:]:
        (nextScore, path) = think(state, succ, score, not minim, bestScore)
        if thres != None and better(nextScore, thres):
            return (thres, [])
        elif better(nextScore, bestScore):
            (bestScore, bestPath) = (nextScore, [action] + path)
    return (bestScore, bestPath)

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


