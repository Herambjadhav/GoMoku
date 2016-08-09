import sys
import copy
import string

infinity = 1000000000
mappingList = (string.ascii_uppercase)

# Find position of all possible next moves
def findAllPossiblePositions(list, value1, value2, value3, boardSize):
    positionList = []
    for i, x in enumerate(list):
        for j, y in enumerate(x):
            if y == value1 or y == value2:
                # west
                if j - 1 >= 0 and list[i][j - 1] == value3:
                    if (next((item for item in positionList if item['x'] == i and item['y'] == j - 1 ), None)) is None:
                        position = {'x': i, 'y': j - 1, 'value': 0}
                        positionList.append(position)
                # east
                if j + 1 < boardSize and list[i][j + 1] == value3:
                    if (next((item for item in positionList if item['x'] == i and item['y'] == j + 1), None)) is None:
                        position = {'x': i, 'y': j + 1 , 'value': 0}
                        positionList.append(position)
                # North
                if i - 1 >= 0 and list[i - 1][j] == value3:
                    if (next((item for item in positionList if item['x'] == i - 1  and item['y'] == j), None)) is None:
                        position = {'x': i - 1, 'y': j, 'value': 0}
                        positionList.append(position)
                # South
                if i + 1 < boardSize and list[i + 1][j] == value3:
                    if (next((item for item in positionList if item['x'] == i + 1 and item['y'] == j), None)) is None:
                        position = {'x': i + 1, 'y': j, 'value': 0}
                        positionList.append(position)
                # North west
                if i - 1 >= 0 and j - 1 >= 0 and list[i - 1][j - 1] == value3:
                    if (next((item for item in positionList if item['x'] == i - 1  and item['y'] == j - 1), None)) is None:
                        position = {'x': i - 1, 'y': j - 1, 'value': 0}
                        positionList.append(position)
                # North east
                if i - 1 >= 0 and j + 1 < boardSize and list[i - 1][j + 1] == value3:
                    if (next((item for item in positionList if item['x'] == i - 1 and item['y'] == j + 1), None)) is None:
                        position = {'x': i - 1, 'y': j + 1, 'value': 0}
                        positionList.append(position)
                # South west
                if i + 1 < boardSize and j - 1 >= 0 and list[i + 1][j - 1] == value3:
                    if (next((item for item in positionList if item['x'] == i + 1 and item['y'] == j - 1), None)) is None:
                        position = {'x': i + 1, 'y': j - 1, 'value': 0}
                        positionList.append(position)
                # South East
                if i + 1 < boardSize and j + 1 < boardSize and list[i + 1][j + 1] == value3:
                    if (next((item for item in positionList if item['x'] == i + 1 and item['y'] == j + 1), None)) is None:
                        position = {'x': i + 1, 'y': j + 1, 'value': 0}
                        positionList.append(position)
    return positionList

# Block Checks
def blockChecks(opponentsStoneCount, position, sideOpen):
    # Block checks

    # blockClosedFour
    if opponentsStoneCount == 4 and sideOpen == 0:
        position['value'] = position['value'] + 10000

    if opponentsStoneCount == 3:
        # blockOpenThree
        if sideOpen == 1:
            position['value'] = position['value'] + 500
        # blockClosedThree
        else:
            position['value'] = position['value'] + 100

# Create Checks
def createChecks(myStoneCount, position, eastOpen, westOpen):
    # winning move
    if myStoneCount == 4:
        position['value'] = position['value'] + 50000
        position['win'] = True

    if myStoneCount == 3:
        # createOpenFour
        if eastOpen == 1 and westOpen == 1:
            position['value'] = position['value'] + 5000
        # createClosedFour
        elif eastOpen == 1 or westOpen == 1:
            position['value'] = position['value'] + 1000

    if myStoneCount == 2:
        # createOpenThree
        if eastOpen == 1 and westOpen == 1:
            position['value'] = position['value'] + 50
        # createClosedThree
        elif eastOpen == 1 or westOpen == 1:
            position['value'] = position['value'] + 10

    if myStoneCount == 1:
        # createOpenTwo
        if eastOpen == 1 and westOpen == 1:
            position['value'] = position['value'] + 5
        # createClosedTwo
        elif eastOpen == 1 or westOpen == 1:
            position['value'] = position['value'] + 1


