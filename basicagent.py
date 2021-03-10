from visualizeBoard import visualizeBoard
from generateMine import generateUserGrid
from collections import deque
import random
from copy import deepcopy

def finalScore (realGrid, userGrid):
    dimension = len(realGrid)
    score = 0
    for i in range(dimension):
        for j in range(dimension):
            if realGrid[i][j]=='M' and userGrid[i][j]=='m':
                score+=1
    return score

# Method to get the state of all neighbors in user board
def getState (grid, index):
    x,y = index
    dimension = len(grid)

    # Dict for states of the neighbors
    state = {"safeSquares":[], "mines":[], "hidden":[]}
    
    for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1, y+1),(x+1, y-1), (x-1, y+1), (x-1, y-1)):
        if 0 <= x2 < dimension and 0 <= y2 < dimension:
            # If the neighbor is a mine
            if grid[x2][y2]=='M' or grid[x2][y2]=='m':
                state["mines"].append((x2,y2))
            # If the neighbor is uncovered
            elif grid[x2][y2]=='?':
                state["hidden"].append((x2,y2))
            # If the neighbor is safe
            elif type(grid[x2][y2]) == int:
                state["safeSquares"].append((x2,y2))
    return state

def addEquationToKnowledge(index, grid, knowldege):
    x,y = index
    dimension = len(grid)

    clue = grid[x][y]

    # create an empty set to hold unknown neighbors
    neighbors = set()
    
    for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1, y+1),(x+1, y-1), (x-1, y+1), (x-1, y-1)):
        if 0 <= x2 < dimension and 0 <= y2 < dimension:
            # If the neighbor is a mine
            if grid[x2][y2]=='M' or grid[x2][y2]=='m':
                clue -= 1
            # If the neighbor is uncovered
            elif grid[x2][y2]=='?':
                neighbors.add((x2,y2))
    
    knowldege.append([neighbors,clue])

    return knowldege

def updateKnowledge(index, grid, knowldege):
    x,y = index

    if grid[x][y] == 'M' or grid[x][y] == 'm':
        for equation in knowldege:
            if (x,y) in equation[0]:
                # remove the mine from left side of equation
                equation[0].remove((x,y))
                # subtract 1 from right side of equation
                equation[1] -= 1
    else:
        for equation in knowldege:
            if (x,y) in equation[0]:
                # remove the safe cell from left side of equation
                equation[0].remove((x,y))

    return knowldege

def basicAgent (realGrid): 
    dimension = len(realGrid)
    # Generate the user board
    userGrid = generateUserGrid(dimension)

    # Create dictionary with all the indices from the board
    cellsDict = {}
    for i in range(dimension):
        for j in range(dimension):
            cellsDict[(i,j)] = None

    # Create the knowledge base which holds the system of equations
    knowledge = []

    # Create queue for cells to be uncovered
    queue = deque()

    # Pick a cell randomly on the board, enque this cell and delete it from the dictionary
    queue.append( random.choice(list(cellsDict.keys())) )
    
    while queue:
        # Dequeue the cell
        currX, currY = queue.popleft()

        # Query the dequeued cell
        if realGrid[currX][currY] == "M":
            # Mark it as a mine
            userGrid[currX][currY] = 'M'
            visualizeBoard(userGrid, "basic agent")

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # Update knowledge base so that it removes the mine
            knowledge = updateKnowledge((currX,currY), userGrid, knowledge)

            # Pick another random cell and queue it
            if len(cellsDict)!=0:
                randIndex = random.choice(list(cellsDict.keys()))
                if randIndex not in queue:
                    queue.append(randIndex)
                    print("line 118")
                    print(queue)
                    print()
        
        else:
            # Get the clue from the real grid
            clue = realGrid[currX][currY]

            # update clue in user grid and visualize it
            userGrid[currX][currY] = clue
            visualizeBoard(userGrid, "basic agent")

            # add to knowldege base
            knowledge = addEquationToKnowledge((currX, currY), userGrid, knowledge)

            # update knowledge base
            knowledge = updateKnowledge((currX, currY), userGrid, knowledge)

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # # DONT NEED --------------------------------

            # # Get the state of the neighbors
            # hoodState = getState(userGrid, (currX,currY))
            # numofneigh = len(hoodState["mines"])+len(hoodState["hidden"])+len(hoodState["safeSquares"])

            # if clue-len(hoodState["mines"])==len(hoodState["hidden"]):
            #     # Mark every cell in hidden as a mine (m) and remove their indeices from dict
            #     for x,y in hoodState["hidden"]:
            #         userGrid[x][y] = 'm'
            #         cellsDict.pop((x,y))
            #     visualizeBoard(userGrid, "basic agent")
            
            # elif (numofneigh-clue)-len(hoodState["safeSquares"])==len(hoodState["hidden"]):
            #     # Enqueue every cell in hidden
            #     for x,y in hoodState["hidden"]:
            #         if (x,y) not in queue:
            #             queue.append((x,y))

            # ------------------------------------------------    
        
        # check knowledge base
        for equation in knowledge:
            if len(equation[0]) == equation[1]:
                hoodNeighbors = deepcopy(equation[0])
                for x,y in hoodNeighbors:
                    userGrid[x][y] = 'm'
                    cellsDict.pop((x,y))
                    knowledge = updateKnowledge((x,y), userGrid, knowledge)
                knowledge.remove(equation)
            elif equation[1] == 0:
                # Enqueue every cell in hidden
                for x,y in equation[0]:
                    if (x,y) not in queue:
                        queue.append((x,y))
                        print("line 174")
                        print(queue)
                        print()
                knowledge.remove(equation)

        visualizeBoard(userGrid, "basic agent")

        if len(queue)==0:
            if len(cellsDict)!=0:
                # Pick a random index from dict and enqueue it
                randIndex = random.choice(list(cellsDict.keys()))
                while randIndex in queue:
                    randIndex = random.choice(list(cellsDict.keys()))

                queue.append(randIndex)
                print("line 174")
                print(queue)
                print()

    for x,y in cellsDict:
        userGrid[x][y] = 'm'
    visualizeBoard(userGrid, "basic agent")
    return userGrid

# grid = [[1, '?', 2],
#         ['?', '?', '?'],
#         ['?', 3, '?']]
# knowledge = addEquationToKnowledge((0,0),grid,[])
# knowledge = addEquationToKnowledge((0,2),grid,knowledge)
# knowledge = addEquationToKnowledge((2,1),grid,knowledge)
# print(knowledge)

# grid = [[1, 'M', 2],
#         ['?', '?', '?'],
#         ['?', 3, '?']]

# print(updateKnowledge((0,1), grid, knowledge))