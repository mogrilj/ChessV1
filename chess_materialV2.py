import chess
from chessboard import display
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import chess.pgn

PIECES = ["p","n","b","r","q","k"]
VALUES = [1,3,3,5,9,100_000]

board = chess.Board()

ALLTIMEMAX = []
#1 = white -1 = black

def movesToList(legalMovesObject):
    moves = []
    for move in legalMovesObject:
        moves.append(move)
    return moves

class Material:
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





    def generateMoves(self,fen,isTurn,player):
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
                    localEvaluation.append(Material.evaluateFenString(board.fen(),player,isTurn))
                    board.pop()
            if len(secondDegreeMoves[legalMoves.index(lM)]) == 0:
                if board.is_checkmate():
                   localEvaluation.append(100_000)
                   return lM
                if board.is_stalemate():
                    localEvaluation.append(0)
                else:
                    localEvaluation.append(0)
            board.pop()
            if len(localEvaluation) > 0:
                globalEvaluation.append(min(localEvaluation))
            else:
                globalEvaluation.append(min(localEvaluation))
       
        #if there are multiple best moves, select one at random
        if globalEvaluation.count(max(globalEvaluation)) > 1:
            bestMoves = []
            for move in legalMoves:
                if globalEvaluation[legalMoves.index(move)] == max(globalEvaluation):
                    bestMoves.append(move)
            return bestMoves[random.randint(0,len(bestMoves)-1)]
        else:
            return legalMoves[globalEvaluation.index(max(globalEvaluation))]
    
class MaterialAndSquare:
    def evaluateFenString(fen,player,turn):
        penalty = 0
        #checking for mates and giving penaltys
        if chess.Board(fen).is_checkmate():
            if (player == 1 and turn == 1) or (player == -1 and turn == 0):
                penalty = 10_000
            if (player == 1 and turn == 0) or (player == -1 and turn == 1):
                penalty = -10_000
        #cleaning the fen 
        fen = fen.split(" ")[0]
       
        fenWithoutSpaces = ""
        for letter in fen.replace("/",""):
              if not letter.isdigit():
                    fenWithoutSpaces = fenWithoutSpaces + letter
        #summing all pieces together
        whiteSumm = 0
        blackSumm = 0
        for piece in fenWithoutSpaces:
            if piece.isupper():
                whiteSumm += VALUES[PIECES.index(piece.lower())]
            else:
                blackSumm += VALUES[PIECES.index(piece.lower())]
     
        #adding the controlled squares:
        b = chess.Board(fen)
        for x in range(8):
            for y in range(8):
                if b.is_attacked_by(chess.WHITE, chess.square(x,y)):
                    whiteSumm += 1
                if b.is_attacked_by(chess.BLACK, chess.square(x,y)):
                    blackSumm += 1
        
        # summe zwischen weiß und schwarz abhängig von player input
        return (whiteSumm*player + blackSumm*(-1*player)) + penalty

    def generateMoves(self,fen,isTurn,player):
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
                    localEvaluation.append(MaterialAndSquare.evaluateFenString(board.fen(),player,isTurn))
                    board.pop()
            if len(secondDegreeMoves[legalMoves.index(lM)]) == 0:
                if board.is_checkmate():
                   localEvaluation.append(100_000)
                   return lM
                if board.is_stalemate():
                    localEvaluation.append(0)
                else:
                    localEvaluation.append(0)
            board.pop()
            if len(localEvaluation) > 0:
                globalEvaluation.append(min(localEvaluation))
            else:
                globalEvaluation.append(min(localEvaluation))
        
        #if there are multiple best moves, select one at random
        if globalEvaluation.count(max(globalEvaluation)) > 1:
            bestMoves = []
            for move in legalMoves:
                if globalEvaluation[legalMoves.index(move)] == max(globalEvaluation):
                    bestMoves.append(move)
            return bestMoves[random.randint(0,len(bestMoves)-1)]
        else:
            return legalMoves[globalEvaluation.index(max(globalEvaluation))]

                        
