import random
import sys
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
import copy
import datetime
import math

# moves = UP, RIGHT, DOWN, LEFT
moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
out_file = ''
f=''
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


def write_output(path,calc):
    global out_file
    global f    
    f.write(','.join(list(path)))
    f.write("$"+calc+"\n")
    


#Map moves to letters to create the output, ie. path to optimal solution
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

#Calculate manhattan distance for the current state Sum(|xi-xG| + |yi-yG|)
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
                    yA = l-1
                    
                 else:
                    xA = quotient
                    yA = rem-1   
                 #print(str(xA)+"  "+str(yA))
                 distance += abs(xA-i)+abs(yA-j)
                # print(str(board[i][j])+"  "+str(xA)+"  "+str(yA)+"  "+str(i)+"  "+str(j))
        return distance


#Calculate the number of misplaced tiles in the current state
def misplacedTiles(board):
    misplaced = 0
    l  = len(board)
    for i in range(l):
        for j in range(l):
           if board[i][j] != 0 and board[i][j] != (n*i+j+1):
             misplaced += 1
    return misplaced                


# def calculateHeuristic(board):
#     return misplacedTiles(board)+manhattanDistance(board)       


stackNodes = 0 #Number of nodes in the stack at a given point
maxNodes = 0 # To track the maximum number of nodes at any point in the stack

def iterativeDeepen(board,g,bound,visitedStates,path):
    global stackNodes
    global maxNodes

    #print(visitedStates)
    oneDBoard = [item for sublist in board for item in sublist]
    if not oneDBoard in visitedStates:
            
        visitedStates.append(oneDBoard)
    
    f = g+manhattanDistance(board) #Calculate the f value, f = g + h


    if f > bound:          # if we find a node with h value greater than current bound, then 
        return [f,False]   # return this bound to be used as next bound and indicate it is not success

    if  misplacedTiles(board) == 0:  # Perform goal test checking if there are any misplaced tiles
        print("Success path = "+path)
        print("Found result")
        print("Max nodes in stack : ")
        print(maxNodes)
        write_output(path+"$"+str(maxNodes)+"$"+depth)

        print("cost = "+str(g))      
        return [f,True]             # return success if Goal State found  


    actualBoard = copy.deepcopy(board)    
    minBound = math.inf     
                # The bound for next iteration is populated in this variable, ie. the minimum value of the max bounds we encounter
    movesList = possibleMoves(board)
    for move in movesList:              #For each next move possible,
        moveGap(board,move)             #Make the move to create the next state
        

        oneDBoard = [item for sublist in board for item in sublist]
   
        if oneDBoard in visitedStates:
            board = copy.deepcopy(actualBoard) #Copy back actual state of board in this state to generate next move on top of it
            continue        
        
        stackNodes += 1                 # Increase current value of depth of nodes in stack
        if  maxNodes < stackNodes:
                maxNodes = stackNodes   #If it is greater than existing maxNodes, make it as maxNodes value           

        nextBound,success = iterativeDeepen(board,g+1,bound,visitedStates,path+translateMoveToLetter(move)) # Perform iterative deepening for the next state
        stackNodes -= 1   #Reduce count of stackNodes as node is removed from stack

        if success == True:
            return [nextBound,True] 

        if nextBound < minBound:
            minBound = nextBound    # Update minBound if we find a lesser value for next bound

        board = copy.deepcopy(actualBoard) #Copy back actual state of board in this state to generate next move on top of it

        
    return [minBound,False]    #Solution not found, hence return minBound,ie. bound for next iteration

def idastar(board):
    print("Inside IDA*")
    start = datetime.datetime.now()             #To calculate time of execution
    actualBoard = copy.deepcopy(board)
    bound = manhattanDistance(actualBoard)      #Initial bound is the h value of root

    while True:
       

        board = copy.deepcopy(actualBoard)
        nextBound,success = iterativeDeepen(board,0,bound,[],'')  # Perform iterative deepening, always from root,ie. g = 0
        if success == True:                         # If success, ie. goal found
            final = datetime.datetime.now()-start
            #print("Finished")
            print("Time taken (in milliseconds) : ",end="")
            print(final.total_seconds()*1000)
            break
        else:
            bound = nextBound     #If not success, update bound to nextBound for next iteration


