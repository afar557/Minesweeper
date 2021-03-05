from visualizeBoard import visualizeBoard
from generateMine import generateUserGrid
from collections import deque
import random

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

def basicAgent (realGrid): 
    dimension = len(realGrid)
    # Generate the user board
    userGrid = generateUserGrid(dimension)

    # Create dictionary with all the indices from the board
    cellsDict = {}
    for i in range(dimension):
        for j in range(dimension):
            cellsDict[(i,j)] = None
    # Queue for cells to be uncovered
    queue = deque()

    # Pick a cell randomly on the board, enque this cell and delete it from the dictionary
    queue.append( random.choice(list(cellsDict.keys())) )
    
    while queue:
        # Dequeue the cell
        currX, currY = queue.popleft()
        if (currX,currY) not in cellsDict:
            if not queue:
                if len(cellsDict)==0:
                    print("Returning inside while line 59")
                    return userGrid

                # Pick a random index from dict and enqueue it
                queue.append( random.choice(list(cellsDict.keys())) )
            continue

        # Query the dequeued cell
        if realGrid[currX][currY] == "M":
            # Mark it as a mine
            userGrid[currX][currY] = 'M'
            visualizeBoard(userGrid, "basic agent")

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # Pick another random cell and queue it
            if len(cellsDict)!=0:
                queue.append( random.choice(list(cellsDict.keys())) )
        
        else:
            # Get the clue from the real grid
            clue = realGrid[currX][currY]
            userGrid[currX][currY] = clue
            visualizeBoard(userGrid, "basic agent")

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # Get the state of thr neighbors
            hoodState = getState (userGrid, (currX,currY))
            numofneigh = len(hoodState["mines"])+len(hoodState["hidden"])+len(hoodState["safeSquares"])

            if clue-len(hoodState["mines"])==len(hoodState["hidden"]):
                # Mark every cell in hidden as a mine (m) and remove their indeices from dict
                for x,y in hoodState["hidden"]:
                    userGrid[x][y] = 'm'
                    cellsDict.pop((x,y))
                visualizeBoard(userGrid, "basic agent")
            
            if (numofneigh-clue)-len(hoodState["safeSquares"])==len(hoodState["hidden"]):
                # Enqueue every cell in hidden
                for x,y in hoodState["hidden"]:
                    queue.append((x,y))

        if len(queue)==0:
            if len(cellsDict)!=0:
                # Pick a random index from dict and enqueue it
                queue.append( random.choice(list(cellsDict.keys())) )

    for x,y in cellsDict:
        userGrid[x][y] = 'm'
    visualizeBoard(userGrid, "basic agent")
    print("Returning outside while")
    return userGrid