# Calculate heuristic
def calculateHeuristic(position, board, stone, opponent, boardSize):
    ### Row checks
    myStoneCount = 0
    opponentsStoneCount = 0

    # check west
    y = position['y']
    x = position['x']
    westOpen = 0

    while y > 0 :
        y = y - 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if y == 0:
                westOpen = 0
        elif board[x][y] == opponent:
            westOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            westOpen = 1
            break

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, westOpen)
        westOpen = 0

    # check east
    y = position['y']
    x = position['x']
    eastOpen = 0
    opponentsStoneCount = 0

    while y < boardSize - 1:
        y = y + 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if y == boardSize - 1:
                eastOpen = 0
        elif board[x][y] == opponent:
            eastOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            eastOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, eastOpen)
        eastOpen = 0

    # Create Checks
    createChecks(myStoneCount, position, eastOpen, westOpen)

    ### Column Checks

    myStoneCount = 0
    opponentsStoneCount = 0

    # check North
    y = position['y']
    x = position['x']
    northOpen = 0

    while x > 0:
        x = x - 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == 0:
                northOpen = 0
        elif board[x][y] == opponent:
            northOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            northOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, northOpen)
        northOpen = 0

    # Check South
    y = position['y']
    x = position['x']
    southOpen = 0
    opponentsStoneCount = 0

    while x < boardSize - 1:
        x = x + 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == boardSize - 1:
                southOpen = 0
        elif board[x][y] == opponent:
            southOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            southOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, southOpen)
        southOpen = 0

    # Create Checks
    createChecks(myStoneCount, position, northOpen, southOpen)

    ###  Diagonal Checks 1

    myStoneCount = 0
    opponentsStoneCount = 0

    # check North-West
    y = position['y']
    x = position['x']
    northWestOpen = 0

    while x > 0 and y > 0:
        x = x - 1
        y = y - 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == 0 or y == 0:
                northWestOpen = 0
        elif board[x][y] == opponent:
            northWestOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            northWestOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, northWestOpen)
        northWestOpen = 0

    # Check South-East
    y = position['y']
    x = position['x']
    southEastOpen = 0
    opponentsStoneCount = 0

    while x < boardSize -  1 and y < boardSize - 1 :
        x = x + 1
        y = y + 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == boardSize - 1 or y == boardSize - 1:
                southEastOpen = 0
        elif board[x][y] == opponent:
            southEastOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            southEastOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, southEastOpen)
        southEastOpen = 0

    # Create Checks
    createChecks(myStoneCount, position, northWestOpen, southEastOpen)

    ### Diagonal Checks 2

    myStoneCount = 0
    opponentsStoneCount = 0

    # check North-East
    y = position['y']
    x = position['x']
    northEastOpen = 1

    while x > 0 and y < boardSize - 1 :
        x = x - 1
        y = y + 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == 0 or y == boardSize - 1:
                northEastOpen = 0
        elif board[x][y] == opponent:
            northEastOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            northEastOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, northEastOpen)
        northEastOpen = 0

    # Check South-West
    y = position['y']
    x = position['x']
    southWestOpen = 1
    opponentsStoneCount = 0

    while x < boardSize - 1 and y > 0:
        x = x + 1
        y = y - 1
        if board[x][y] == stone:
            myStoneCount = myStoneCount + 1
            if opponentsStoneCount != 0:
                break;
            if x == boardSize - 1 or y == 0:
                southWestOpen = 0
        elif board[x][y] == opponent:
            southWestOpen = 0
            if myStoneCount != 0:
                break;
            else:
                opponentsStoneCount = opponentsStoneCount + 1
        else:
            southWestOpen = 1
            break;

    # Block checks
    if opponentsStoneCount > 0:
        myStoneCount = 0
        blockChecks(opponentsStoneCount, position, southWestOpen)
        southWestOpen = 0

    # Create Checks
    createChecks(myStoneCount, position, northEastOpen, southWestOpen)

