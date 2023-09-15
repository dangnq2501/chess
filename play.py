import chess
import chess.svg

board = chess.Board(chess.STARTING_BOARD_FEN) #starting position
print(board)


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

# print(board.is_game_over())
# is it ended ?

#print(board.has_insufficient_material(True))
# return to False if white (True) can still win the game
# we may want to avoid state when we cant win the game ==> negative factor here

#print(board.can_claim_draw())
# Checks if the player to move can claim a draw by the fifty-move rule or by threefold repetition.

#print(board.piece_at(1))
# get the piece at position 0,1,2,3,4,5,....63 (A1 = 0, B1 = 1,..)

# legal_moves = list(board.legal_moves)
# print(legal_moves)
# convert legal move to a list and iterate through it

# possible_knight_attack = list(board.attacks(1))
# print(possible_knight_attack)
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
lis =[         [4, 54, 47, -99, -99, 60, 83, -62],         [-32, 10, 55, 56, 56, 55, 10, 3],         [-62, 12, -57, 44, -67, 28, 37, -31],         [-55, 50, 11, -4, -19, 13, 0, -49],         [-55, -43, -52, -28, -51, -47, -8, -50],         [-47, -42, -43, -79, -64, -32, -29, -32],         [-4, 3, -14, -50, -57, -18, 13, 4],         [17, 30, -3, -14, 6, -1, 40, 18],      ]
res = []
for i in range(8):
    for x in lis[7-i]:
        res.append(x)

print(res)