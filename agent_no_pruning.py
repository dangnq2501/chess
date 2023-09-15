import chess
import chess.svg

inf = 1000000

board = chess.Board(chess.STARTING_BOARD_FEN) #starting position
print(board)
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

def detect_end_score(board):
    outcome = board.outcome()
    if (outcome.winner == True): return inf
    elif (outcome.winner == False): return -inf
    else: return 0

class Agent_no_pruning():
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

    def make_next_move(self,depth):
        if (self.board.is_game_over()):
            return detect_end_score(self.board)
        if (depth == self.depth): return self.getScore()
        legal_move = list(self.board.legal_moves)

        current_turn = self.board.turn

        highest_score = -1000000
        highest_move = legal_move[0]

        lowest_score = 1000000
        lowest_move = legal_move[0]
        for move in legal_move:

            self.board.push(move)
            next_score = self.make_next_move(depth + 1)
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

chess_weight_standard = [1,3,3,5,9,1]

move4_pruning_2best = Agent_pruning_best2(weight = chess_weight_standard,board = board, depth = 4)
move3_no_pruning_bot = Agent_no_pruning(weight = chess_weight_standard,board = board, depth = 3)
move2_no_pruning_bot = Agent_no_pruning(weight = chess_weight_standard,board = board, depth = 2)
move1_no_pruning_bot = Agent_no_pruning(weight = chess_weight_standard,board = board, depth = 1)

'''
print(move3_bot.make_next_move(0))

board.push(chess.Move.from_uci('g8h6'))
print(move3_bot.getScore())

board.pop()
board.push(chess.Move.from_uci('d5e4'))
print(move3_bot.getScore())
exit(0)
'''

def human_vs_agent(agent):
    while (board.is_game_over() == False):
        legal_move = board.legal_moves
        while (True):
            print('enter your move : ')
            move_str = input()
            player_move = chess.Move.from_uci(move_str)
            if (player_move in legal_move):
                board.push(player_move)
                break
            else:
                print('illegal move, move again')
        print('--------------------------------')
        print(board)

        bot_move = agent.make_next_move(0)
        print(bot_move)
        board.push(bot_move)
        print('--------------------------------')
        print(board)

def agent_vs_agent(agent1, agent2):
    step = 0
    while(board.is_game_over() == False and step <= 500):
        bot_move1 = agent1.make_next_move(0,0)
        # i have to modified this a litte bit, how can we completely get rid of best2_score params ?
        #print(bot_move1)
        board.push(bot_move1)
        #print('--------------------------------')
        #print(board)

        bot_move2 = agent2.make_next_move(0)
        #print(bot_move2)
        board.push(bot_move2)
        #print('--------------------------------')
        #print(board)
        step += 1
        print(f'Score at step {step} is :',agent1.getScore())

#human_vs_agent(move1_no_pruning_bot)
agent_vs_agent(move4_pruning_2best,move3_no_pruning_bot)