def mapToAplhabets(x):
    return mappingList[x]

# traversal for alpha beta
def logTraversalAlphaBeta(fileHandler, position, depth, boardSize, node):
    if position['value'] == infinity:
        value = 'Infinity'
    elif position['value'] == -infinity:
        value = '-Infinity'
    else:
        value = position['value']

    if node['alpha'] == infinity:
        alpha = 'Infinity'
    elif node['alpha'] == -infinity:
        alpha = '-Infinity'
    else:
        alpha = node['alpha']

    if node['beta'] == infinity:
        beta = 'Infinity'
    elif node['beta'] == -infinity:
        beta = '-Infinity'
    else:
        beta = node['beta']

    if position['x'] == 'root':
        # print position['x'], depth, position['value']
        fileHandler.write("%s,%d,%s,%s,%s\n" % (position['x'], depth, value, alpha, beta))
    else:
        # print mapToAplhabets(position['y']), boardSize - position['x'], depth, position['value']
        fileHandler.write("%s%d,%d,%s,%s,%s\n" % (mapToAplhabets(position['y']), boardSize - position['x'], depth, value, alpha, beta))


# Alpha Beta pruning
def alphaBeta(node, board, boardSize, cutOffDepth, stone, opponent, fileHandler, toggle):
    if node['depth'] > cutOffDepth - 1:
        return

    depth = node['depth'] + 1
    winFlag = False
    prune = False

    childList = findAllPossiblePositions(board, 'w', 'b', '.', boardSize)
    childList = sorted(childList, key=lambda item: (item['y'], - item['x']))

    for position in childList:
        # create node for new move
        newNode = {'parent':node, 'value': 0, 'depth': depth, 'position': position, 'children':[], 'sum':0, 'alpha': node['alpha'], 'beta': node['beta']}
        node['children'].append(newNode)

        # create board for new move
        tempBoard = copy.copy(board)
        tempBoard[position['x']][position['y']] = stone

        # calculate heuristic
        if depth == cutOffDepth:
            calculateHeuristic(position, tempBoard, stone, opponent, boardSize)
            if not toggle:
                position['value'] = -1 * position['value']
            position['value'] += node['sum']

            # check win condition
            if 'win' in position:
                winFlag = True
        else:
            temp = copy.copy(position)
            calculateHeuristic(temp, tempBoard, stone, opponent, boardSize)
            if not toggle:
                temp['value'] = -1 * temp['value']
            newNode['sum'] = temp['value'] + node['sum']

            # set min/max node
            if toggle:
                position['value'] = infinity
            else:
                position['value'] = -infinity

            # check win condition
            if 'win' in temp:
                position['value'] = newNode['sum']
                winFlag = True

        # log
        logTraversalAlphaBeta(fileHandler, position, depth, boardSize, newNode)

        # call child node recursively only if win condition is false
        if not winFlag:
            alphaBeta(newNode, tempBoard, boardSize, cutOffDepth, opponent, stone , fileHandler, not toggle)

        tempBoard[position['x']][position['y']] = '.'

        parentPosition = node['position']
        if toggle:
            if position['value'] > parentPosition['value']:
                parentPosition['value'] = position['value']
            if position['value'] > node['alpha']:
                if position['value'] >= node['beta']:
                    prune = True
                else:
                    node['alpha'] = position['value']
                    newNode['alpha'] = position['value']
        else:
            if position['value'] < parentPosition['value']:
                parentPosition['value'] = position['value']
            if position['value'] < node['beta']:
                if position['value'] <= node['alpha']:
                    prune = True
                else:
                    node['beta'] = position['value']
                    newNode['beta'] = position['value']

        logTraversalAlphaBeta(fileHandler, node['position'], node['depth'], boardSize, node)

        if node['beta'] <= node['alpha'] or prune:
            break

        # reset winFlag
        if winFlag:
            winFlag = False


