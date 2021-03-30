import chess
from chessboard import display
import time
import random
import matplotlib.pyplot as plt
import numpy as np

PIECES = ["p","n","b","r","q","k"]
VALUES = [1,3,3,5,9,100_000]

board = chess.Board()

ALLTIMEMAX = []
#1 = white -1 = black
def evaluateFenString(fen,player,turn):
    penalty = 0
    if chess.Board(fen).is_checkmate():
        if (player == 1 and turn == 1) or (player == -1 and turn == 0):
            penalty = 10_000
        if (player == 1 and turn == 0) or (player == -1 and turn == 1):
            penalty = -10_000
    fen = fen.split(" ")[0]
   
    fenWithoutSpaces = ""
    for letter in fen.replace("/",""):
          if not letter.isdigit():
                fenWithoutSpaces = fenWithoutSpaces + letter
    whiteSumm = 0
    blackSumm = 0
    for piece in fenWithoutSpaces:
        if piece.isupper():
            whiteSumm += VALUES[PIECES.index(piece.lower())]
        else:
            blackSumm += VALUES[PIECES.index(piece.lower())]
 
    
    # summe zwischen weiß und schwarz abhängig von player input
    return (whiteSumm*player + blackSumm*(-1*player)) + penalty

def evaluateFenStringControll(fen,player,turn):
    penalty = 0
    if chess.Board(fen).is_checkmate():
        if (player == 1 and turn == 1) or (player == -1 and turn == 0):
            penalty = 10_000
        if (player == 1 and turn == 0) or (player == -1 and turn == 1):
            penalty = -10_000
    fen = fen.split(" ")[0]
   
    fenWithoutSpaces = ""
    for letter in fen.replace("/",""):
          if not letter.isdigit():
                fenWithoutSpaces = fenWithoutSpaces + letter
    whiteSumm = 0
    blackSumm = 0
    for piece in fenWithoutSpaces:
        if piece.isupper():
            whiteSumm += VALUES[PIECES.index(piece.lower())]
        else:
            blackSumm += VALUES[PIECES.index(piece.lower())]
 
    
    # summe zwischen weiß und schwarz abhängig von player input
    return (whiteSumm*player + blackSumm*(-1*player)) + penalty


def evaluateFenStringControll(fen,player,turn):
    penalty = 0
    #checking for checkmate and giving penaltys based on it
    if chess.Board(fen).is_checkmate():
        if (player == 1 and turn == 1) or (player == -1 and turn == 0):
            penalty = 10_000
        if (player == 1 and turn == 0) or (player == -1 and turn == 1):
            penalty = -10_000
    #cleaning the fenString
    fen = fen.split(" ")[0]
   
    fenWithoutSpaces = ""
    for letter in fen.replace("/",""):
          if not letter.isdigit():
                fenWithoutSpaces = fenWithoutSpaces + letter
    #initzializing summs and checking for the pieces
    whiteSumm = 0
    blackSumm = 0
    for piece in fenWithoutSpaces:
        if piece.isupper():
            whiteSumm += VALUES[PIECES.index(piece.lower())]
        else:
            blackSumm += VALUES[PIECES.index(piece.lower())]
    b = chess.Board(fen)
    #checking which squares are attacked by whom and adding it to the evaluation
    for i in range(0,8):
        for x in range(0,8):
            if b.is_attacked_by(chess.WHITE,chess.square(i,x)):
                whiteSumm += 1
            if b.is_attacked_by(chess.BLACK,chess.square(i,x)):
                blackSumm += 1

    # summe zwischen weiß und schwarz abhängig von player input
    return (whiteSumm*player + blackSumm*(-1*player)) + penalty


def evaluateFenStringControllSeperate(fen,player,turn):
    penalty = 0
    if chess.Board(fen).is_checkmate():
        if (player == 1 and turn == 1) or (player == -1 and turn == 0):
            penalty = 10_000
        if (player == 1 and turn == 0) or (player == -1 and turn == 1):
            penalty = -10_000
    fen = fen.split(" ")[0]
   
    fenWithoutSpaces = ""
    for letter in fen.replace("/",""):
          if not letter.isdigit():
                fenWithoutSpaces = fenWithoutSpaces + letter
    whiteSumm = 0
    blackSumm = 0
    for piece in fenWithoutSpaces:
        if piece.isupper():
            whiteSumm += VALUES[PIECES.index(piece.lower())]
        else:
            blackSumm += VALUES[PIECES.index(piece.lower())]
 
    
    # summe zwischen weiß und schwarz abhängig von player input
    return (whiteSumm*player + blackSumm*(-1*player)) + penalty


