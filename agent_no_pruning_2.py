import chess
import chess.svg
inf = 1000000
board = chess.Board(chess.STARTING_BOARD_FEN)
def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0
piece_value = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, -31, 8, -7, -37, -36, -14, 3, -31, -22, 9, 5, -11, -10, -2, 3, -19, -26, 3, 10, 9, 6, 1, 0, -23, -17, 16, -2, 15, 14, 0, 15, -13, 7, 29, 21, 44, 40, 31, 44, 7, 78, 83, 86, 73, 102, 82, 85, 90, 100, 100, 100, 100, 105, 100, 100, 100],
    chess.KNIGHT: [-74, -23, -26, -24, -19, -35, -22, -69, -23, -15, 2, 0, 2, 0, -23, -20, -18, 10, 13, 22, 18, 15, 11, -14, -1, 5, 31, 21, 22, 35, 2, 0, 24, 24, 45, 37, 33, 41, 25, 17, 10, 67, 1, 74, 73, 27, 62, -2, -3, -6, 100, -36, 4, 62, -4, -14, -66, -53, -75, -75, -10, -55, -58, -70],
    chess.BISHOP: [-7, 2, -15, -12, -14, -15, -10, -10, 19, 20, 11, 6, 7, 6, 20, 16, 14, 25, 24, 15, 8, 25, 20, 15, 13, 10, 17, 23, 17, 16, 0, 7, 25, 17, 20, 34, 26, 25, 15, 10, -9, 39, -32, 41, 52, -10, 28, -14, -11, 20, 35, -42, -39, 31, 2, -22, -59, -78, -82, -76, -23, -107, -37, -50],
    chess.ROOK: [-30, -24, -18, 5, -2, -18, -31, -32, -53, -38, -31, -26, -29, -43, -44, -53, -42, -28, -42, -25, -25, -35, -26, -46, -28, -35, -16, -21, -13, -29, -46, -30, 0, 5, 16, 13, 18, -4, -9, -6, 19, 35, 28, 33, 45, 27, 25, 15, 55, 29, 56, 67, 55, 62, 34, 60, 35, 29, 33, 4, 37, 33, 56, 50],
    chess.QUEEN: [-39, -30, -31, -13, -31, -36, -34, -42, -36, -18, 0, -19, -15, -15, -21, -38, -30, -6, -13, -11, -16, -11, -16, -27, -14, -15, -2, -5, -1, -10, -20, -22, 1, -16, 22, 17, 25, 20, -13, -6, -2, 43, 32, 60, 72, 63, 43, 2, 14, 32, 60, -10, 20, 76, 57, 24, 6, 1, -8, -104, 69, 24, 88, 26],
    chess.KING:[17, 30, -3, -14, 6, -1, 40, 18, -4, 3, -14, -50, -57, -18, 13, 4, -47, -42, -43, -79, -64, -32, -29, -32, -55, -43, -52, -28, -51, -47, -8, -50, -55, 50, 11, -4, -19, 13, 0, -49, -62, 12, -57, 44, -67, 28, 37, -31, -32, 10, 55, 56, 56, 55, 10, 3, 4, 54, 47, -99, -99, 60, 83, -62]  # King value is often set to 0 in simple evaluations
}    
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

            if color > 0:
                score += color * piece_value[piece.piece_type][i] 
            else:
                score += color * piece_value[piece.piece_type][(7-i//8)*8+i%8] 

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

chess_weight_standard = [1,3,3,5,9,1]

move4_pruning_2best = Agent_pruning_best2(weight = chess_weight_standard,board = board, depth = 4)