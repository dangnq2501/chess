import chess
import chess.svg
import random
inf = 100000000

# print(board)
'''
board.push(chess.Move.from_uci("e2e4"))
board.push(chess.Move.from_uci("h7h5"))
board.push(chess.Move.from_uci("d1h5"))
board.push(chess.Move.from_uci("h8h5"))
'''

#print(board.turn) get the turn

'''
movement = chess.Move.from_uci("g1f3")
if (movement in board.legal_moves):
    print('---------------------------')
    board.push(movement)  # Make the move
    print(board)
else: print('illegal move')
#checking move
'''

#print(board.outcome())
# detailed outcome check out document for more
# document got stuff like who win, why win, why draw, etc

#print(board.is_game_over())
# is it ended ?

#print(board.has_insufficient_material(True))
# return to False if white (True) can still win the game
# we may want to avoid state when we cant win the game ==> negative factor here

#print(board.can_claim_draw())
# Checks if the player to move can claim a draw by the fifty-move rule or by threefold repetition.

'''
piece = board.piece_at(8)
print(piece,'?')
if (piece.piece_type == chess.KNIGHT):
    print('yesssss')
else: print('noooooo')
print(chess.KNIGHT)
print(piece.color)
# get the piece at position 0,1,2,3,4,5,....63 (A1 = 0, B1 = 1,..)
'''

#legal_moves = list(board.legal_moves)
#print(legal_moves)
# convert legal move to a list and iterate through it

#possible_knight_attack = list(board.attacks(1))
#print(possible_knight_attack)
# get possible attack of a cell on board
# same for is_attacked_by

'''
print('--------------------------')
board.pop()
print(board)
# pop the last move, backtrack need this for sure
'''

#board.peek()
# get the last move, not remove that move

###--------------------------Here come the code-----------------------###
piece_value = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 
                 1, 1, 0, -3, -3, 0, 1, 1, 
                 1, -1, -2, 0, 0, -2, -1, 1, 
                 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50, 
                   -40, -20, 0, 5, 5, 0, -20, -40, 
                   -30, 5, 10, 15, 15, 10, 5, -30, 
                   -30, 0, 15, 20, 20, 15, 0, -30, 
                   -30, 5, 15, 20, 20, 15, 5, -30, 
                   -30, 0, 10, 15, 15, 10, 0, -30, -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
    chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
    chess.ROOK: [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    chess.QUEEN: [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
    chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20]  # King value is often set to 0 in simple evaluations
}

def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0

class Agent_alpha_beta():
    def __init__(self, weight : list, board : chess.Board, depth):
        self.pawnWeight = weight[0]
        self.knightWeight = weight[1]
        self.bishopWeight = weight[2]
        self.rookWeight = weight[3]
        self.queenWeight = weight[4]
        self.kingWeight = 3
        self.pawnAdvance = 1
        self.checkmate = weight[5]
        self.board = board
        self.depth = depth
        self.start_state = 4
        #we will get protective stuff, folk piece, checkmate significant etcetera,... later
    
    def count_pieces(self):
        cnt = 0
        for i in range(64):
            if self.board.piece_at(i):
                cnt += 1
        return cnt  
    
    def getScore(self):
        score = 0
        for i in range (0,64):
            piece = self.board.piece_at(i)
            if (piece is None): continue
            color = 1
            base = 0
            if (piece.color == False): color = -1
            if (piece.piece_type == chess.PAWN):
                if (piece.color == True):
                    base = self.pawnWeight + self.pawnAdvance*(i//8 - 1)
                else:
                    base = self.pawnWeight + self.pawnAdvance*(6 - i//8)
            if (piece.piece_type == chess.KNIGHT): base = self.knightWeight
            if (piece.piece_type == chess.BISHOP): base = self.bishopWeight
            if (piece.piece_type == chess.ROOK): base = self.rookWeight
            if (piece.piece_type == chess.QUEEN): base = self.queenWeight

            if color > 0:
                score += color * base *  piece_value[piece.piece_type][i]
            else:
                score += color * base *  piece_value[piece.piece_type][63-i]

        return score

    # Minimax algorithm with Alpha-Beta Pruning
    def minimax(self, depth, alpha, beta):
        if (self.board.is_game_over()):
            return detect_end_score(self.board)
        if (depth == self.depth): return self.getScore()

        maximizing_player = self.board.turn
        tmp = []
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            pos = move.from_square
            piece = self.board.piece_at(pos)
            behind_piece = None 
            if 0 <= pos - 8 and pos - 8 < 64 and self.board.piece_at(pos-8):
                behind_piece = self.board.piece_at(pos-8)
            if 0 <= pos + 8 and pos + 8 < 64 and self.board.piece_at(pos+8):
                behind_piece = self.board.piece_at(pos+8)
            # 3 first move only use knight and pawn in front of king
            if self.start_state == 0 or ((pos < 16 or pos > 48)  and self.start_state > 0 and (piece.piece_type == chess.KNIGHT or (piece.piece_type == chess.PAWN   and behind_piece and behind_piece.piece_type == chess.KING ))):
                tmp.append((move,self.getScore()))
        legal_moves = tmp
        best_move = legal_moves[0]
        # random.shuffle(legal_moves)
        if maximizing_player:
            max_eval = -inf
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth + 1, alpha, beta)
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if (depth == 0): return best_move
            else: return max_eval
        else:
            min_eval = inf
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth + 1, alpha, beta)
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if (depth == 0): return best_move
            else: return min_eval

    # Find the best move using Minimax with Alpha-Beta Pruning
    def make_next_move(self):
        return self.minimax(0,-inf,inf)


