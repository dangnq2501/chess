import chess
import chess.svg
import random
inf = 1000000

board = chess.Board(chess.STARTING_BOARD_FEN)
def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0
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
                    base = self.pawnWeight + self.pawnAdvance*(i//8 - 1)
                else:
                    base = self.pawnWeight + self.pawnAdvance*(6 - i//8)
            if (piece.piece_type == chess.KNIGHT): base = self.knightWeight
            if (piece.piece_type == chess.BISHOP): base = self.bishopWeight
            if (piece.piece_type == chess.ROOK): base = self.rookWeight
            if (piece.piece_type == chess.QUEEN): base = self.queenWeight

            score += color * base 

        return score

    def make_next_move(self, depth, best2_score):
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



        highest_score = -inf
        highest_move = legal_move[0]

        lowest_score = inf
        lowest_move = legal_move[0]
        for move in legal_move:

            self.board.push(move)
            next_score = self.make_next_move(depth + 1,best2_score)
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