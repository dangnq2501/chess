import chess
import chess.svg
import random
inf = 1000000

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
# piece_value = {
#     chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -3, -3, 0, 1, 1, 1, -1, -2, 0, 0, -2, -1, 1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
#     chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40, -30, 5, 10, 15, 15, 10, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10, 0, -30, -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
#     chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
#     chess.ROOK: [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
#     chess.QUEEN: [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
#     chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20]  # King value is often set to 0 in simple evaluations
# }

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
                score += color * base 
            else:
                score += color * base 

        return score

    # Minimax algorithm with Alpha-Beta Pruning
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.getScore()
        
        legal_moves = list(self.board.legal_moves)
        # random.shuffle(legal_moves)
        if maximizing_player:
            max_eval = float("-inf")
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Find the best move using Minimax with Alpha-Beta Pruning
    def best_move(self, maximizing_player):
        best_move = None
        legal_moves = list(self.board.legal_moves)
        random.shuffle(legal_moves)
        # print(sellegal_moves)
        
       
        if maximizing_player:
            max_eval = float("-inf")
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(self.depth + 4-self.count_pieces()//8, float("-inf"), float("inf"), False)
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
        else:
            min_eval = float("inf")
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(self.depth + 4-self.count_pieces()//8, float("-inf"), float("inf"), True)
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
        return best_move