def astar(board,heu):
    print("Inside astar")
    start = datetime.datetime.now()    # To calculate time of execution
    visitedStates = []                 # List to keep track of visited states
    steps = 0                          # keeping track of steps for analysis purposes
    queue = Q.PriorityQueue() # queue of tuples with priority as the f value of the state)
    
    actualBoard = copy.deepcopy(board)
    #visitedStates.append(actualBoard)
    visitedStates.append([item for sublist in actualBoard for item in sublist]) #Add the initial state into visited list
    #print("actual board"+str(actualBoard))
    if heu == 1:
        queue.put((misplacedTiles(actualBoard),actualBoard,0, ''))    # (h+g,state,g,path)        
    else:
        queue.put((manhattanDistance(actualBoard),actualBoard,0, ''))    # (h+g,state,g,path)        

    while not queue.empty():
        steps += 1       
        boardConfig = queue.get() 
        fCurrent = boardConfig[0]
        board = copy.deepcopy(boardConfig[1])
        gCurrent = boardConfig[2]
        pathCurrent = boardConfig[3]

        if misplacedTiles(board) == 0:                      #Check the goal state after poping state out of queue
                final = datetime.datetime.now() - start
                print("breaking with answer")
                printBoard(board)
                print("answer path is "+pathCurrent)
                print("Time taken (in milliseconds)  : ",end="")
                print(final.total_seconds()*1000)
                print("Visited states: ",end = "")
                print(len(visitedStates))
                print("Queue len:  ",end="")
                print(len(queue.queue))   
                print("Explored states : ",end = "")
                print(len(visitedStates)-len(queue.queue))
                explored = len(visitedStates)-len(queue.queue)
                print("Depth : ")
                print(len(pathCurrent))
                write_output(pathCurrent,str(explored)+"$"+str(final.total_seconds()*1000)+"$"+str(len(pathCurrent))) 
                break;
        actualBoard = copy.deepcopy(board)
        movesList = possibleMoves(board)   #Collect all possible moves possible
        for move in movesList:             #Try each move possible
          #  print("Move: "+str(move))
            moveGap(board,move)             #Make the move
            if heu == 1:
                heuristic = misplacedTiles(board)
            else:
                heuristic = manhattanDistance(board) #Calculate the heuristic of this state
            
            oneDBoard = [item for sublist in board for item in sublist]
            if not oneDBoard in visitedStates:      # If not present in visitedStates, add it to visited state
                    visitedStates.append([item for sublist in board for item in sublist])

                    queue.put((heuristic+gCurrent+1,board,gCurrent+1, pathCurrent+translateMoveToLetter(move))) # add new h', ie. h+g , board, new g and current path to queue     
                    


            
            board = copy.deepcopy(actualBoard)         #Go back to current state to check the next move

    #print("Number of steps : "+str(steps))

if __name__ == '__main__':
    n = 0
    k = -1
    algo = -1
    in_file = ''


    if len(sys.argv) == 5:
        print("here")
        algo = int(sys.argv[1])
        n = int(sys.argv[2])
        in_file = open(sys.argv[3],'r')
        out_file = sys.argv[4]
        f = open(out_file,'w')
        print('n = ' + str(n))
        print('k = '+str(k))
        print('algo = '+str(algo))
        print("Solving Mode ")
        board = []
        for i in range(n):
            currentLine = in_file.readline().split(',')
            board.append([])
            for currentNumber in currentLine:
                a = 0 if currentNumber=='\n' or currentNumber == '' else int(currentNumber)
                board[i].append(a)    
        print("Initial setup :")        
        printBoard(board)
        
        if algo == 1:
            astar(board,1)     
            astar(board,2)   
            f.close()
        elif algo == 2:    
            idastar(board)

    else:
        print('Wrong number of arguments. Usage:\npuzzleSolver.py <A - Algorithm No.> <N -Puzzle Format> <INPUT_FILE_PATH> <OUTPUT_FILE_PATH>')
