import tkinter as tk
from tkinter import *
import random
from PIL import Image, ImageTk
from GameInstance import GameInstance
import fen_settings as s
from agent_no_pruning_2 import Agent_alphabeta_best2 
from agent_no_pruning import Agent_pruning_best2
from hanhai import HA_alpha_beta

import chess
import chess.engine
import chess.pgn

global canvasSize
canvasSize = 1

game = chess.pgn.Game()
game.headers["Event"] = "Example"

class TkFrame(Frame):
    # main Tk frame

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=RAISED)
        self.parent = parent
        self.img = {}
        self.initUI()

    def initUI(self):
        self.parent.title("Chess GUI")
        self.parent.minsize(687, 505)
        self.pack(fill=BOTH, expand=YES)


def drawPieces():
    global boardCanvas
    global canvasSize
    global app
    global flipped
    global count
    global g_board
    count = 0
    app.img = {}
    # dspboard = list(board)
    # if flipped: dspboard = reversed(board)
    # if boardHistoryPos != (len(boardHistory) - 1) and boardHistory != []:
    #	dspboard = list(boardHistory[boardHistoryPos])
    #	if flipped: dspboard = reversed(dspboard)
    for i in range(0, 64):

        #real_square_id = s.real_board_squares[::-1][i]

        correct_index = 8*(i//8) + 7-(i%8)  # Fixme - janky mapping between different board representations
        c = 63 - i
        # xTile goes from 0 to 7 (files)
        # yTile goes from 0 to 7 (ranks)
        xTile = (7 - c % 8)  # every 8th byte is a new row
        yTile = int(c / 8)  # each column is the nth byte in a row
        squareSize = int(canvasSize / 8)
        if squareSize < 1: squareSize = 1
        xDrawPos = (xTile * squareSize) - 3
        yDrawPos = (yTile * squareSize) - 3
        if flipped:
            xDrawPos = ((7 - xTile) * squareSize) - 3
            yDrawPos = ((7 - yTile) * squareSize) - 3

        mytext = str(i)
        #piece = str(board.piece_at(i))

        piece = g_board.piece_at(i)
        pieceFile = ''
        if piece:
            if piece.color:
                color = 'w'
            else:
                color = 'b'
        
            if color == 'w':
                if (piece.piece_type == chess.ROOK): pieceFile = 'texture/WR.png'  # white rook
                if (piece.piece_type == chess.KNIGHT): pieceFile = 'texture/WN.png'  # white knight
                if (piece.piece_type == chess.BISHOP): pieceFile = 'texture/WB.png'  # white bishop
                if (piece.piece_type == chess.QUEEN): pieceFile = 'texture/WQ.png'  # white queen
                if (piece.piece_type == chess.KING): pieceFile = 'texture/WK.png'  # white king
                if (piece.piece_type == chess.PAWN): pieceFile = 'texture/WP.png'  # white pawn
            elif color == 'b':
                if (piece.piece_type == chess.ROOK): pieceFile = 'texture/BR.png'  # black rook
                if (piece.piece_type == chess.KNIGHT): pieceFile = 'texture/BN.png'  # black knight
                if (piece.piece_type == chess.BISHOP): pieceFile = 'texture/BB.png'  # black bishop
                if (piece.piece_type == chess.QUEEN): pieceFile = 'texture/BQ.png'  # black queen
                if (piece.piece_type == chess.KING): pieceFile = 'texture/BK.png'  # black king
                if (piece.piece_type == chess.PAWN): pieceFile = 'texture/BP.png'  # black pawn

        if (pieceFile != ''):
            img = Image.open(pieceFile)
            img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
            app.img[count] = ImageTk.PhotoImage(img)
            boardCanvas.create_image(xDrawPos + 3, yDrawPos + 3, image=app.img[count], anchor=NW)

        count += 1


def appresize(event):
    global boardCanvas
    global canvasSize
    global app
    global root
    global boardImg

    boardCanvas.pack(expand=YES)
    # boardCanvas.config(width=30, height=30,bg="black")
    # boardCanvas.pack(expand=NO)
    # print app.winfo_height()
    appheight = app.winfo_height()
    appwidth = app.winfo_width()
    biggestDim = "height"
    canvasSize = appwidth - 202
    if appwidth > appheight:
        biggestDim = "width"
        canvasSize = appheight - 25
    if appwidth < (canvasSize + 202):
        canvasSize = appwidth - 202

    canvasSize = (int(canvasSize / 8) * 8)
    h = canvasSize
    w = canvasSize
    # boardImg.zoom(scalew, scaleh)
    boardCanvas.place(x=00, y=0, w=w, h=h)
    gameStateLabel.place(x=0, y=h + 1, w=300, h=20)
    drawBoard()
    drawPieces()
    root.update()


def drawBoard():
    global count
    global boardCanvas
    global canvasSize
    global colLight, colDark
    global app
    global boardImg
    global scalew, scaleh
    count = 0
    # img = Image.Open(file='board.PNG')
    img = Image.open("texture/board_2.png")
    img = img.resize((canvasSize, canvasSize), Image.ANTIALIAS)
    boardImg = ImageTk.PhotoImage(img)
    # boardImg.config(file='board.PNG')
    # boardImg = PhotoImage(file='board.PNG').zoom(320,320)
    # boardImg.width = scalew
    # boardImg.height = scaleh
    # print dir(boardImg)
    boardCanvas.delete("all")
    boardCanvas.create_image(3, 3, image=boardImg, anchor=NW)


def convertXYtoBoardIndex(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts cursor X, Y position to board array X, Y position
    returnX = int(x / squareSize)
    returnY = int(y / squareSize)
    if flipped:
        returnX = int((canvasSize - x) / squareSize)
        returnY = int((canvasSize - y) / squareSize)
    return (returnX, returnY)


def convertBoardIndextoXY(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts board index X, Y to tile draw position X, Y
    returnX = x * squareSize
    returnY = y * squareSize
    if flipped:
        returnX = int((7 - x) * squareSize)
        returnY = int((7 - y) * squareSize)
    return (returnX, returnY)


def islower(c):
    if c >= 'a' and c <= 'z': return True
    return False


def isupper(c):
    if c >= 'A' and c <= 'Z': return True
    return False

def convert(x):
    return x % 10 - 1 + (x // 10-2)*8

def canvasClick(event):
    global clickDragging
    global canvasSize

    global ClickStartScrPos
    global clickStartPiece
    global clickStartBoardIndex
    global lastTileXIndex, lastTileYIndex
    global clickStartSquare
    global g_board
    # print("{} {} {} \n".format(g_board.turn, p1, p2))
    if ((g_board.turn and p1 == "Human") or (not g_board.turn and p2 == "Human")):
        # human to move

        squareSize = canvasSize / 8
        mouseX = event.x
        mouseY = event.y

        # convert mouseX, mouseY to board array indices
        (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
        # convert board indices to screen X Y position of tiles
        (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)

        boardIndex = tileYIndex * 8 + tileXIndex
        boardIndex = 63 - boardIndex
        boardIndexX = 7 - (boardIndex % 8)
        boardIndexY = boardIndex // 8
        boardIndex = boardIndexY * 8 + boardIndexX
        #piece = board.piece_at(boardIndex)

        correct_index = 8*(7-tileYIndex) + tileXIndex  # Fixme - janky mapping between different board representations
        # print("{} {} {}".format(tileYIndex, tileXIndex, correct_index))
        # print("CanvasClick: ", 63-correct_index)
        # Check if it is your piece
        piece = g_board.piece_at(correct_index)
        # print(63-correct_index, piece.color)
        if (not piece or piece.color != g_board.turn): return

        # draw green square over tile
        # boardCanvas.draw.rect(pygScreen, (0,255,0), (tileScrX + 2, tileScrY + 2, 57, 57), 4)
        boardCanvas.create_rectangle(tileScrX + 3, tileScrY + 3, (tileScrX + squareSize - 2),
                                     (tileScrY + squareSize - 2), outline="#00FF00",
                                     width=6)
        clickDragging = True
        clickStartScrPos = (tileScrX, tileScrY)  # store top left screen X, Y for tile position
        clickStartBoardIndex = (tileXIndex, tileYIndex)
        clickStartPiece = piece
        lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex
        clickStartSquare = boardIndex


def canvasMotion(event):
    global lastTileScrX
    global lastTileScrY
    global lastTileXIndex
    global lastTileYIndex
    global canvasSize
    global clickStartBoardIndex
    global clickStartSquare
    global clickEndSquare

    if not clickDragging: return
    squareSize = canvasSize / 8
    mouseX = event.x
    mouseY = event.y
    if (mouseX > canvasSize or mouseX < 0 or mouseY > canvasSize or mouseY < 0): return
    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    # convert board indices to screen X Y position of tiles
    (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)

    # clickStartBoardIndex = (tileXIndex, tileYIndex)
    # calculate boardIndex = board[] square index
    boardIndex = tileYIndex * 8 + tileXIndex
    boardIndex = 63 - boardIndex
    boardIndexX = 7 - (boardIndex % 8)
    boardIndexY = boardIndex // 8
    boardIndex = boardIndexY * 8 + boardIndexX
    clickEndSquare = boardIndex
    move = chess.Move(from_square=clickStartSquare, to_square=boardIndex)
    # print("canvasMotion: ", move)
    if move in list(g_board.legal_moves):
        # draw green square over moused over square
        boardCanvas.create_rectangle(tileScrX + 3, tileScrY + 3, (tileScrX + (squareSize - 2)),
                                     (tileScrY + (squareSize - 2)),
                                     outline="#00FF00", width=6)
        if ((lastTileXIndex != tileXIndex) or (lastTileYIndex != tileYIndex)):  # user mouses to a new square
            if (clickStartBoardIndex != (lastTileXIndex, lastTileYIndex)):  # don't redraw if it's the start square
                # g_board.push(move)
                # print(g_board)
                redrawTile(lastTileXIndex, lastTileYIndex)  # redraw over last square (to remove green rect)

        lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex


def canvasRelease(event):
    global clickDragging
    global root
    global clickStartSquare
    global p1, p2
    global gameStateVar
    global clickEndSquare
    global g_board

    if (clickDragging == False):
        return

    clickDragging = False
    mouseX = event.x
    mouseY = event.y

    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    # convert board indices to X Y position of tiles
    # (tileScrX, tileScrY) = convertBoardIndextoXY(tileXindex, tileYindex)
    # startSquare = (clickStartBoardIndex[0], clickStartBoardIndex[1])
    # endSquare = (tileXindex, tileYindex)

    endSquare = clickEndSquare
    # startSquare = clickStartSquare[1] * 8 + clickStartSquare[0]
    # startSquare = 63 - startSquare
    startSquare = clickStartSquare

    move = chess.Move(from_square=startSquare, to_square=endSquare)

    if move in list(g_board.legal_moves):
        g_board.push(move)
        # print(g_board)
        # board.make_move(legalmove)
        if (g_board):
            gameStateVar.set("White to move.")
        else:
            gameStateVar.set("Black to move.")

    drawBoard()
    drawPieces()
    root.update()
    if g_board.is_game_over():
        gameStateVar.set("End of game.")
        root.update()
        return


    if (g_board.turn and p1 != "Human"):
        getAIMove(turn='White')
    elif (not g_board.turn and p2 != "Human"):
        getAIMove(turn='Black')


def getAIMove(turn):
    # global board
    global root
    global canvasSize
    global gameStateVar
    global pvmove
    global p1
    global p2
    global g_board
    global engine_1
    global engine_2

    lastpvmovestr = ""
    # if (p1 == "AI" and board.turn): engine = engine1
    # elif (p2 == "AI" and not board.turn): engine = engine2
    if g_board.turn:
        move = engine_1.make_next_move()
    else:
        move = engine_2.make_next_move()

    # print("Move: ", move)
    if g_board.is_game_over():
        gameStateVar.set("End of game.")
        root.update()
        gameinprogress = False
    else:
        #print(move)
        #board.push_uci(str(move))
        # board.make_move(move)
        # move = chess.Move(convert(int(move[0])), convert(int(move[1])))
        # print(move)
        g_board.push(move)
        # print("AI: ", g_board)
        drawBoard()
        drawPieces()

    if g_board.is_game_over():
        gameStateVar.set("End of game.")
        root.update()
        gameinprogress = False
        print('no legal')

    else:
        if (g_board.turn):
            gameStateVar.set("White to move.")
        else:
            gameStateVar.set("Black to move.")
        root.update()
        if (p1 == "AI" and g_board.turn):
            getAIMove(turn='white')
        elif (p2 == "AI" and not g_board.turn):
            getAIMove(turn='black')
        # print("Done")


def redrawTile(x, y):
    global count
    global flipped
    global canvasSize
    count = 0
    #colLight = (240,218,181)
    #colDark = (181,135,99)
    #colLight = '#%02x%02x%02x' % colLight
    colDark = '#b58763'
    colLight = '#f0dab5'
    #colDark = '#%02x%02x%02x' % colDark

    squareSize = canvasSize / 8
    # redraws a tile with its piece
    boardIndex = y * 8 + x
    boardIndex = 63 - boardIndex
    boardIndexX = 7 - (boardIndex % 8)
    boardIndexY = int(boardIndex / 8)
    boardIndex = boardIndexY * 8 + boardIndexX
    i = x
    j = y
    # print(i, j)
    xpos = (i * squareSize) - 3
    ypos = (j * squareSize) - 3  # each tile is 60x60 px
    if flipped:
        xpos = ((7 - i) * squareSize)
        ypos = ((7 - j) * squareSize)
    col = colLight
    if (((i + j) % 2)): col = colDark  # alternate tiles are dark
    # redraw tile
    drawEndX = (xpos + squareSize)
    drawEndY = (ypos + squareSize)
    if flipped:
        drawEndX = ((7 - xpos) + squareSize)
        drawEndY = ((7 - ypos) + squareSize)

    tempDrawDir = 1
    if (not g_board.turn) and (flipped == True): tempDrawDir = 0
    if (g_board.turn) and (flipped == True): tempDrawDir = 0
    boardCanvas.create_rectangle(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, (xpos + squareSize + 3 * tempDrawDir),
                                 (ypos + squareSize + 3 * tempDrawDir), fill=col, outline=col)
    # redraw piece
    #piece = str(board.piece_at(boardIndex))
    correct_index = 8 * (boardIndex // 8) + 7 - (boardIndex % 8)  # Fixme - janky mapping between different board representations
    #real_square_id = s.real_board_squares[::-1][boardIndex]

    piece = g_board.piece_at(correct_index)
    pieceFile = ''
    if piece:
        if piece.color:
            color = 'w'
        else:
            color = 'b'
    
        if color == 'w':
            if (piece.piece_type == chess.ROOK): pieceFile = 'texture/WR.png'  # white rook
            if (piece.piece_type == chess.KNIGHT): pieceFile = 'texture/WN.png'  # white knight
            if (piece.piece_type == chess.BISHOP): pieceFile = 'texture/WB.png'  # white bishop
            if (piece.piece_type == chess.QUEEN): pieceFile = 'texture/WQ.png'  # white queen
            if (piece.piece_type == chess.KING): pieceFile = 'texture/WK.png'  # white king
            if (piece.piece_type == chess.PAWN): pieceFile = 'texture/WP.png'  # white pawn
        elif color == 'b' and piece:
            if (piece.piece_type == chess.ROOK): pieceFile = 'texture/BR.png'  # black rook
            if (piece.piece_type == chess.KNIGHT): pieceFile = 'texture/BN.png'  # black knight
            if (piece.piece_type == chess.BISHOP): pieceFile = 'texture/BB.png'  # black bishop
            if (piece.piece_type == chess.QUEEN): pieceFile = 'texture/BQ.png'  # black queen
            if (piece.piece_type == chess.KING): pieceFile = 'texture/BK.png'  # black king
            if (piece.piece_type == chess.PAWN): pieceFile = 'texture/BP.png'  # black pawn
    if (pieceFile != ''):
        # app.img[count] = ImageTk.PhotoImage(file=pieceFile)
        # boardCanvas.create_image((xpos), (ypos), image=app.img[count], anchor=NW)

        img = Image.open(pieceFile)
        img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
        app.img[boardIndex] = ImageTk.PhotoImage(img)
        boardCanvas.create_image(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, image=app.img[boardIndex], anchor=NW)
    count += 1
    pass


def main(player1, player2):
    global p1
    global p2
    global p1engine, p2engine
    global boardCanvas
    global canvasSize
    global app
    global root
    global g_board
    global clickDragging
    global flipped
    global gameStateVar, gameStateLabel
    global engine_1
    global engine_2
    global keeprunning
    global gameinprogerss

    gameinprogress = False

    flipped = False
    clickDragging = False

    root = tk.Tk()
    x = 100
    y = 100
    w = 687
    h = 505
    oldappheight = h
    oldappwidth = w
    geostring = "%dx%d+%d+%d" % (w, h, x, y)

    root.geometry(geostring)
    app = TkFrame(root)
    app.bind("<Configure>", appresize)

    boardCanvas = Canvas(app, width=480, height=480)

    boardCanvas.bind("<Button-1>", canvasClick)
    boardCanvas.bind("<ButtonRelease-1>", canvasRelease)
    boardCanvas.bind("<B1-Motion>", canvasMotion)

    boardCanvas.pack(expand=YES)
    boardCanvas.place(x=0, y=0)

    gameStateVar = StringVar()
    g_board = chess.Board()
    gameStateLabel = Label(root, font=('calibri', 15), justify=LEFT, anchor="w", textvariable=gameStateVar)
    gameStateLabel.pack()
    gameStateLabel.place(x=0, y=480)
    chess_weight_standard = [1,3,3,5,9,1]
    HA_chess_weight_standard = [100,280,320,479,929,100,1000000000]

    p1 = player1
    p2 = player2

    if p1 == "AI":
        engine_1 = Agent_pruning_best2(weight = chess_weight_standard,board = g_board, depth = 3)    
    if p2 == "AI":
        engine_2 = HA_alpha_beta(weight = HA_chess_weight_standard,board = g_board, depth = 3)

    initGame(p1, p2)
    drawBoard()
    drawPieces()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def on_closing():
    global root
    global engine1
    global engine2
    root.destroy()


def initGame(player1, player2):
    global gameinprogress
    global gameStateVar
    global g_board

    gameinprogress = True
    gameStateVar.set("White to move.")
    print(p1, p2)
    if (p1 == "AI" and g_board.turn):
        getAIMove(turn='white')

    elif (p2 == "AI" and not g_board.turn):
        getAIMove(turn='black')

if __name__ == "__main__":
    p1 = input("Player1: ")
    p2 = input("Player2: ")
    main(p1, p2)
# cProfile.run('foo()')
