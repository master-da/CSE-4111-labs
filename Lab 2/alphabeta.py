from CTK import CTK
from copy import deepcopy
import time

def alpha_beta(depth, maximizingPlayer, alpha, beta, game: CTK, debug = False):
    
    if game.max_player_state[0] == None: return float('-inf'), (None, None)
    if game.min_player_state[0] == None: return float('inf'), (None, None)

    if depth == 0:
        return game.min_player_state.count(None) - game.max_player_state.count(None), (None, None)
    
    if maximizingPlayer:
        maxEval = float('-inf')
        bestMove = None
        
        backup = game.max_player_state.copy(), game.min_player_state.copy()
        
        for i in range(game.size+1):

            # print(depth, i, game.max_player_state, game.min_player_state)
            if game.max_player_state[i] is None: continue
            
            for move in game.getLegalMoveSet(True, i):
                
                game.makeMove(True, i, move)
                evaluation, _ = alpha_beta(depth - 1, False, alpha, beta, game, debug)
                # print(depth, (i, move), evaluation)
                
                if evaluation >= maxEval:
                    maxEval = evaluation
                    bestMove = (i, move)
                    if evaluation >= beta: break
                    alpha = max(alpha, evaluation)
                    
            # if depth == 2 and debug: print(i, "maxEval", maxEval, bestMove)
                
                
            game.max_player_state, game.min_player_state = deepcopy(backup)

                
        return maxEval, bestMove
    
    else:
        minEval = float('inf')
        bestMove = None
        
        backup = game.max_player_state.copy(), game.min_player_state.copy()
        
        for i in range(game.size+1):
            
            if game.min_player_state[i] is None: continue
            
            for move in game.getLegalMoveSet(False, i):
                
                game.makeMove(False, i, move)
                evaluation, _ = alpha_beta(depth - 1, True, alpha, beta, game, debug)
                
                if evaluation <= minEval:
                    minEval = evaluation
                    bestMove = (i, move)
                    if evaluation <= alpha: break
                    beta = min(beta, evaluation)

            game.max_player_state, game.min_player_state = deepcopy(backup)

        return minEval, bestMove
    
    
if __name__ == "__main__":
    game = CTK(4)
    # print(game.max_player_state, game.min_player_state)
    # print(game)
    
    start = time.time()
    
    move_history = []
    print(game)
    print(game.max_player_state, game.min_player_state)
    maxPlayerTurn = True
    # for it in range(16):
    while not game.ifEndGame():
        
        evaluation, move = alpha_beta(8, maxPlayerTurn, float('-inf'), float('+inf'), game)        
        
        if move[0] is None:
            print("GAME TIED!!")
            break
        game.makeMove(maxPlayerTurn, move[0], move[1])

        move_history.append(move)
        if len(move_history) > 9 and move_history[-1] == move_history[-5] and move_history[-1] == move_history[-9]:
            print("Draw by repetition")
            break
        
        print("\'Player 1\'" if maxPlayerTurn else "\'Player 2\'" , move[0], "->", move[1], "eval: ", evaluation)
        print(game)
        
        # print(move_history)

        maxPlayerTurn = not maxPlayerTurn    
        
    if game.min_player_state[0] is None: print("Player 1 wins")
    if game.max_player_state[0] is None: print("Player 2 wins")
    end = time.time() - start
    print("time:", end)
    