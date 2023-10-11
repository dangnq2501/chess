
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
piece_value = {
    chess.PAWN:[0, 0, 0, 0, 0, 0, 0, 0, -31, 3, -14, -36, -37, -7, 8, -31, -19, 3, -2, -10, -11, 5, 9, -22, -23, 0, 1, 6, 9, 10, 3, -26, -13, 15, 0, 14, 15, -2, 16, -17, 7, 44, 31, 40, 44, 21, 29, 7, 90, 85, 82, 102, 73, 86, 83, 78, 100, 100, 100, 105, 100, 100, 100, 100],
    chess.KNIGHT: [-69, -22, -35, -19, -24, -26, -23, -74, 
                   -20, -23, 0, 2, 0, 2, -15, -23, 
                   -14, 11, 15, 18, 22, 13, 10, -18, 
                   0, 2, 35, 22, 21, 31, 5, -1, 17, 25, 41, 33, 37, 45, 24, 24, -2, 62, 27, 73, 74, 1, 67, 10, -14, -4, 62, 4, -36, 100, -6, -3, -70, -58, -55, -10, -75, -75, -53, -66],
    chess.BISHOP: [-10, -10, -15, -14, -12, -15, 2, -7, 16, 20, 6, 7, 6, 11, 20, 19, 15, 20, 25, 8, 15, 24, 25, 14, 7, 0, 16, 17, 23, 17, 10, 13, 10, 15, 25, 26, 34, 20, 17, 25, -14, 28, -10, 52, 41, -32, 39, -9, -22, 2, 31, -39, -42, 35, 20, -11, -50, -37, -107, -23, -76, -82, -78, -59],
    chess.ROOK: [-32, -31, -18, -2, 5, -18, -24, -30, -53, -44, -43, -29, -26, -31, -38, -53, -46, -26, -35, -25, -25, -42, -28, -42, -30, -46, -29, -13, -21, -16, -35, -28, -6, -9, -4, 18, 13, 16, 5, 0, 15, 25, 27, 45, 33, 28, 35, 19, 60, 34, 62, 55, 67, 56, 29, 55, 50, 56, 33, 37, 4, 33, 29, 35],
    chess.QUEEN: [-42, -34, -36, -31, -13, -31, -30, -39, -38, -21, -15, -15, -19, 0, -18, -36, -27, -16, -11, -16, -11, -13, -6, -30, -22, -20, -10, -1, -5, -2, -15, -14, -6, -13, 20, 25, 17, 22, -16, 1, 2, 43, 63, 72, 60, 32, 43, -2, 24, 57, 76, 20, -10, 60, 32, 14, 26, 88, 24, 69, -104, -8, 1, 6],
    chess.KING: [18, 40, -1, 6, -14, -3, 30, 17, 4, 13, -18, -57, -50, -14, 3, -4, -32, -29, -32, -64, -79, -43, -42, -47, -50, -8, -47, -51, -28, -52, -43, -55, -49, 0, 13, -19, -4, 11, 50, -55, -31, 37, 28, -67, 44, -57, 12, -62, 3, 10, 55, 56, 56, 55, 10, -32, -62, 83, 60, -99, -99, 47, 54, 4] # King value is often set to 0 in simple evaluations
}
def cmp_func(a,b):
    if (a[1] > b[1]): return 1
    else: return -1
from functools import cmp_to_key
cmp_key = cmp_to_key(cmp_func)
def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0

class HA_alpha_beta():
    def __init__(self, weight : list, board : chess.Board, depth):
        self.pawnWeight = weight[0]
        self.knightWeight = weight[1]
        self.bishopWeight = weight[2]
        self.rookWeight = weight[3]
        self.queenWeight = weight[4]
        self.kingWeight = weight[5]
        self.pawnAdvance = 1
        self.checkmate = weight[6]
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
            if piece.color:
                score += color * base * piece_value[piece.piece_type][i]
            else:
                score += color * base * piece_value[piece.piece_type][(7-i//8)*8+i%8]

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