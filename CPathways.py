import copy
import math
global Nsize,humanTurn, board, winner,bestX,bestY,worstX,worstY, depth, isPlaying, amMachine
humanTurn = False


def GenerateComputerPlayerMove():
    global board, depth
    g = copy.deepcopy(board)
    v = minMax('M', g, -math.inf, math.inf, depth)
    board[bestY][bestX] = 'M'
    print("My Move is X:", bestX, "Y:", bestY)
    printBoard()
    return

def minMax(player, copyBoard, alpha, beta,depth):
    global Nsize, bestX, bestY
    if depth == 0:
        if player == 'M':
            return staticEval('H',copyBoard)
        elif player == 'H':
            return staticEval('M', copyBoard)
    if player == 'M':
        maxEval = -math.inf
        for row in range(Nsize):
            for column in range(Nsize):
                if copyBoard[row][column] == ' ':
                    copyB = copy.deepcopy(copyBoard)
                    copyB[row][column] = player
                    eval = minMax('H',copyB, alpha, beta, depth-1)
                    maxEval = max(maxEval,eval)
                    if alpha < eval:
                        alpha = eval
                        bestX = column
                        bestY = row

                    if beta <= alpha:
                        break
        return maxEval

    elif player == 'H':
        minEval = math.inf
        for row in range(Nsize):
            for column in range(Nsize):
                if copyBoard[row][column] == ' ':
                    copyC = copy.deepcopy(copyBoard)
                    copyC[row][column] = player
                    eval = minMax('H',copyC, alpha, beta, depth-1)
                    minEval = min(eval, minEval)
                    #if minEval > eval:
                    #    minEval = eval
                    #beta = min(eval, alpha)
                    if beta > eval:
                        beta = eval
                        worstX = column
                        worstY = row

                    if beta <= alpha:
                        break
        return minEval


def staticEval(player, copyBoard):
    global Nsize
    bestR = 0
    if player == 'M':
        opponent = 'H'
    elif player == 'H':
        opponent ='M'
    if columnCheck(opponent):
        for y in range(Nsize):
            if copyBoard[y][1] == opponent:
                tempR = pathRater(1,y,opponent,copyBoard)
                if bestR < tempR:
                    bestR = tempR
    else:
        for y in range(Nsize):
            if copyBoard[y][0] == player:
                tempR = pathRater(0,y,player,copyBoard)
                if bestR < tempR:
                    bestR = tempR
    return bestR


def pathRater(x, y, player,copyBoard):
    global Nsize
    rate = 0
    mult = 0
    endFound = False
    while not endFound:
        if x + 1 < Nsize and copyBoard[y][x+1] == player:
            copyBoard[y][x] = '-'
            x += 1
            mult = 1
            if y+1 < Nsize and (copyBoard[y+1][x] == player or copyBoard[y+1][x] == ' '):
                mult +=1
            if y-1 > -1 and (copyBoard[y-1][x] == player or copyBoard[y-1][x] == ' '):
                mult +=1
            if x+1 < Nsize and (copyBoard[y][x+1] == player or copyBoard[y][x+1] == ' '):
                mult += 2
            rate += 5*x
        elif y+1 < Nsize and copyBoard[y+1][x] == player:
            copyBoard[y][x] = '-'
            y += 1
            mult = 1
            if y+1 < Nsize and (copyBoard[y+1][x] == player or copyBoard[y+1][x] == ' '):
                mult +=1
            if x+1 < Nsize and (copyBoard[y][x+1] == player or copyBoard[y][x+1] == ' '):
                mult +=2
            rate +=1 * x * mult
        elif y-1 > -1 and copyBoard[y-1][x] == player:
            copyBoard[y][x] = '-'
            y-=1
            mult = 1
            if y-1 > -1 and (copyBoard[y-1][x] == player or copyBoard[y-1][x] == ' '):
                mult +=1
            if x+1 < Nsize and (copyBoard[y][x+1] == player or copyBoard[y][x+1] == ' '):
                mult +=2
            rate += 1*x*mult
        else:
            return rate





#-------------------------------------------------------------------------------------------
def checkForWin(X, Y, player, boardCopy):
    global Nsize
    won = False
    if X == Nsize -1:
        return True
    if X+1 < Nsize and boardCopy[Y][X+1] == player:
        xb = copy.deepcopy(boardCopy)
        xb[Y][X] = '>'
        won = checkForWin(X + 1, Y, player, xb)
        if won:
            return won
    if X-1 > -1 and boardCopy[Y][X-1] == player:
        xb = copy.deepcopy(boardCopy)
        xb[Y][X] = '<'
        won = checkForWin(X - 1, Y, player, xb)
        if won:
            return won
    if Y+1 < Nsize and boardCopy[Y+1][X] == player:
        ypb = copy.deepcopy(boardCopy)
        ypb[Y][X] = '^'
        won = checkForWin(X, Y + 1, player, ypb)
        if won:
            return won
    if Y-1 > -1 and boardCopy[Y-1][X] == player:
        ymb = copy.deepcopy(boardCopy)
        ymb[Y][X] = 'v'
        won = checkForWin(X,Y - 1,player, ymb)
        if won:
            return won
    return False


