import random
import chess
from chess import svg
import datetime

class Checkers:
    def __init__(self):
        self.size = 8
        self.turn = chess.BLACK
        self.board = chess.Board("1p1p1p1p/p1p1p1p1/1p1p1p1p/8/8/P1P1P1P1/1P1P1P1P/P1P1P1P1 b KQkq - 0 4")
    
    def isCellEmpty(self, i):
        return self.board.piece_at(i) is None
    
    def changeTurn(self, turn):
        if turn is chess.WHITE:
            return chess.BLACK
        else:
            return chess.WHITE
    
    def displayBoard(self):
        display(svg.board(board = self.board))
            
    def ifIsPositionWithinBoundary(self, x, y):
        return x>=0 and y>=0 and x<self.size and y<self.size
    
    def bottomRight(self, pos):
        x, y = pos//self.size-1, pos%self.size+1
        return x*self.size+y if self.ifIsPositionWithinBoundary(x,y) else None 
    
    def bottomLeft(self, pos):
        x, y = pos//self.size-1, pos%self.size-1
        return x*self.size+y if self.ifIsPositionWithinBoundary(x,y) else None 
    
    def topRight(self, pos):
        x, y = pos//self.size+1, pos%self.size+1
        return x*self.size+y if self.ifIsPositionWithinBoundary(x,y) else None 
        
    def topLeft(self, pos):
        x, y = pos//self.size+1, pos%self.size-1
        return x*self.size+y if self.ifIsPositionWithinBoundary(x,y) else None
    
    def pieceAtPosition(self,pos):
        return self.board.piece_at(pos)
        
    def validNeighbors(self,pos):
        tl = self.topLeft(pos)
        tr = self.topRight(pos)
        bl = self.bottomLeft(pos)
        br = self.bottomRight(pos)
        valid = []
        piece = self.pieceAtPosition(pos)
        if piece is None:
            raise Exception("Sorry, no piece present at position" + str(pos))
        
        if piece.piece_type == chess.PAWN and piece.color == chess.WHITE:
            if tl is not None:
                valid.append(tl)
            if tr is not None:
                valid.append(tr)
                
        elif piece.piece_type == chess.PAWN and piece.color == chess.BLACK:
            if bl is not None:
                valid.append(bl)
            if br is not None:
                valid.append(br)
                
        else:
            if tl is not None:
                valid.append(tl)
            if tr is not None:
                valid.append(tr)
            if bl is not None:
                valid.append(bl)
            if br is not None:
                valid.append(br)
                
        return valid
    
        
    def getOppColorPieces(self, neighbors, color):
        return [neighbor for neighbor in neighbors if self.pieceAtPosition(neighbor) is not None \
                               and self.pieceAtPosition(neighbor).color is not color]
    
    def validJumps(self, pos1, pos2):
        x1, y1 = pos1//self.size, pos1%self.size
        x2, y2 = pos2//self.size, pos2%self.size
        x, y = 2 *  x2 - x1, 2 * y2 - y1
        return x*self.size+y if self.ifIsPositionWithinBoundary(x,y) and self.isCellEmpty(x*self.size+y) else None
    
    def getFirstJumpsForPos(self, pos):
        jumps = []
        oppColorPositons = self.getOppColorPieces(self.validNeighbors(pos), self.board.piece_at(pos).color)
        for positions in oppColorPositons:
            if self.validJumps(pos,positions) is not None:
                jumps.append(self.validJumps(pos,positions))
        return jumps
    
    
    
    
    def getAllFirstJumps(self, turn):
        firstJumps = {}
        allPiecesPosition = [position for position in self.board.piece_map().keys() if self.board.piece_at(position).color == turn]
        for position in allPiecesPosition:
            firstJumpPos = self.getFirstJumpsForPos(position)
            if len(firstJumpPos) is not 0:
                firstJumps[position] = firstJumpPos
        return firstJumps
    

    def getCaptureMovesForPos(self, pos):
        paths = []
        
        testing = self.getFirstJumpsForPos(pos)

        for nextPos in testing:

          pieceRemoved, isConvertedToKing = self.makeMoveForRecursion(pos, nextPos)
          remainingPaths = self.getCaptureMovesForPos(nextPos)

          if not remainingPaths:
            paths.append([nextPos])

          else:
            for remainingPath in remainingPaths:
              paths.append([nextPos] + remainingPath)

          self.unMove(pos, nextPos, pieceRemoved, isConvertedToKing)
        
        return paths
    
    def makeMoveForRecursion(self, i, j):
        piece = self.board.remove_piece_at(i)
        self.board.set_piece_at(j, piece)
        isConverted = self.convertToKing(j)
        if self.isCaptureMove(i, j):
          return self.capturePiece(i, j), isConverted
        
        else:
          return None, isConverted


    def getAllCaptureMoves(self, turn):
      moves = {}
      allPiecesPosition = [position for position in self.board.piece_map().keys() if self.board.piece_at(position).color == turn]
      for position in allPiecesPosition:
          captureMoves = self.getCaptureMovesForPos(position)
          if captureMoves:
              moves[position] = captureMoves
      return moves
        


            
    def capturePiece(self, fromPos, toPos):
      x1, y1 = fromPos//self.size, fromPos%self.size
      x2, y2 = toPos//self.size, toPos%self.size

      # add checks for valid jump
      # add checks for piece in between

      x, y = (x1 + x2) // 2, (y1 + y2) // 2

      return self.board.remove_piece_at(x * self.size + y)  
                
    def unCapturePiece(self, fromPos, toPos, piece):
      x1, y1 = fromPos//self.size, fromPos%self.size
      x2, y2 = toPos//self.size, toPos%self.size

      # add checks for valid jump
      # add checks for piece in between

      x, y = (x1 + x2) // 2, (y1 + y2) // 2

      self.board.set_piece_at(x * self.size + y, piece)  


    
    def getRemainingMovesForPos(self, pos):
        return [positions for positions in self.validNeighbors(pos) if self.isCellEmpty(positions)]
    
    
    def getAllRemainingMoves(self, turn):
        moves = {}
        allPiecesPosition = [position for position in self.board.piece_map().keys() if self.board.piece_at(position).color == turn]
        for position in allPiecesPosition:
            moveForPos = self.getRemainingMovesForPos(position)
            if len(moveForPos) is not 0:
                moves[position] = moveForPos
        return moves
    
    def isValidMove(self, i, j):
        if self.isCellEmpty(i) or self.board.piece_at(i).color is not self.turn:
            return False
        
        moves = self.getAllFirstJumps(self.turn)
        
        if not moves:
            moves = self.getAllRemainingMoves(self.turn)
            
        return i in moves and j in moves[i]
            
    def isCaptureMove(self, i, j):
      return abs((j % self.size) - (i % self.size)) == 2
    
    def convertToKing(self, i):
        if self.board.piece_at(i).piece_type == chess.KING:
            return False
        
        if self.board.piece_at(i).color is chess.WHITE and i in range(56,64):
            self.board.set_piece_at(i, chess.Piece(chess.KING, chess.WHITE))
            return True
        if self.board.piece_at(i).color is chess.BLACK and i in range(0,8):
            self.board.set_piece_at(i, chess.Piece(chess.KING, chess.BLACK))
            return True
        
        return False
        
            
    
    def makeMove(self, i, j):
        if self.isValidMove(i, j):
            piece = self.board.remove_piece_at(i)
            self.board.set_piece_at(j, piece)
            isConverted = self.convertToKing(j)
        else:
            return None, None
            
        if self.isCaptureMove(i, j):
          return self.capturePiece(i, j), isConverted
        
        else:
          return None, isConverted
    
    def isGameComplete(self):
        if not self.getAllCaptureMoves(chess.WHITE) and not self.getAllRemainingMoves(chess.WHITE):
            return 1 
        elif not self.getAllCaptureMoves(chess.BLACK) and not self.getAllRemainingMoves(chess.BLACK):
            return 0 
        return -1


    def getAllMoves(self, turn):
        if self.getAllCaptureMoves(turn):
            return self.getAllCaptureMoves(turn)
        else:
            return self.getAllRemainingMoves(turn)
    
    def unMove(self, i, j, pieceToPlace, isConvertedToKing):
      piece = self.board.remove_piece_at(j)
      if isConvertedToKing:
        piece.piece_type = chess.PAWN
        
      self.board.set_piece_at(i, piece)

      if pieceToPlace is not None:
        self.unCapturePiece(i, j, pieceToPlace)  
        
    def makeAllCaptureMoves(self, i, options):
        stack = []
        for j in options:
            piece, isKing = self.makeMoveForRecursion(i,j)
            stack.append((piece, isKing))
            i = j
        return stack
    
    def reverseAllCaptureMoves(self, i, options, stack):
        optionsCopy = options.copy()
        j = optionsCopy.pop()
        optionsCopy.insert(0,i)
        for i in reversed(optionsCopy):
            piece, isKing = stack.pop()
            self.unMove(i, j, piece, isKing)
            j = i


    def heuristics(self):
        king = 1.2
        bk = 0
        bp = 0
        wk = 0
        wp = 0
        pieces = [self.board.piece_at(p) for p in self.board.piece_map().keys()]
        for piece in pieces:
            if piece.color is chess.WHITE:
                if piece.piece_type is chess.PAWN:
                    wp+=1
                else:
                    wk+=1
            else:
                if piece.piece_type is chess.PAWN:
                    bp+=1
                else:
                    bk+=1
        return wp + king*wk - bp - king*bk


    def heuristics2(self):
        king = 1.2
        bk = 0
        bp = 0
        wk = 0
        wp = 0
        pieces = [self.board.piece_at(p) for p in self.board.piece_map().keys()]
        for piece in pieces:
            if piece.color is self.turn:
                if piece.piece_type is chess.PAWN:
                    wp+=1
                else:
                    wk+=1
            else:
                if piece.piece_type is chess.PAWN:
                    bp+=1
                else:
                    bk+=1
        return wp + king*wk - bp - king*bk
        
        
    def minMax(self, depth, isMaxPlayer, alpha, beta):
        if isMaxPlayer:
            turn = chess.WHITE
        else:
            turn = chess.BLACK
        
        if depth>3:
            return {'position' : None, 'prize' : self.heuristics()}
            
        finalState = self.isGameComplete()
        if finalState in [0,1]:
            if finalState == 0:
                return {'position' : None, 'prize' : 100-depth}
            else:
                return {'position' : None, 'prize' : -100+depth}
    
        if isMaxPlayer:
            best = -50
        else:
            best = 50
    
        moves = self.getAllMoves(turn)
        for move in moves.keys():
            for options in moves[move]:
                if isinstance(options,list):
                    stack = self.makeAllCaptureMoves(move, options)
                        
                    recur = self.minMax(depth+1,not isMaxPlayer, alpha, beta)
                    
                    self.reverseAllCaptureMoves(move, options, stack)
                    
                    if isMaxPlayer:
                        if recur['prize'] > best:
                            best = recur['prize']
                            nextMove = (move,options)
                            alpha = max(alpha,best)
                            if alpha>=beta:
                                break

                    else:
                        if recur['prize'] < best:
                            best = recur['prize']
                            nextMove = (move,options)
                            beta = min(beta,best)
                            if alpha>=beta:
                                break
                        
                else:
                    piece, isKing = self.makeMoveForRecursion(move,options)
                    recur = self.minMax(depth+1,not isMaxPlayer, alpha, beta)
                    self.unMove(move, options, piece, isKing)

                    if isMaxPlayer:
                        if recur['prize'] > best:
                            best = recur['prize']
                            nextMove = (move,[options])
                            alpha = max(alpha,best)
                            if alpha>=beta:
                                break

                    else:
                        if recur['prize'] < best:
                            best = recur['prize']
                            nextMove = (move,[options])
                            beta = min(beta,best)
                            if alpha>=beta:
                                break
        
        return {'position': nextMove, 'prize': best}


    def minMax2(self, depth, isMaxPlayer, alpha, beta):
        if isMaxPlayer:
            turn = self.turn
        else:
            turn = self.changeTurn(self.turn)

        if depth>3:
            return {'position' : None, 'prize' : self.heuristics2()}

        finalState = self.isGameComplete()

        if finalState in [0,1]:
            if self.turn is chess.WHITE:
                if finalState == 0:
                    return {'position' : None, 'prize' : 100-depth}
                else:
                    return {'position' : None, 'prize' : -100+depth}
            else:
                if finalState == 1:
                    return {'position' : None, 'prize' : 100-depth}
                else:
                    return {'position' : None, 'prize' : -100+depth}

        if isMaxPlayer:
            best = -100
        else:
            best = 100

        moves = self.getAllMoves(turn)
        move_keys_list = list(moves.keys())
        random.shuffle(move_keys_list)
        for move in move_keys_list:
            for options in moves[move]:
                if isinstance(options,list):
                    stack = self.makeAllCaptureMoves(move, options)

                    recur = self.minMax2(depth+1,not isMaxPlayer, alpha, beta)

                    self.reverseAllCaptureMoves(move, options, stack)

                    if isMaxPlayer:
                        if recur['prize'] > best:
                            best = recur['prize']
                            nextMove = (move,options)
                            alpha = max(alpha,best)
                            if alpha>=beta:
                                break

                    else:
                        if recur['prize'] < best:
                            best = recur['prize']
                            nextMove = (move,options)
                            beta = min(beta,best)
                            if alpha>=beta:
                                break

                else:
                    piece, isKing = self.makeMoveForRecursion(move,options)
                    recur = self.minMax2(depth+1,not isMaxPlayer, alpha, beta)
                    self.unMove(move, options, piece, isKing)

                    if isMaxPlayer:
                        if recur['prize'] > best:
                            best = recur['prize']
                            nextMove = (move,[options])
                            alpha = max(alpha,best)
                            if alpha>=beta:
                                break

                    else:
                        if recur['prize'] < best:
                            best = recur['prize']
                            nextMove = (move,[options])
                            beta = min(beta,best)
                            if alpha>=beta:
                                break

        return {'position': nextMove, 'prize': best}


    def attempt_player_move(self, from_square, to_square):
        if not self.isValidMove(from_square, to_square):
            return

        piece_captured, is_converted = self.makeMove(from_square, to_square)

        if not piece_captured or not self.getCaptureMovesForPos(to_square):
            self.turn = self.changeTurn(self.turn)


    def attempt_bot_move(self):
        if self.turn is chess.WHITE:
            self.make_bot_move()

    def make_bot_move(self):
        print("Thinking.. please wait :( .. I'm not so graphically advanced")
        d = self.minMax(0, True, -2000, 2000)
        i,move = d['position']
        # print(i, move)
        for j in move:
          self.makeMoveForRecursion(i,j)
          i = j

        self.turn = self.changeTurn(self.turn)

        print("Thanks for waiting. Please make your move")


    def move_or_ignore(self, from_square, to_square):
        if self.turn is chess.BLACK:
            self.attempt_player_move(from_square, to_square)

    def turn_as_string(self):
        return "White" if self.turn is chess.WHITE else "Black"


    def make_bot_move_any_color(self):
        print(self.turn_as_string(), " thinking. ")
        t0 = datetime.datetime.now()

        d = self.minMax2(0, True, -2000, 2000)
        i,move = d['position']
        # print(i, move)
        for j in move:
          self.makeMoveForRecursion(i,j)
          i = j

        self.turn = self.changeTurn(self.turn)

        delta = datetime.datetime.now() - t0
        print("Made move in ", delta.total_seconds(), " seconds")


    def play(self,youFirst = True):
        print("\t Checkers \n Bot = Black \n You = White ")
        while True:
          res = self.isGameComplete()
          if res in [0,1]:
            if res == 0:
              print("WHITE Wins")
              self.displayBoard()
            elif res == 1:
              print("BLACK Wins")
              self.displayBoard()
            break
          if self.turn == chess.WHITE:
            print("White's Turn") 
          else:
            print("Black's Turn")
          self.displayBoard()
          
          if self.turn == chess.BLACK:
            i = int(input("Enter Start Location"))-1
            j = int(input("Enter End Location"))-1
          
            if not self.isValidMove(i,j):
              print("Invalid Input! Please enter another number ")
              continue
            
            piece, _ = self.makeMove(i,j)
          
            if piece is not None:
              leftMoves = self.getCaptureMovesForPos(j)
              if leftMoves:
                print("Continue to Capture")
                continue
            
          
          else:
            print("Bots Turn")
            d = self.minMax(0,True, -2000, 2000)
            i,move = d['position']
            print(i,move)
            for j in move:
              self.makeMoveForRecursion(i,j)
              i = j
        
          self.turn = self.changeTurn(self.turn)    
#           clear_output(True)
          

#     def minimax()
        