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
            ["bR","bN","bB","bQ","bK","bB","bK","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wK","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        pass