"""
Responsible for storing all the info about the current state of the chess game
Like:
Determining the valid moves.
Keep a log of moves allowing undo of moves.
"""

class GameState():
    
    def __init__(self) -> None:
        # The board is an 8x8 2d list with each element having 2 characters
        # First character represents the color of the piece - b for Black and w for White
        # Second character represents the piece - R for rook, N for Knight, B for Bishop and K for King
        # Blank/empty spaces are denoted by '--'
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ] #Note: a two pawns have been added for testing
        self.moveFunctions = {'P':self.getPawnMoves,'B':self.getBishopMoves,'K':self.getKingMoves,
                              'N':self.getNightMoves,'Q':self.getQueenMoves,'R':self.getRookMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = () # coords for the square where en-passant capture lands the pawn
        # handle castling rights
        self.currentCastlingRights = CastlingRights(True,True,True,True)
        # to keep track of castling rights considering undo of moves
        self.castleRightLog = [self.currentCastlingRights]
        self.castleRightLog = [CastlingRights(self.currentCastlingRights.wks,self.currentCastlingRights.wqs,
                                              self.currentCastlingRights.bks,self.currentCastlingRights.bqs)]

    
    '''
    Makes a move (cannot castle/en-passant/promote a pawn)
    '''
    def makeMove(self,move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # swap current player
        # update the kings' positions when needed
        if(move.piece_moved == "wK"):
            self.whiteKingLocation = (move.end_row,move.end_col)
        elif(move.piece_moved == "bK"):
            self.blackKingLocation = (move.end_row,move.end_col)
        
        # promote to a Queen
        if move.isPawnPromotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0]+'Q'
        
        # en-passant
        if move.isEnPassantMove:
            self.board[move.start_row][move.end_col] = '--'
        
        # update enPassantPossible
        if (move.piece_moved[1] == "P" and abs(move.start_row-move.end_row) == 2):
            self.enPassantPossible = ((move.start_row+move.end_row)//2,move.end_col)
        else:
            self.enPassantPossible = () #reset is the pawn move did not lead to en-passant

        # castle
            if move.isCastleMove:
                if move.end_col-move.start_col == 2: # kingside castle
                    self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] # move the rook
                    self.board[move.end_row][move.end_col+1] = '--' #remove the rook
                else: #queenside castle
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2] # move the rook
                    self.board[move.end_row][move.end_col-2] = '--'

        # update castling rights (only when a rook or a king has moved)
        self.updateCastlingRights(move)
        self.castleRightLog.append(CastlingRights(self.currentCastlingRights.wks,self.currentCastlingRights.wqs,
                                              self.currentCastlingRights.bks,self.currentCastlingRights.bqs))

    '''
    Undo the last move
    '''
    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured # places empty if there was no piece captured
            self.whiteToMove = not self.whiteToMove # switch back to the player's move
            # update the kings' positions when needed
            if(move.piece_moved == "wK"):
                self.whiteKingLocation = (move.start_row,move.start_col)
            elif(move.piece_moved == "bK"):
                self.blackKingLocation = (move.start_row,move.start_col)
            
            # undo en-passant
            if move.isEnPassantMove:
                self.board[move.end_row][move.end_col] = '--' # reset the landing square after en-passant
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enPassantPossible = (move.end_row,move.end_col)
                # if we don't reset this, we won't be able to repeat en-passant after an undo
            if move.piece_moved[1] == 'P' and abs(move.start_row-move.end_row) == 2:
                self.enPassantPossible = ()
            
            # undo castling rights
            self.castleRightLog.pop() # pop the latest castle rights from the undone move
            self.currentCastlingRights = self.castleRightLog[-1] # update castle rights to what they were 
            # undo castle move
            if move.isCastleMove:
                if move.end_col-move.start_col == 2: #kingside
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else: #queenside
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'

    def updateCastlingRights(self,move):
        if move.piece_moved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.piece_moved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0: # white's queen side rook
                    self.currentCastlingRights.wqs = False
                elif move.start_col == 7: # white's king side rook
                    self.currentCastlingRights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0: # black's queen side rook
                    self.currentCastlingRights.bqs = False
                elif move.start_col == 7: # black's king side rook
                    self.currentCastlingRights.bks = False
    
    '''
    All valid moves considering check
    '''
    def getValidMove(self):
        print(self.currentCastlingRights.wks,self.currentCastlingRights.wqs,self.currentCastlingRights.bks,self.currentCastlingRights.bqs)
        tempEnPassantPossible = self.enPassantPossible # copy of square where enpassant is possible
        tempCastleRights = CastlingRights(self.currentCastlingRights.wks,self.currentCastlingRights.wqs,
                                          self.currentCastlingRights.bks,self.currentCastlingRights.bqs)
        #1. generate all possible moves
        moves = self.getPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)
        #2. for each move -> make the move
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            #3. generate opponent's possible moves
            opponentMoves = self.getPossibleMoves()
            #4. for all of opponent's possible moves -> see if the king is being attacked
            self.whiteToMove = not self.whiteToMove
            if self.isInCheck():
                moves.remove(moves[i]) #5. Not a valid move if king is under attack
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.isInCheck():
                self.checkMate = True
                print("CHECKMATE")
                print("BLACK" if self.whiteToMove else "WHITE","WON!")
                quit()
            else:
                print("STALEMATE!")
                self.staleMate = True
        # if we make a move leading to either of the mates -> the values will become true
        # but if we undo after a checkmate/stalemate, we need to reset the values to False
        else:
            self.checkMate = False
            self.staleMate = False

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves

    '''
    Determine if the current player is in check
    '''
    def isInCheck(self):
        if self.whiteToMove:
            return self.isUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.isUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    '''
    Determine if the opponenet can attack the square r,c 
    (probably containing current player's king)
    '''
    
    def isUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's perspective
        opponentMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch back to current player

        for move in opponentMoves:
            if move.end_row == r and move.end_col == c:
                return True
        return False


        
    '''
    All valid moves without considering checks
    '''
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # use len(self.board) instead of simply 8
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves 
    
    '''
    Get all pawn moves for the pawn located at [r][c] and add them to the list
    '''
    def getPawnMoves(self,r,c,moves):
        # white Pawn moves
        if self.whiteToMove: #white's turn 
            if self.board[r-1][c] == '--': # move one place
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == '--': # move two places
                    moves.append(Move((r,c),(r-2,c),self.board))

            # captures
            if c-1 >= 0: #edge case - cannot capture beyond the extreme
                if self.board[r-1][c-1][0] == 'b': #capture to the left
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnPassantMove= True))
            if c+1 <= 7: #capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEnPassantMove= True))

        # black Pawn moves
        else:
            if self.board[r+1][c] == '--': # move one place
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == '--': # move two places
                    moves.append(Move((r,c),(r+2,c),self.board))
            # captures
            if c-1 >= 0: #edge case - cannot capture beyond the extreme
                if self.board[r+1][c-1][0] == 'w': #capture to the left
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEnPassantMove= True))
            if c+1 <= 7: #capture to the right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEnPassantMove= True))
    '''
    Get all rook moves for the rook located at [r][c] and add them to the list
    '''
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(0,1),(1,0))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r,c,moves),(endRow,endCol,moves),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c,moves),(endRow,endCol,moves),self.board))
                        break
                    else:
                        break
                else:
                    break


    '''
    Get all bishop moves for the bishop located at [r][c] and add them to the list
    '''
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break


    
    '''
    Get all night moves for the night located at [r][c] and add them to the list
    '''
    def getNightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        playerColor = "w" if self.whiteToMove else "b"

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != playerColor:
                    moves.append(Move((r,c,moves),(endRow,endCol,moves),self.board))

    '''
    Get all queen moves for the queen located at [r][c] and add them to the list
    '''
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    '''
    Get all king moves for the king located at [r][c] and add them to the list
    '''
    def getKingMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,0),(-1,1),
                      (0,-1),(0,1),
                      (1,-1),(1,0),(1,1))
        playerColor = "w" if self.whiteToMove else "b"
        for i in range(1,8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != playerColor:
                    moves.append(Move((r,c,moves),(endRow,endCol,moves),self.board))

    '''
    Generate all valid castling moves for the king
    '''
    def getCastleMoves(self,r,c,moves):
        if self.isUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r,c,moves)
    
    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.isUnderAttack(r,c+1) and not self.isUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove = True))


    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.isUnderAttack(r,c-1) and not self.isUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove = True))

class CastlingRights():
    def __init__(self,wks,wqs,bks,bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    # map keys (ranks/files) to values (rows/cols)

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()} # reverse the above dictionary
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self,start_square,end_square,board, isEnPassantMove = False, isCastleMove = False):

        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        # check if the move leads to pawn promotion
        self.isPawnPromotion = ((self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7))

        # check for en passant move
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        # check for castle move
        self.isCastleMove = isCastleMove

        self.moveId = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col

    """
    Override the equals method
    """
    def __eq__(self,other):
        if isinstance(other,Move): # isinstance is a function
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.start_row,self.start_col)+self.getRankFile(self.end_row,self.end_col)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
