from random import *
from argparse import ArgumentParser

spacesLeft = 64
printEachWin = True
board = [[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]]

# reset the board for consecutive games
def resetBoard():
    global board, spacesLeft
    board = [[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], \
         [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]]
    spacesLeft = 64

# A simple print function for the board
def printBoard():
    for i in range(0, 4):
        print("\nLayer " + str(i+1) + ":")
        for j in range(0, 4):
            print(board[i][j])

# Check for any winning rows
def checkRows(symbol):
    for layer in board:
        for row in layer:
            if all(s == symbol for s in row):
                if printEachWin:
                    print(symbol + "s win with a row!")
                return True
    return False

# Check for any winning columns
def checkColumns(symbol):
    for layer in board:
        for col in range(0, 4):
            if all(row[col] == symbol for row in layer):
                if printEachWin:
                    print(symbol + "s win with a column!")
                return True
    return False

# Check for any winning aisles
def checkAisles(symbol):
    for i in range(0, 4):
        for j in range(0, 4):
            if all(board[k][i][j] == symbol for k in range(0, 4)):
                if printEachWin:
                    print(symbol + "s win with an aisle!")
                return True
    return False

# Check for any winning diagonals 
def checkDiagonals(symbol):
    for i in range(0, 4):
        if all(board[i][j][j] == symbol for j in range(0, 4)) or all(board[i][j][3-j] == symbol for j in range(0, 4)):
            if printEachWin:
                print(symbol + "s win with a diagonal across a layer!")
            return True
    
        if all(board[j][i][j] == symbol for j in range(0, 4)) or all(board[j][i][3-j] == symbol for j in range(0, 4)):
            if printEachWin:
                print(symbol + "s win with a diagonal along a row!")
            return True
        
        if all(board[j][j][i] == symbol for j in range(0, 4)) or all(board[j][3-j][i] == symbol for j in range(0, 4)):
            if printEachWin:
                print(symbol + "s win with a diagonal along a column!")
            return True
    
    if all(board[i][i][i] == symbol for i in range(0, 4)) or all(board[3-i][i][i] == symbol for i in range(0, 4)) or \
       all(board[i][3-i][i] == symbol for i in range(0, 4)) or all(board[3-i][3-i][i] == symbol for i in range(0, 4)):
        if printEachWin:
            print(symbol + "s win with a corner to corner diagonal!")
        return True

    return False
               
# Checks the entire board to see if a player has won
def checkForWin(symbol):
    if checkRows(symbol) or checkColumns(symbol) or checkAisles(symbol) or checkDiagonals(symbol):
        return True
    else:
        return False

# returns a heuristic score for a position based on a set of 4 positions on the board
def evaluate(lst, symbol, method):
    # Method 1 puts more priority on blocking the opponent, method 2 prioritizes connecting 4
    (ownCount, opponentCount) = (0, 0)
    for s in lst:
        if s == symbol:
            ownCount += 1
        elif s != " ":
            opponentCount += 1

    if ownCount == 3 and opponentCount == 0:
        # VERY IMPORTANT to play here becasue we will win
        score = 100000
        #print("I have 3")
    elif opponentCount == 3 and ownCount == 0:
        # IMPORTANT to play here because opponent can win next turn
        score = 1000
        #print("Opponent has 3")
    elif ownCount == 0:
        # if we have not played in this set yet, the score is determined by how many times the opponent has
        if method == 1:
            score = 1 + opponentCount * 10
        elif method == 2:
            score = 1 + opponentCount
    elif opponentCount == 0:
        # if the opponent has not played in this set, the score is based on how many times we have
        if method == 1:
            score = 1 + ownCount
        elif method == 2:
            score = 1 + ownCount * 10
    else:
        # both sides have played here, so nobody can win this set
        score = 0
    return score

def evaluateAll(i, j, k, symbol, method):
    score = 0
    col = []
    aisle = []
    
    for x in range(0, 4):
        col.append(board[i][x][k])
        aisle.append(board[x][j][k])

    # Row
    score += evaluate(board[i][j], symbol, method)
    
    # Column
    score += evaluate(col, symbol, method)
    
    # Aisle
    score += evaluate(aisle, symbol, method)

    # Diagonals
    # Diagonal across a layer
    if j == k:
        diag = []
        for x in range(0, 4):
            diag.append(board[i][x][x])
        score += evaluate(diag, symbol, method)
        
    elif j == 3-k:
        diag = []
        for x in range(0, 4):
            diag.append(board[i][x][3-x])
        score += evaluate(diag, symbol, method)

    # Diagonal along a row
    if i == k:
        diag = []
        for x in range(0, 4):
            diag.append(board[x][j][x])
        score += evaluate(diag, symbol, method)

    elif i == 3-k:
        diag = []
        for x in range(0, 4):
            diag.append(board[x][j][3-x])
        score += evaluate(diag, symbol, method)

    # Diagonal along a column and corner-to-corner
    if i == j:
        diag = []
        for x in range(0, 4):
            diag.append(board[x][x][k])
        score += evaluate(diag, symbol, method)
        if i == k:
            diag = []
            for x in range(0, 4):
                diag.append(board[x][x][x])
            score += evaluate(diag, symbol, method)
        if i == 3-k:
            diag = []
            for x in range(0, 4):
                diag.append(board[x][x][3-x])
            score += evaluate(diag, symbol, method)

    elif i == 3-j:
        diag = []
        for x in range(0, 4):
            diag.append(board[x][3-x][k])
        score += evaluate(diag, symbol, method)
        if i == k:
            diag = []
            for x in range(0, 4):
                diag.append(board[x][3-x][x])
            score += evaluate(diag, symbol, method)
        if i == 3-k:
            diag = []
            for x in range(0, 4):
                diag.append(board[x][3-x][3-x])
            score += evaluate(diag, symbol, method)

    return score

