import random
import sys
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
import copy
import datetime

# moves = UP, RIGHT, DOWN, LEFT
moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def isPositionLegal(board, x, y):
    n = len(board)
    return ((x >= 0) and (x < n) and (y >= 0) and (y < n))

def nextPos(x,y, move):
    nextX = x + move[0]
    nextY = y + move[1]

    return nextX, nextY

def canMove(board, direction):

    mv = moves[direction]
    x, y = findGap(board)
    x2, y2 = nextPos(x, y, mv)

    return isPositionLegal(board, x2, y2)

# def canMove(board):
#     x, y = findGap(board)
#
#     for mv in moves:
#         x2, y2 = nextPos(x, y, mv)
#         if isPositionLegal(board, x2, y2):
#             return True
#
#     return False

def possibleMoves(board):

    global moves
    x, y = findGap(board)

    res = []
    for mv in moves:
        x2, y2 = nextPos(x, y, mv)
        if isPositionLegal(board, x2, y2):
            res.append(mv)

    return res


def moveGap(board, move):

    x, y = findGap(board)
    x2, y2 = nextPos(x, y, move)

    tmp = board[x][y]
    board[x][y] = board[x2][y2]
    board[x2][y2] = tmp

def findGap(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i,j
    return -1, -1

def printBoard(board):

    print("")
    for row in board:
        row_str = ""
        for cell in row:
            row_str += str(cell) + " "
        print(row_str)

def translateMoveToLetter(move):
    m1,m2 = move
    if m1 == -1 and m2 == 0:
            return 'U'
    if m1 == 0 and m2 == 1:
            return 'R'
    if m1 == 1 and m2 == 0:
            return 'D'
    if m1 ==0 and m2 == -1:
            return 'L'

def manhattanDistance(board):
        distance = 0
        l  = len(board)
        for i in range(l):
            for j in range(l):
               if board[i][j] != 0 and board[i][j] != (n*i+j+1):
                #Mapping to actual positions to find Manhattan distance - xA,yA are the actual positions
                 rem = board[i][j] % l
                 quotient = int(board[i][j] / l)
                 if rem == 0:
                    xA = quotient-1
                    yA = l-1;
                    
                 else:
                    xA = quotient
                    yA = rem-1   
                 #print(str(xA)+"  "+str(yA))
                 distance += abs(xA-i)+abs(yA-j)
                # print(str(board[i][j])+"  "+str(xA)+"  "+str(yA)+"  "+str(i)+"  "+str(j))
        return distance



def misplacedTiles(board):
    misplaced = 0
    l  = len(board)
    for i in range(l):
        for j in range(l):
           if board[i][j] != 0 and board[i][j] != (n*i+j+1):
             misplaced += 1
    return misplaced                

def calculateHeuristic(board):
    return misplacedTiles(board)+manhattanDistance(board)       

def astar(board):
    print("Inside astar")
    start = datetime.datetime.now()
    visitedStates = []
    steps = 0
    queue = Q.PriorityQueue() # queue of tuples with priority value )
    
    actualBoard = copy.deepcopy(board)
    #visitedStates.append(actualBoard)
    visitedStates.append([item for sublist in actualBoard for item in sublist])
    #print("actual board"+str(actualBoard))
    queue.put((calculateHeuristic(actualBoard),actualBoard,0, ''))    # (h+g,state,g)        

    while not queue.empty():
        steps += 1       
        boardConfig = queue.get() 
        fCurrent = boardConfig[0]
        board = boardConfig[1]
        gCurrent = boardConfig[2]
        pathCurrent = boardConfig[3]
        #if steps == 10:
         #  print("ending : ")
          # for v in visitedStates:
           #        print(v)
           #break;
    #    print("**********************************************")
     #   printBoard(board)
      #  print("**********************************************")
        if misplacedTiles(board) == 0:                      #Check the goal state before expansion
                final = datetime.datetime.now() - start
                print("breaking with answer")
                printBoard(board)
                print("answer path is "+pathCurrent)
                print("Time taken : ")
                print(final.total_seconds())
                break;
        actualBoard = copy.deepcopy(board)
        movesList = possibleMoves(board)
        for move in movesList:
          #  print("Move: "+str(move))
            moveGap(board,move)             #Make the move
            heuristic = calculateHeuristic(board) #Calculate number of misplaced tiles
           # print("No. of misplaced tiles : "+str(misplaced))
            #printBoard(board)
            
            oneDBoard = [item for sublist in board for item in sublist]

            if not oneDBoard in visitedStates:
             #       print("visited : ")
            #        print(board)
                    queue.put((heuristic+gCurrent+1,board,gCurrent+1, pathCurrent+translateMoveToLetter(move))) # add new h', ie. h+g , board, new g and current path to queue     
                    #visitedStates.append(board)
                    visitedStates.append([item for sublist in board for item in sublist])
            
            board = copy.deepcopy(actualBoard)         #Go back to current state to check the next move

    print("Number of steps : "+str(steps))

if __name__ == '__main__':

    n = 0
    k = -1
    algo = -1
    in_file = ''
    out_file = ''
    process_input = False

    if len(sys.argv) == 5:
        print("here")
        algo = int(sys.argv[1])
        n = int(sys.argv[2])
        in_file = open(sys.argv[3],'r')
        out_file = open(sys.argv[4],'w')
        process_input = True
    elif len(sys.argv) == 4:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
        out_file = open(sys.argv[3], 'w')
    elif len(sys.argv) == 3:
        n = int(sys.argv[1])
        out_file = open(sys.argv[2], 'w')
    else:
        print('Wrong number of arguments. Usage:\npuzzleGenerator.py <N> <K - number of moves> <OUTPATH>\npuzzleGenerator.py <N> <OUTPATH>')
    print('n = ' + str(n))
    print('k = '+str(k))
    print('algo = '+str(algo))
    if process_input == False:
        if k == -1:
            a = list(range(1, n*n + 1))
            random.shuffle(a)

            for i in range(n):
                for j in range(n):
                    cur = a[i * n + j]
                    if cur == (n*n):
                        out_file.write('')
                    else:
                        out_file.write(str(cur))
                    if j != (n-1):
                        out_file.write(',')
                out_file.write('\n')
        else:
            board = []
            for i in range(n):
                board.append([])
                for j in range(n):
                    if (n*i+j+1) == n*n:
                        board[i].append(0)
                    else:
                        board[i].append(n * i + j + 1)

            printBoard(board)

            for move_cnt in range(k):
                pos_moves = possibleMoves(board)
                move = random.choice(pos_moves)
                moveGap(board, move)

            printBoard(board)

            for row in board:
                for i in range(len(row)):
                    cell = row[i]
                    if cell != 0:
                        out_file.write(str(cell))
                    if i != (len(row) - 1):
                        out_file.write(",")


                out_file.write("\n")

    else:
        print("THIS")
        board = []
        for i in range(n):
            currentLine = in_file.readline().split(',')
            board.append([])
            for currentNumber in currentLine:
                a = 0 if currentNumber=='\n' or currentNumber == '' else int(currentNumber)
                board[i].append(a)    
        print("Initial setup :")        
        printBoard(board)   
     #   print(misplacedTiles(board))
        astar(board)        

    out_file.close()
