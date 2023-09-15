import chess
import chess.svg
import random

# Evaluation function (simple material count)
def evaluate_board(board, player):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        if piece.color == chess.WHITE:
            if(player):
                score += piece_value[piece.piece_type][square]
            else:
                score += piece_value_1[piece.piece_type][square]
        else:
            if player:
                score -= piece_value[piece.piece_type][(7-square//8)*8+square%8]
            else:
                score -= piece_value_1[piece.piece_type][(7-square//8)*8+square%8]
    return score

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, maximizing_player)

    if maximizing_player:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Find the best move using Minimax with Alpha-Beta Pruning
def best_move(board, depth):
    best_move = None
    max_eval = float("-inf")
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, float("-inf"), float("inf"), False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

# Piece values (simple material count)
piece_value = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -3, -3, 0, 1, 1, 1, -1, -2, 0, 0, -2, -1, 1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    chess.KNIGHT: 3 * [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40, -30, 5, 10, 15, 15, 10, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10, 0, -30, -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
    chess.BISHOP: 3 * [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
    chess.ROOK: 5 * [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    chess.QUEEN: 9 * [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
    chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20]  # King value is often set to 0 in simple evaluations
}
piece_value_1 = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, -31, 8, -7, -37, -36, -14, 3, -31, -22, 9, 5, -11, -10, -2, 3, -19, -26, 3, 10, 9, 6, 1, 0, -23, -17, 16, -2, 15, 14, 0, 15, -13, 7, 29, 21, 44, 40, 31, 44, 7, 78, 83, 86, 73, 102, 82, 85, 90, 100, 100, 100, 100, 105, 100, 100, 100],
    chess.KNIGHT: 3 * [-74, -23, -26, -24, -19, -35, -22, -69, -23, -15, 2, 0, 2, 0, -23, -20, -18, 10, 13, 22, 18, 15, 11, -14, -1, 5, 31, 21, 22, 35, 2, 0, 24, 24, 45, 37, 33, 41, 25, 17, 10, 67, 1, 74, 73, 27, 62, -2, -3, -6, 100, -36, 4, 62, -4, -14, -66, -53, -75, -75, -10, -55, -58, -70],
    chess.BISHOP: 3 * [-7, 2, -15, -12, -14, -15, -10, -10, 19, 20, 11, 6, 7, 6, 20, 16, 14, 25, 24, 15, 8, 25, 20, 15, 13, 10, 17, 23, 17, 16, 0, 7, 25, 17, 20, 34, 26, 25, 15, 10, -9, 39, -32, 41, 52, -10, 28, -14, -11, 20, 35, -42, -39, 31, 2, -22, -59, -78, -82, -76, -23, -107, -37, -50],
    chess.ROOK: 5 * [-30, -24, -18, 5, -2, -18, -31, -32, -53, -38, -31, -26, -29, -43, -44, -53, -42, -28, -42, -25, -25, -35, -26, -46, -28, -35, -16, -21, -13, -29, -46, -30, 0, 5, 16, 13, 18, -4, -9, -6, 19, 35, 28, 33, 45, 27, 25, 15, 55, 29, 56, 67, 55, 62, 34, 60, 35, 29, 33, 4, 37, 33, 56, 50],
    chess.QUEEN: 9 * [-39, -30, -31, -13, -31, -36, -34, -42, -36, -18, 0, -19, -15, -15, -21, -38, -30, -6, -13, -11, -16, -11, -16, -27, -14, -15, -2, -5, -1, -10, -20, -22, 1, -16, 22, 17, 25, 20, -13, -6, -2, 43, 32, 60, 72, 63, 43, 2, 14, 32, 60, -10, 20, 76, 57, 24, 6, 1, -8, -104, 69, 24, 88, 26],
    chess.KING:[17, 30, -3, -14, 6, -1, 40, 18, -4, 3, -14, -50, -57, -18, 13, 4, -47, -42, -43, -79, -64, -32, -29, -32, -55, -43, -52, -28, -51, -47, -8, -50, -55, 50, 11, -4, -19, 13, 0, -49, -62, 12, -57, 44, -67, 28, 37, -31, -32, 10, 55, 56, 56, 55, 10, 3, 4, 54, 47, -99, -99, 60, 83, -62]  # King value is often set to 0 in simple evaluations
}

# Initialize the chessboard
board = chess.Board()

# Main game loop
while not board.is_game_over():
    best_move_white = best_move(board, depth=3)  # Adjust depth for AI strength
    board.push(best_move_white)
    # print("White's move:", best_move_white)
    continue 
    if board.turn == chess.WHITE:
        # White's turn
        best_move_white = best_move(board, depth=3)  # Adjust depth for AI strength
        board.push(best_move_white)
        print("White's move:", best_move_white)
    else:
        # Black's turn (random move for simplicity)
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves)
        your_move = random_move
        # your_move = input("Your move: ")
        while not your_move in legal_moves:
            your_move = input("Your move illegal. Move again: ")    
        board.push(your_move)
        print("Black's move:", your_move)

# Print the final board
print(board)

# Determine the result of the game
if board.is_checkmate():
    print("Checkmate!")
elif board.is_stalemate():
    print("Stalemate!")
elif board.is_insufficient_material():
    print("Insufficient material!")
elif board.is_seventyfive_moves():
    print("Draw (75-move rule)!")
elif board.is_fivefold_repetition():
    print("Draw (fivefold repetition)!")
else:
    print("Game result: In progress")