# Writes an X or an O in the game board at a specified location
def move(i, j, k, symbol):
    global board, spacesLeft
    if any(a < 0 for a in [i, j, k]):
        raise IndexError
    if board[i][j][k] != " ":
        raise Exception
    board[i][j][k] = symbol
    spacesLeft -= 1

# Reads the actual input from a human player
def readMove():
    i = int(input("Enter Layer: "))
    j = int(input("Enter Row: "))
    k = int(input("Enter Column: "))
    return (i-1, j-1, k-1)

# For a human player
def humanMove(symbol):
    global spacesLeft
    (i, j, k) = readMove()
    try:
        move(i, j, k, symbol)
    except IndexError:
        print("Invalid Move: That spot is not within the play space. Please try again.")
        humanMove(symbol)
    except:
        print("Invalid Move: That spot is already taken. Please try again.")
        humanMove(symbol)

# An algorithm that plays randomly
def randoMove(symbol):
    global spacesLeft
    spot = randint(0, spacesLeft-1)
    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 4):
                if board[i][j][k] == " ":
                    spot -= 1
                    if spot == -1:
                        move(i, j, k, symbol)
                        return

# An algorithm that plays based on a heuristic
def heuristicMove(symbol, method):
    # Go through the game board and assign a score to every empty space
    scores = {}
    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 4):
                if board[i][j][k] == " ":
                    score = evaluateAll(i, j, k, symbol, method)
                    # put the score in a dictionary with the position as the key
                    scores[(i, j, k)] = score

    # Now find the position with the highest score
    best = -1
    for position in scores:
        if scores[position] == best:
            if randint(0, 2) == 2: # Add some randomness to the algorithm
                (x, y, z) = position
                best = scores[position]
        elif scores[position] > best:
            (x, y, z) = position
            best = scores[position]

    # This position is our next move
    move(x, y, z, symbol)

def defenderMove(symbol):
    heuristicMove(symbol, 1)

def attackerMove(symbol):
    heuristicMove(symbol, 2)

def play(mode):
    if mode == 0:
        return humanMove
    elif mode == 1:
        return randoMove
    elif mode == 2:
        return defenderMove
    elif mode == 3:
        return attackerMove
    else:
        raise Exception

# Play a single game, prints the board a lot
def playGame(mode1, mode2):
    player1 = play(mode1)
    player2 = play(mode2)
    turn = 1
    while(1):
        print("Turn: " + str(turn))
        if spacesLeft == 0:
            print("Tie Game")
            break
        print("Player 1: ")
        player1("X")
        printBoard()
        if checkForWin("X"):
            break
        print("Player 2: ")
        player2("O")
        printBoard()
        if checkForWin("O"):
            break
        turn += 1

# Used for running a bunch of consecutive games, less printing
def testPlay(iterations, mode1, mode2):  

    global printEachWin
    printEachWin = False
    p1 = play(mode1)
    p2 = play(mode2)
    p1Wins = 0
    p2Wins = 0
    ties = 0
    turns = 0
    
    for i in range(0, iterations):
        resetBoard()
        while(1):
            turns += 1
            if spacesLeft == 0:
                ties += 1
                break
            p1("X")
            if checkForWin("X"):
                p1Wins += 1
                break
            p2("O")
            if checkForWin("O"):
                p2Wins += 1
                break
    
    print("Average turn count: " + str(turns/iterations))
    print("Player 1 wins: " + str(p1Wins))
    print("Player 2 wins: " + str(p2Wins))
    print("Ties: " + str(ties))

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('player1', type = int, help = 'specify how player 1 will play. 0:human, 1:random, 2:defensive, 3:offensive')
    parser.add_argument('player2', type = int, help = 'specify how player 2 will play. 0:human, 1:random, 2:defensive, 3:offensive')
    parser.add_argument('tests', type = int, nargs = '?', help = 'optionally specify an amount of test iterations')
    args = parser.parse_args()
    return (args.player1, args.player2, args.tests)

if __name__ == '__main__':
    (p1, p2, iterations) = parse_args()
    if iterations is None:
        playGame(p1, p2)
    else:
        testPlay(iterations, p1, p2)