def generateMoves(fen,isTurn,player,game_min):
    board = chess.Board(fen)
    legalMoves = movesToList(board.legal_moves)
    secondDegreeMoves = []
    #generating all answers to the legal moves
    for lM in legalMoves:
        board.push(lM)
        secondDegreeMoves.append(movesToList(board.legal_moves))
        board.pop()
    globalEvaluation = []
    #looping through all possible outcomes and evaluating them
    for lM in legalMoves:
        board.push(lM)
        localEvaluation = []
        for m in secondDegreeMoves[legalMoves.index(lM)]:
            if board.is_checkmate():
                localEvaluation.append(0)
            else:
                board.push(m)
                localEvaluation.append(evaluateFenString(board.fen(),player,isTurn))
                board.pop()
        if len(secondDegreeMoves[legalMoves.index(lM)]) == 0:
            if board.is_checkmate():
               localEvaluation.append(100_000)
               return lM, game_min
            if board.is_stalemate():
                localEvaluation.append(0)
            else:
                localEvaluation.append(0)
        board.pop()
        if len(localEvaluation) > 0:
            globalEvaluation.append(min(localEvaluation))
        else:
            globalEvaluation.append(min(localEvaluation))
    #check if the best worst move is higher valued than before
    if game_min < max(globalEvaluation):
        game_min = max(globalEvaluation)
    #if there are multiple best moves, select one at random
    if globalEvaluation.count(max(globalEvaluation)) > 1:
        bestMoves = []
        for move in legalMoves:
            if globalEvaluation[legalMoves.index(move)] == max(globalEvaluation):
                bestMoves.append(move)
        return bestMoves[random.randint(0,len(bestMoves)-1)], game_min
    else:
        return legalMoves[globalEvaluation.index(max(globalEvaluation))], game_min
    
def gM(fen,isTurn,player,game_min):
    board = chess.Board(fen)
    legalMoves = movesToList(board.legal_moves)
    secondDegreeMoves = []
    #generating all answers to the legal moves
    for lM in legalMoves:
        board.push(lM)
        secondDegreeMoves.append(movesToList(board.legal_moves))
        board.pop()
    globalEvaluation = []
    #looping through all possible outcomes and evaluating them
    for lM in legalMoves:
        board.push(lM)
        localEvaluation = []
        for m in secondDegreeMoves[legalMoves.index(lM)]:
            if board.is_checkmate():
                localEvaluation.append(0)
            else:
                board.push(m)
                localEvaluation.append(evaluateFenStringControll(board.fen(),player,isTurn))
                board.pop()
        if len(secondDegreeMoves[legalMoves.index(lM)]) == 0:
            if board.is_checkmate():
               localEvaluation.append(100_000)
               return lM, game_min
            if board.is_stalemate():
                localEvaluation.append(0)
            else:
                localEvaluation.append(0)
        board.pop()
        if len(localEvaluation) > 0:
            globalEvaluation.append(min(localEvaluation))
        else:
            globalEvaluation.append(min(localEvaluation))
    #check if the best worst move is higher valued than before
    if game_min < max(globalEvaluation):
        game_min = max(globalEvaluation)
    #if there are multiple best moves, select one at random
    if globalEvaluation.count(max(globalEvaluation)) > 1:
        bestMoves = []
        for move in legalMoves:
            if globalEvaluation[legalMoves.index(move)] == max(globalEvaluation):
                bestMoves.append(move)
        return bestMoves[random.randint(0,len(bestMoves)-1)], game_min
    else:
        return legalMoves[globalEvaluation.index(max(globalEvaluation))], game_min
    

    
                      
def movesToList(legalMovesObject):
    moves = []
    for move in legalMovesObject:
        moves.append(move)
    return moves
        
#player 1 = white player -1 = black    
def playGame(pauseTime,player,showDisplay=False,playYourself=False):
    if showDisplay:
        display.start()
    board = chess.Board()
    pgn = []
    game_min = -100_000_000
    while True:
        #generating moves based on the turn
        if board.turn ==  bool(player+1):
            move, game_min = generateMoves(board.fen(),board.turn,player,game_min)
        else:
            if not playYourself:
                
                #move = movesToList(board.legal_moves)[random.randint(0,len(movesToList(board.legal_moves))-1)]
                move,_ = gM(board.fen(),board.turn,-player,game_min)
            else:
                while True:
                    moveInput = input("enter your move:")
                    try:
                        move = chess.Move.from_uci(moveInput)
                        print(move)
                        if move in board.legal_moves:
                            break
                        else:
                            print("please enter a legal move!")
                    except ValueError:
                        print("Please enter a real move!")
        #moving, displaying, checking if the game has ended
        time.sleep(pauseTime)
        pgn.append(move)
        board.push(move)
        if showDisplay:
            display.update(board.fen())
        if board.is_checkmate():
            if board.turn == bool(player+1):
                      print("newOne")
                      return False,pgn,board.fen(),game_min
                      
            else:
                      print("mate")
                      return True, pgn, board.fen(),game_min
                      
        if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_threefold_repetition() or board.is_seventyfive_moves() or board.can_claim_fifty_moves():
            print("No one")
            return None,pgn,board.fen(),game_min
            
    
    
def playpgn(pgn):
    display.start()
    board = chess.Board()
    for move in pgn:
        board.push(move)
        display.update(board.fen())
        input()

games = []
wins = 0
losses = 0
for i in range(0,100):
    isWin, pgn, fen, game_min = playGame(0,1,True,False)
    if isWin:
        wins += 1
    elif not isWin:
        losses += 1
    games.append(pgn)
    ALLTIMEMAX.append(game_min)
 
    print(i)
plt.plot(ALLTIMEMAX, label=str(i))
plt.legend()
plt.show()


display.terminate()

    