class MaterialThenSquare:
    def evaluateFenString(fen,player,turn):
        penalty = 0
        #checking for mates and giving penaltys
        if chess.Board(fen).is_checkmate():
            if (player == 1 and turn == 1) or (player == -1 and turn == 0):
                penalty = 10_000
            if (player == 1 and turn == 0) or (player == -1 and turn == 1):
                penalty = -10_000
        #cleaning the fen 
        fen = fen.split(" ")[0]
       
        fenWithoutSpaces = ""
        for letter in fen.replace("/",""):
              if not letter.isdigit():
                    fenWithoutSpaces = fenWithoutSpaces + letter
        #summing all pieces together
        whiteSumm = 0
        blackSumm = 0
        for piece in fenWithoutSpaces:
            if piece.isupper():
                whiteSumm += VALUES[PIECES.index(piece.lower())]
            else:
                blackSumm += VALUES[PIECES.index(piece.lower())]
     
        #adding the controlled squares:
        b = chess.Board(fen)
        whiteSquares = 0
        blackSquare = 0
        for x in range(8):
            for y in range(8):
                if b.is_attacked_by(chess.WHITE, chess.square(x,y)):
                    whiteSquares += 1
                if b.is_attacked_by(chess.BLACK, chess.square(x,y)):
                    blackSquare += 1
        
        # summe zwischen weiß und schwarz abhängig von player input
        return (whiteSumm*player + blackSumm*(-1*player)) + penalty, (whiteSquares*player + blackSquare*(-1*player))
    
    
        
    def generateMoves(self,fen,isTurn,player):
        board = chess.Board(fen)
        legalMoves = movesToList(board.legal_moves)
        secondDegreeMoves = []
        #generating all answers to the legal moves
        for lM in legalMoves:
            board.push(lM)
            secondDegreeMoves.append(movesToList(board.legal_moves))
            board.pop()
        globalEvaluation = []
        globalSquareControll = []
        #looping through all possible outcomes and evaluating them
        for lM in legalMoves:
            board.push(lM)
            localEvaluation = []
            localSquareControll = []
            for m in secondDegreeMoves[legalMoves.index(lM)]:
                if board.is_checkmate():
                    localEvaluation.append(0)
                else:
                    board.push(m)
                    evaluation,squares = MaterialThenSquare.evaluateFenString(board.fen(),player,isTurn)
                    localEvaluation.append(evaluation)
                    localSquareControll.append(squares)
                    board.pop()
            if len(secondDegreeMoves[legalMoves.index(lM)]) == 0:
                if board.is_checkmate():
                   localEvaluation.append(100_000)
                   return lM
                if board.is_stalemate():
                    localEvaluation.append(0)
                else:
                    localEvaluation.append(0)
            board.pop()
            
            globalEvaluation.append(min(localEvaluation))
            if len(localSquareControll) > 0:
                globalSquareControll.append(min(localSquareControll))
            else:
                globalSquareControll.append(0)
               
        print(globalEvaluation,globalSquareControll,legalMoves)
        #if there are multiple best moves, select one at random
        if globalEvaluation.count(max(globalEvaluation)) > 1:
            maxes = []
            maxesSquares = []
            for lM in legalMoves:
                if globalEvaluation[legalMoves.index(lM)] == max(globalEvaluation):
                    maxes.append(lM)
                    maxesSquares.append(globalSquareControll[legalMoves.index(lM)])
            if len(maxes) > 1:
                moves = []
                for m in maxes:
                    if maxesSquares[maxes.index(m)] == max(maxesSquares):
                        moves.append(m)
                if len(moves) > 1:
                    return moves[random.randint(0,len(moves)-1)]
                else:
                    return moves[0]
                
            else:
                return maxes[0]
                        
                    
           
        else:
            return legalMoves[globalEvaluation.index(max(globalEvaluation))]  
                      

        
#player 1 = white player -1 = black    
def playGame(pauseTime,player,algorithms,showDisplay=False,playYourself=False):
    if showDisplay:
        display.start()
    board = chess.Board()
    pgn = []
    
    print("player is:"+str(player))
    while True:
        #generating moves based on the turn
        if board.turn ==  bool(player+1):
            move = algorithms[0].generateMoves(board.fen(),board.turn,player)
        else:
            if not playYourself:
                
                #move = movesToList(board.legal_moves)[random.randint(0,len(movesToList(board.legal_moves))-1)]
                move = algorithms[1].generateMoves(board.fen(), board.turn, -player)
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
                      print("loss")
                      return False,pgn,board.fen()
                      
            else:
                      print("win")
                      return True, pgn, board.fen()
                      
        if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_threefold_repetition() or board.is_seventyfive_moves() or board.can_claim_fifty_moves():
            print("No one")
            return None,pgn,board.fen()
            
    
    
def playpgn(pgn):
    display.start()
    board = chess.Board()
    for move in pgn:
        board.push(move)
        display.update(board.fen())
        input()

def createPGN(game):
    x = chess.pgn.Game()
    pgn = x

    for move in game:
        pgn = pgn.add_variation(move)
        
    return x
        
games = []
players = [-1,1]
wins = 0
losses = 0
for i in range(0,100):
    isWin, pgn, fen = playGame(0,players[random.randint(0,1)],[MaterialThenSquare(),MaterialAndSquare()],False,False)
    if not isWin == None:
        if isWin:
            wins += 1
        elif not isWin:
            losses += 1
    
    games.append(pgn)
 
    print(i)
plt.plot(ALLTIMEMAX, label=str(i))
plt.legend()
plt.show()


display.terminate()

    