board = chess.Board(chess.STARTING_BOARD_FEN)
def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0

def cmp_func(a,b):
    if (a[1] > b[1]): return 1
    else: return -1
from functools import cmp_to_key
cmp_key = cmp_to_key(cmp_func)

class Agent_pruning_best2():
    def __init__(self, weight : list, board : chess.Board, depth):
        self.pawnWeight = weight[0]
        self.knightWeight = weight[1]
        self.bishopWeight = weight[2]
        self.rookWeight = weight[3]
        self.queenWeight = weight[4]
        self.kingWeight = 3000
        self.pawnAdvance = 1
        self.checkmate = weight[5]
        self.board = board
        self.depth = depth
        self.start_state = 4
        #we will get protective stuff, folk piece, checkmate significant etcetera,... later

    def getScore(self):
        score = 0
        for i in range (0,64):
            piece = self.board.piece_at(i)
            if (piece is None): continue
            color = 1
            base = 0
            if (piece.color == False): color = -1
            if (piece.piece_type == chess.PAWN):
                if (piece.color == True):
                    cell_advanced = self.pawnAdvance*(i//8 - 1)
                else:
                    cell_advanced = self.pawnAdvance*(6 - i//8)

                if (cell_advanced > 0 and cell_advanced <= 2): base += 1  # case 0 1 2
                if (cell_advanced > 2 and cell_advanced < 5): base += 2  # case 3 4
                if (cell_advanced == 5): base += 4  # case 5, pawn become extrem dangerous
                base += self.pawnWeight
            if (piece.piece_type == chess.KNIGHT): base = self.knightWeight
            if (piece.piece_type == chess.BISHOP): base = self.bishopWeight
            if (piece.piece_type == chess.ROOK): base = self.rookWeight
            if (piece.piece_type == chess.QUEEN): base = self.queenWeight

            if color > 0:
                score += color * base *  piece_value[piece.piece_type][i]
            else:
                score += color * base *  piece_value[piece.piece_type][63-i]

        return score

    def make_move(self, depth, best2_score):
        if (self.board.is_game_over()):
            return detect_end_score(self.board)
        if (depth == self.depth): return self.getScore()
        current_turn = self.board.turn

        if (depth == 0):
            if (current_turn == True): best2_score = -inf
            else: best2_score = inf

        if (depth == 2):
            current_2score = self.getScore()
            if (current_turn == True):
                if (current_2score > best2_score):
                    best2_score = current_2score
                elif (current_2score < best2_score):
                    return -inf
            else:
                if (current_2score > best2_score):
                    return inf
                elif (current_2score < best2_score):
                    best2_score = current_2score

        legal_move = list(self.board.legal_moves)
        
        tmp_array = []

        #sort by immediate score, dont try to make a sudden fucked move
        #-----------------------------
        for move in legal_move:
            pos = move.from_square
            piece = self.board.piece_at(pos)
            behind_piece = None 
            if 0 <= pos - 8 and pos - 8 < 64 and self.board.piece_at(pos-8):
                behind_piece = self.board.piece_at(pos-8)
            if 0 <= pos + 8 and pos + 8 < 64 and self.board.piece_at(pos+8):
                behind_piece = self.board.piece_at(pos+8)
            # 3 first move only use knight and pawn in front of king
            self.board.push(move)
            if self.start_state == 0 or ((pos < 16 or pos > 48) and self.start_state > 0 and (piece.piece_type == chess.KNIGHT or (piece.piece_type == chess.PAWN   and behind_piece and behind_piece.piece_type == chess.KING ))):
                tmp_array.append((move,self.getScore()))
            self.board.pop()
        tmp_array = list(tmp_array)
        tmp_array.sort(key = cmp_key)
        #------------------------------

        highest_score = -inf
        highest_move = legal_move[0]

        lowest_score = inf
        lowest_move = legal_move[0]

        for i in tmp_array:
            move = i[0]

            self.board.push(move)
            next_score = self.make_move(depth + 1,best2_score)
            self.board.pop()

            if (next_score > highest_score):
                highest_score = next_score
                highest_move = move
            if (next_score < lowest_score):
                lowest_score = next_score
                lowest_move = move

        #print(highest_score,'x',lowest_score)
        #exit(0)
        if (depth > 0):
            if (self.board.turn == True): return highest_score
            else: return lowest_score

        else:
            if (self.board.turn == True): return highest_move
            else: return lowest_move

    def make_next_move(self):
        if self.start_state > 0:
            self.start_state -= 1
        return self.make_move(0,0)