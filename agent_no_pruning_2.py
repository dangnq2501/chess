import chess
import chess.svg
import random

inf = 100000000

def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True):
        return inf
    elif (outcome.winner == False):
        return -inf
    else:
        return 0

def cmp_func(a,b):
    if (a[1] > b[1]): return 1
    else: return -1
from functools import cmp_to_key
cmp_key = cmp_to_key(cmp_func)

class Agent_alphabeta_best2():
    def __init__(self, weight: list, board: chess.Board, depth):
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
        # we will get protective stuff, folk piece, checkmate significant etcetera,... later

    def count_pieces(self):
        cnt = 0
        for i in range(64):
            if self.board.piece_at(i):
                cnt += 1
        return cnt

    def getScore(self):
        score = 0
        for i in range(0, 64):
            piece = self.board.piece_at(i)
            if (piece is None): continue
            color = 1
            base = 0
            if (piece.color == False): color = -1
            if (piece.piece_type == chess.PAWN):
                if (piece.color == True):
                    cell_advanced = self.pawnAdvance * (i // 8 - 1)
                else:
                    cell_advanced = self.pawnAdvance * (6 - i // 8)

                if (cell_advanced > 0 and cell_advanced <= 2): base += 1  # case 0 1 2
                if (cell_advanced > 2 and cell_advanced < 5): base += 2  # case 3 4
                if (cell_advanced == 5): base += 4  # case 5, pawn become extrem dangerous
                base += self.pawnWeight
            if (piece.piece_type == chess.KNIGHT): base = self.knightWeight
            if (piece.piece_type == chess.BISHOP): base = self.bishopWeight
            if (piece.piece_type == chess.ROOK): base = self.rookWeight
            if (piece.piece_type == chess.QUEEN): base = self.queenWeight

            score += color * base

        return score

    # Minimax algorithm with Alpha-Beta Pruning
    def minimax(self, depth, alpha, beta, best2_score):
        if (self.board.is_game_over()):
            return detect_end_score(self.board)
        if (depth == self.depth): return self.getScore()

        #init best2 score, too lazy to properly merging shit together
        #-------------------------------------------
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
        #----------------------------------------------------

        maximizing_player = self.board.turn
        legal_moves = list(self.board.legal_moves)
        random.shuffle(legal_moves)

        tmp_array = []
        # sort by immediate score, dont try to make a sudden fucked move
        # -----------------------------
        for move in legal_moves:
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
                tmp_array.append((move, self.getScore()))
            self.board.pop()
        tmp_array = list(tmp_array)
        tmp_array.sort(key=cmp_key)
        # ------------------------------


        best_move = legal_moves[0]
        # random.shuffle(legal_moves)
        if maximizing_player:
            max_eval = -inf
            for i in tmp_array:
                move = i[0]
                self.board.push(move)
                eval = self.minimax(depth + 1, alpha, beta, best2_score)
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if (depth == 0):
                return best_move
            else:
                return max_eval
        else:
            min_eval = inf
            for i in tmp_array:
                self.board.push(move)
                eval = self.minimax(depth + 1, alpha, beta, best2_score)
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if (depth == 0):
                return best_move
            else:
                return min_eval

    # Find the best move using Minimax with Alpha-Beta Pruning
    def make_next_move(self):
        if self.start_state > 0:
            self.start_state -= 1
        return self.minimax(0, -inf, inf, 0)

if __name__ == "__main__":
    board = chess.Board()
    chess_weight_standard = [1,3,3,5,9,1]
    engine = Agent_alphabeta_best2(chess_weight_standard, board, 3)
    print(engine.make_next_move())