def logTraversal(fileHandler, position, depth, boardSize):
    if position['value'] == infinity:
        value = 'Infinity'
    elif position['value'] == -infinity:
        value = '-Infinity'
    else:
        value = position['value']
    if position['x'] == 'root':
        #print position['x'], depth, position['value']
        fileHandler.write("%s,%d,%s\n" % (position['x'], depth, value))
    else:
        #print mapToAplhabets(position['y']), boardSize - position['x'], depth, position['value']
        fileHandler.write("%s%d,%d,%s\n" % (mapToAplhabets(position['y']), boardSize - position['x'], depth, value))

# create Tree
def minimax(node, board, boardSize, cutOffDepth, stone, opponent, fileHandler, toggle):
    if node['depth'] > cutOffDepth - 1:
        return

    depth = node['depth'] + 1
    winFlag = False

    childList = findAllPossiblePositions(board, 'w', 'b', '.', boardSize)
    childList = sorted(childList, key=lambda item: (item['y'], - item['x']))

    for position in childList:
        # create node for new move
        newNode = {'parent':node, 'value': 0, 'depth': depth, 'position': position, 'children':[], 'sum':0}
        node['children'].append(newNode)

        # create board for new move
        tempBoard = copy.copy(board)
        tempBoard[position['x']][position['y']] = stone

        # calculate heuristic
        if depth == cutOffDepth:
            calculateHeuristic(position, tempBoard, stone, opponent, boardSize)
            if not toggle:
                position['value'] = -1 * position['value']
            position['value'] += node['sum']

            # check win condition
            if 'win' in position:
                winFlag = True
        else:
            temp = copy.copy(position)
            calculateHeuristic(temp, tempBoard, stone, opponent, boardSize)
            if not toggle:
                temp['value'] = -1 * temp['value']
            newNode['sum'] = temp['value'] + node['sum']

            # set min/max node
            if toggle:
                position['value'] = infinity
            else:
                position['value'] = -infinity

            # check win condition
            if 'win' in temp:
                position['value'] = newNode['sum']
                winFlag = True

        # log
        logTraversal(fileHandler, position, depth, boardSize)

        # call child node recursively only if win condition is false
        if not winFlag:
            minimax(newNode, tempBoard, boardSize, cutOffDepth, opponent, stone , fileHandler, not toggle)
        tempBoard[position['x']][position['y']] = '.'

        parentPosition = node['position']
        if toggle:
            if position['value'] > parentPosition['value']:
                parentPosition['value'] = position['value']
        else:
            if position['value'] < parentPosition['value']:
                parentPosition['value'] = position['value']

        logTraversal(fileHandler, node['position'], node['depth'], boardSize)

        # reset winFlag
        if winFlag:
            winFlag = False

def outputNextStep(board, boardSize):
    fileHandler = open("next_state.txt", "w")
    for i in range(boardSize):
        for j in range(boardSize):
            fileHandler.write(board[i][j])
        fileHandler.write('\n')

    fileHandler.close()

### Greedy Algo
def runGreedy(board, stone, opponent, boardSize):
    # get all possible next moves
    positionList = findAllPossiblePositions(board, 'w', 'b', '.', boardSize)
    print 'positionList length : ', len(positionList)
    # print 'positionList : ', positionList

    # calculate heuristic values
    for position in positionList:
        calculateHeuristic(position, board, stone, opponent, boardSize)

    # sort positionList on value
    sortedPositionList = sorted(positionList, key = lambda item: ( - item['value'], item['y'], - item['x'] ))
    #print 'sorted positionList : ', sortedPositionList

    print 'Board with heuristics'
    newBoard = copy.deepcopy(board);
    for position in positionList:
        newBoard[position['x']][position['y']] = position['value']

    for i in range(boardSize):
        for j in range(boardSize):
            print newBoard[i][j],
        print

    # write output to file
    nextMove = sortedPositionList[0]
    board[nextMove['x']][nextMove['y']] = stone
    outputNextStep(board, boardSize);

