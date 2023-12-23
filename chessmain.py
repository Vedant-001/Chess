""" To display the current game state and the user input
"""

import pygame as p
import chessEngine

width = height = 512
dimension = 8 # Chess board is of 8x8 dimension
square_size = width//dimension
max_fps = 15

images = {}

'''
Initialize a global dictionary of images.
Will be called only once in the main - to reduce time
'''

def load_images():
    pieces = ["bB","bK","bN","bP","bQ","bR",
              "wB","wK","wN","wP","wQ","wR"]
    
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("C:/Users/HP/Desktop/Coding/Game/Chess/images/"+piece+".png"),(square_size,square_size))
    # images["bB"] can be used to access black Bishop and similar with other pieces

"""
Driver Code
"""

def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gamestate = chessEngine.GameState()
    valid_moves = gamestate.getValidMove()
    move_made = False # flag variable for when a move is valid
    load_images()

    running = True
    selected_square = () #to keep track of the last click by the user
    player_clicks = [] #to keep track of the player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x,y location of mouse
                row = location[1]//square_size
                col = location[0]//square_size

                # if player clicks the same square twice -> undo
                if selected_square == (row,col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row,col)
                    player_clicks.append(selected_square) # append for both 1st and 2nd clicks

                # if the player has clicked for the second time on a valid square,
                # which is not necessarily a legal move -> still move the piece
                if len(player_clicks) == 2:
                    move = chessEngine.Move(player_clicks[0],player_clicks[1],gamestate.board)
                    print(move.getChessNotation())
                    if move in valid_moves:
                        gamestate.makeMove(move)
                        move_made = True
                    selected_square = ()
                    player_clicks = [] # reset the clicks
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gamestate.undoMove()
                    move_made = True # considering undo as a valid move 
    # generate valid moves only when a valid move is made
        if move_made:
            valid_moves = gamestate.getValidMove()
            move_made = False

        drawGameState(screen,gamestate)
        clock.tick(max_fps)
        p.display.flip()

'''
The below function is responsible for the graphics of the current gamestate
'''
def drawGameState(screen,gamestate):
    draw_board(screen) #draws the squares
    draw_pieces(screen,gamestate.board) #draws pieces on the squares
    '''Note: we draw the squares before drawing the pieces'''

def draw_board(screen):
    colors = [p.Color('white'),p.Color('dark gray')]

    for row in range(dimension):
        for col in range(dimension):
            square_color = colors[(row+col)%2]
            p.draw.rect(screen,square_color,p.Rect(col*square_size,row*square_size,square_size,square_size))
                

def draw_pieces(screen,board):

    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != "--":
                screen.blit(images[piece], p.Rect(col*square_size,row*square_size,square_size,square_size))

# If this file is imported in another program, then it wouldn't implicitly run
if __name__ == "__main__":
    main()