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
        ]
        self.whiteToMove = True
        self.moveLog = []
    
    '''
    Makes a move (cannot castle/en-passant/promote a pawn)
    '''
    def makeMove(self,move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # swap current player

    '''
    Undo the last move
    '''
    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured # places empty if there was no piece captured
            self.whiteToMove = not self.whiteToMove # switch back to the player's move
    
    '''
    All valid moves considering check
    '''
    def getValidMove(self):
        return self.getPossibleMoves()
        pass

    '''
    All valid moves without considering checks
    '''
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # use len(self.board) instead of simply 8
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'N':
                        self.getNightMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
    '''
    Get all pawn moves for the pawn located at [r][c] and add them to the list
    '''
    def getPawnMoves(r,c,moves):
        pass

    '''
    Get all rook moves for the rook located at [r][c] and add them to the list
    '''
    def getRookMoves(r,c,moves):
        pass 

    '''
    Get all bishop moves for the bishop located at [r][c] and add them to the list
    '''
    def getBishopMoves(r,c,moves):
        pass
    
    '''
    Get all night moves for the night located at [r][c] and add them to the list
    '''
    def getNightMoves(r,c,moves):
        pass

    '''
    Get all queen moves for the queen located at [r][c] and add them to the list
    '''
    def getQueenMoves(r,c,moves):
        pass

    '''
    Get all king moves for the king located at [r][c] and add them to the list
    '''
    def getKingMoves(r,c,moves):
        pass


class Move():
    # map keys (ranks/files) to values (rows/cols)

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()} # reverse the above dictionary
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self,start_square,end_square,board):

        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def getChessNotation(self):
        return self.getRankFile(self.start_row,self.start_col)+self.getRankFile(self.end_row,self.end_col)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