### MiniMax Algo
def runMiniMax(board, stone, opponent, boardSize, cutOffDepth):
    # create tree
    fileHandler = open('traverse_log.txt','w')
    fileHandler.write("Move,Depth,Value\n")
    fileHandler.write("%s,%d,%s\n" % ("root",0,"-Infinity"))

    # create root node
    position = {'x':'root', 'value':-infinity}
    node = {'parent':0, 'value': 0, 'children': [], 'depth': 0, 'position': position, 'sum':0}

    # create and log tree traversal
    minimax(node, board, boardSize, cutOffDepth, stone, opponent, fileHandler, True)
    fileHandler.close();

    nextMove = {}
    # find next move
    for child in node['children']:
        pos = child['position']
        if pos['value'] == position['value']:
            print 'next move: ', pos['x'], pos['y']
            nextMove['x'] = pos['x']
            nextMove['y'] = pos['y']
            break;

    # write output to file
    board[nextMove['x']][nextMove['y']] = stone
    outputNextStep(board, boardSize)

### AlphaBeta Algo
def runAlphaBeta(board, stone, opponent, boardSize, cutOffDepth):
    # create tree
    fileHandler = open('traverse_log.txt', 'w')
    fileHandler.write("Move,Depth,Value,Alpha,Beta\n")
    fileHandler.write("%s,%d,%s,%s,%s\n" % ("root", 0, "-Infinity", "-Infinity", "Infinity"))

    # create root node
    position = {'x': 'root', 'value': -infinity}
    node = {'parent': 0, 'value': 0, 'children': [], 'depth': 0, 'position': position, 'sum': 0, 'alpha': -infinity, 'beta':infinity}

    # create and log tree traversal for alpha beta
    alphaBeta(node, board, boardSize, cutOffDepth, stone, opponent, fileHandler, True)
    fileHandler.close();

    nextMove = {}
    # find next move
    for child in node['children']:
        pos = child['position']
        if pos['value'] == position['value']:
            print 'next move: ', pos['x'], pos['y']
            nextMove['x'] = pos['x']
            nextMove['y'] = pos['y']
            break;

    # write output to file
    board[nextMove['x']][nextMove['y']] = stone
    outputNextStep(board, boardSize)

print 'Argument count : ', len(sys.argv)
#exit if file name is not provided as command line argument
if len(sys.argv) != 2:
    print 'Please send file name as command line argument'
    exit(0)

fileName = sys.argv[1]
print 'File name : ', sys.argv[1]

#read all lines of file
fileHandler = open(fileName,"r")
lines = fileHandler.readlines()
fileHandler.close()

algoType = int(lines[0])
print 'Algo Type : ', algoType

player = int(lines[1])
print 'Player : ', player

cutOffDepth = int(lines[2])
print 'Cut Off Depth : ', cutOffDepth

boardSize = int(lines[3])
print 'Board Size : ', boardSize

# initialize board matrix
board = [[char for char in line.strip()] for line in lines[4:]]

# output
print 'Original Board'
for i in range(boardSize):
    for j in range(boardSize):
        print board[i][j],
    print

if player == 1:
    stone = 'b'
    opponent = 'w'
else:
    stone = 'w'
    opponent = 'b'

# call appropriate algo
if algoType == 1:
    runGreedy(board, stone, opponent, boardSize)
elif algoType == 2:
    runMiniMax(board, stone, opponent, boardSize, cutOffDepth)
elif algoType == 3:
    runAlphaBeta(board, stone, opponent, boardSize, cutOffDepth)
else:
    print 'Please enter a valid algo type'
    exit(1)

