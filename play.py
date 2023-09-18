import chess
import tkinter as tk
from chess.svg import board as svg_board
from agent_no_pruning import Agent_alpha_beta
from agent_no_pruning_2 import Agent_pruning_best2
board = chess.Board()
chess_weight_standard = [1,3,3,5,9,1]

agent_2 = Agent_pruning_best2(weight = chess_weight_standard,board = board, depth = 3)
agent_1 = Agent_alpha_beta(weight = chess_weight_standard,board = board, depth = 2)
step = 0
import pdb 
pdb.set_trace()


while(not board.is_game_over() and step <= 5000):
    bot_move1 = agent_1.best_move(True)
    # i have to modified this a litte bit, how can we completely get rid of best2_score params ?
    print("Player1: ", bot_move1)
    board.push(bot_move1)
    
    # print(agent_2.board)
    #print('--------------------------------')
    #print(board)
    if board.is_game_over():
        break
    bot_move2 = agent_2.make_next_move(0, 0)
    print("Player2: ",bot_move2)
    board.push(bot_move2)
    #print('--------------------------------')
    #print(board)
    step += 1
    # print(f'Score at step {step} is :',agent1.getScore())
# Print the final board
# print(board)

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