#--------------------------------------------------------------------------------------------
def printBoard():
    global board
    print("\n")
    for row in range(Nsize):
        index = Nsize-1-row
        print(board[index])


#--------------------------------------------------------------------------------------------
def ResetGrid():
    global Nsize, amMachine
    board = [ [ ' ' for i in range(Nsize) ] for j in range(Nsize) ]
    if amMachine == 'y':
        for row in range(Nsize):
            for column in range(Nsize):
                if (column % 2) == 1 and (row % 2) == 0:
                    board[row][column] = 'H'
                elif (column % 2) == 0 and (row % 2)== 1:
                    board[row][column] = 'M'
    else:
        for row in range(Nsize):
            for column in range(Nsize):
                if (column % 2) == 1 and (row % 2) == 0:
                    board[row][column] = 'M'
                elif (column % 2) == 0 and (row % 2)== 1:
                    board[row][column] = 'H'
    return board


#--------------------------------------------------------------------------------------------
def GetWhoMovesFirst():
    global humanTurn
    moveFirst = input("Do you want to go first Y/N?")
    if moveFirst == 'Y' or moveFirst == 'y':
        humanTurn = True
    else:
        humanTurn = False
    return


#--------------------------------------------------------------------------------------------
def GetHumanPlayerMove():
    global board, Nsize
    validMove = False
    while not validMove:
        #printBoard()
        Hmove = input("What is your next move? In format xCoordinate, Ycoordinate \n")
        xCoor = int(Hmove[0])
        yCoor = int(Hmove[2])
        if type(xCoor) == int and type(yCoor) == int:
            if xCoor > Nsize or yCoor > Nsize:
                print("Those coordinates are outside the bounds of the board. Please try again.")
            else:
                print("x coor ", xCoor, "y coor ", yCoor)
                if board[yCoor][xCoor] == ' ':
                    board[yCoor][xCoor] = "H"
                    validMove = True
                    break

        print("Invalid move. Try again. ")
        validMove = False
    return


#--------------------------------------------------------------------------------------------
def columnCheck(player):
    global Nsize, board
    columnFound = False
    for x in range(Nsize):
        y = 0
        while not columnFound:
            if y == Nsize - 1 and board[y][x] == player:
                columnFound = True
                #print("Found Column")
                break
            elif y+1 < Nsize and board[y+1][x] == player:
                y += 1
            else:
                 break
    return columnFound


#--------------------------------------------------------------------------------------------
def tieCheck():
    global Nsize, board
    _ = True
    for x in range(Nsize):
        for y in range(Nsize):
            if board[y][x] == ' ':
                return False
    return True


#--------------------------------------------------------------------------------------------

def theGame():
    global humanTurn, winner, amMachine
    Won = False
    winner = " "
    machineMoved = False
    while not Won:
        if humanTurn:
            GetHumanPlayerMove()
            g = copy.deepcopy(board)
            for y in range(0,Nsize):
                if g[y][0]== 'H':
                    if checkForWin(0,y, 'H',g):
                        Won = True
                        winner = "Humanity"

            if tieCheck():
                Won = True
            humanTurn = False
        elif not humanTurn:
            print("My turn")
            if not machineMoved and not amMachine:
                for y in range(0,Nsize):
                    if board[y][0] == ' ':
                        board[y][0] = 'M'
                        break
                printBoard()
                machineMoved = True
            else:
                GenerateComputerPlayerMove()
                g = copy.deepcopy(board)
                for y in range(0,Nsize):
                    if g[y][0] == 'M':
                        if checkForWin(0,y, 'M',g):
                            Won = True
                            winner = "The Machine"
            if tieCheck():
                Won = True
            humanTurn = True
    if winner == " ":
        print("It is a tie")
    else:
        print("The winner is :", winner)
    print("###############################################")
    printBoard()
    print("###############################################")
    return


#--------------------------------------------------------------------------------------------
def main():
    global Nsize, board, depth,amMachine
    Nsize = input("Enter a row/column size: ")
    Nsize = int(Nsize)
    depth = input("Enter a search depth: ")
    depth = int(depth)
    amMachine = input("Are you the machine this game y/n")
    GetWhoMovesFirst()
    board = ResetGrid()
    printBoard()
    theGame()
if __name__ == '__main__':
    main()
