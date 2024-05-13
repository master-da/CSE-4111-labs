
    
class CTK:
    size = 0
    
    max_player_state = []
    min_player_state = []
    
    _visited = {}
    
    def __init__(self, size):
        if size < 4:
            print("size too small. changed to 4")
            size = 4
        self.size = size
        self.max_player_state = [0 for _ in range(size+1)]
        self.min_player_state = [0 for _ in range(size+1)]
        center = (size-1) // 2
        
        self.max_player_state[0] = 0 * size + center
        self.min_player_state[0] = (size-1) * size + center

        for i in range(size):
            self.max_player_state[i+1] = 1 * size + i
            self.min_player_state[i+1] = (size-2) * size + i

    def __str__(self) -> str:
        board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        if self.max_player_state[0] is not None: board[self.max_player_state[0] // self.size][self.max_player_state[0] % self.size] = "V"
        if self.min_player_state[0] is not None: board[self.min_player_state[0] // self.size][self.min_player_state[0] % self.size] = "A"
        
        for i in range(1, self.size+1):
            if self.max_player_state[i] is not None: board[self.max_player_state[i] // self.size][self.max_player_state[i] % self.size] = "v"
            if self.min_player_state[i] is not None: board[self.min_player_state[i] // self.size][self.min_player_state[i] % self.size] = "^"
            
        return "\n".join(["\t".join([str(x) for x in row]) for row in board])
    
    def printState(self, state):

        max_player_state, min_player_state = state
        
        board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        if max_player_state[0] is not None: board[max_player_state[0] // self.size][max_player_state[0] % self.size] = "V"
        if min_player_state[0] is not None: board[min_player_state[0] // self.size][min_player_state[0] % self.size] = "A"
        
        for i in range(1, self.size+1):
            if max_player_state[i] is not None: board[max_player_state[i] // self.size][max_player_state[i] % self.size] = "v"
            if min_player_state[i] is not None: board[min_player_state[i] // self.size][min_player_state[i] % self.size] = "^"
        print("\n".join(["\t".join([str(x) for x in row]) for row in board]))
            
    
    def getLegalMoveSet(self, maximizingPlayer, piece) -> list[int]:
        move_position = []
        player = self.max_player_state if maximizingPlayer is True else self.min_player_state
        enemy = self.min_player_state if maximizingPlayer is True else self.max_player_state
        friendly = player.copy()
        friendly.pop(piece)
        
        if piece == 0:
            # this is the king, it can move in 4 cardinal directions withing the size x size board.
            if player[piece] >= self.size and player[piece] - self.size not in friendly:
                move_position.append(player[piece] - self.size)
            if player[piece] < (self.size-1) * self.size and player[piece] + self.size not in friendly:
                move_position.append(player[piece] + self.size)
            if player[piece] % self.size != 0 and player[piece] - 1 not in friendly:
                move_position.append(player[piece] - 1)
            if player[piece] % self.size != self.size-1 and player[piece] + 1 not in friendly:
                move_position.append(player[piece] + 1)
            
        else:
            # this is a pawn
            if maximizingPlayer is True:
                # pawn can only move down in 3 directions: forward and diagonal.
                if player[piece] < (self.size-1) * self.size:
                    if player[piece] + self.size not in friendly and player[piece] + self.size not in enemy:
                        move_position.append(player[piece] + self.size)
                    if player[piece] % self.size != 0 and (player[piece] + self.size - 1) in enemy:
                        move_position.append(player[piece] + self.size - 1)
                    if player[piece] % self.size != self.size-1 and (player[piece] + self.size + 1) in enemy:
                        move_position.append(player[piece] + self.size + 1)
            else:
                # pawn can only move up in 3 directions: forward and diagonal.
                if player[piece] >= self.size:
                    if player[piece] - self.size not in friendly and player[piece] - self.size not in enemy:
                        move_position.append(player[piece] - self.size)
                    if player[piece] % self.size != 0 and (player[piece] - self.size - 1) in enemy:
                        move_position.append(player[piece] - self.size - 1)
                    if player[piece] % self.size != self.size-1 and (player[piece] - self.size + 1) in enemy:
                        move_position.append(player[piece] - self.size + 1)

        return move_position
                
    def ifEndGame(self) -> bool:
        return self.max_player_state[0] == None or self.min_player_state[0] == None
        
    def makeMove(self, player, piece, move):
        if player is True:
            if move in self.min_player_state:
                self.min_player_state[self.min_player_state.index(move)] = None
            self.max_player_state[piece] = move
        else:
            if move in self.max_player_state:
                self.max_player_state[self.max_player_state.index(move)] = None
            self.min_player_state[piece] = move
