# Create a board. It's empty at first.
# Determine player 1 and player 2
# min to winner =5
# Iterating through loop

    # create board
    # Players take turn
    # update board
    # Test if a player has won
    # Test if it's a draw
    # check if it's a valid move


# subproblem_1: Creating a board
# parameters:
# returns:
def createBoard(board):
    pass
# This function will mainly contain the "print" syntax to create the borad.
# The each box will have numbers from 0 which represents empty.


# subproblem_2: Players take turn
# parameters: who's first
# returns: player number
def firstturn(x=1):
    pass

# This function will then decide which player (Player1 or Player2) will go first
# Here, I created a parameter with a default value of 1 and the players will get an
# option to choose either 1 or 2 depending on who goes first
# If a player chooses 1, his/her icon will automatically become O and the other player
# will have X as his/her icon


# subproblem_3: Update a board
# parameters: Which location, whose turn, board
# returns: board, whose turn next
def boardupdate(number):
    pass

# This function will require a input of numbers for spot on the board.
# This function will also automatically print. If player 1 select a spot, it changes to X.
# And if player 2 select a spot, it changed to O
# It returns updated board and whose turn next.


# subproblem_4:
# parameters: board
# returns: winner

def checkwinner():
    pass

# This function will check for a winner after each move either by a player1 or
# player2. There are total of 8 possible cases to determin a winner.


# subproblem_5:
# parameters: board
# returns:draw
def checkdraw():
    pass

# This functino will check whether it is draw.
# It returns the resul of draw and ends game.
