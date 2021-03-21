from visualizeBoard import visualizeBoard
from generateMine import generateUserGrid
from collections import deque
import random
from copy import deepcopy

# calculate the final score of the agent
def finalScore (realGrid, userGrid):
    # get the board dimension
    dimension = len(realGrid)
    # initialize score to 0
    score = 0
    # loop through every cell in the board
    for i in range(dimension):
        for j in range(dimension):
            # if the cell in the realGrid is a mine and we marked it as a mine in userGrid, increment score by 1
            if realGrid[i][j]=='M' and userGrid[i][j]=='m':
                score+=1
    return score

# function to add an equation to the knowledge base
def addEquationToKnowledge(index, grid, knowledge):
    # get the x,y coordinates of the current cell
    x,y = index
    # get the dimension of the grid
    dimension = len(grid)
    # get the value of the clue from grid
    clue = grid[x][y]

    # create an empty set to hold unknown neighbors
    neighbors = set()
    
    # for each of the valid neighbors, get an equation
    for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1, y+1),(x+1, y-1), (x-1, y+1), (x-1, y-1)):
        if 0 <= x2 < dimension and 0 <= y2 < dimension:
            # If the neighbor is a mine, decrement the clue by 1
            if grid[x2][y2]=='M' or grid[x2][y2]=='m':
                clue -= 1
            # If the neighbor is uncovered, add it to the set of neighbors
            elif grid[x2][y2]=='?':
                neighbors.add((x2,y2))
    # add the equation to the knowledge base
    knowledge.append([neighbors,clue])

    return knowledge

# function to update the knowledge base
def updateKnowledge(index, grid, knowledge):
    # get the x,y coordinate of the current cell
    x,y = index
    # if the current cell is actually a mine or is marked as a mine
    if grid[x][y] == 'M' or grid[x][y] == 'm':
        # for each equation in the knowledge base
        for equation in knowledge:
            # if the mine exists in the equation
            if (x,y) in equation[0]:
                # remove the mine from left side of equation
                equation[0].remove((x,y))
                # subtract 1 from right side of equation
                equation[1] -= 1
    # otherwise if it is not a mine
    else:
        for equation in knowledge:
            if (x,y) in equation[0]:
                # simply remove the safe cell from left side of equation
                equation[0].remove((x,y))

    # use while loop to remove equations that are completely empty
    i = 0
    while i < len(knowledge):
        # if equation at i is empty
        if len(knowledge[i][0]) == 0:
            # remove the equation from knowledge & dont increment i, bc i will be the next element
            knowledge.remove(knowledge[i])
        else:
            # otherwise increment bc nothing was removed, and need to move to next element
            i+=1
            
    return knowledge

# function for basic agent
def basicAgent (realGrid): 
    # get the dimension of the grid
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
            # visualizeBoard(userGrid, "basic agent")

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # Update knowledge base so that it removes the mine
            knowledge = updateKnowledge((currX,currY), userGrid, knowledge)    
        else:
            # Get the clue from the real grid
            clue = realGrid[currX][currY]

            # update clue in user grid and visualize it
            userGrid[currX][currY] = clue
            # visualizeBoard(userGrid, "basic agent")

            # add to knowledge base
            knowledge = addEquationToKnowledge((currX, currY), userGrid, knowledge)

            # update knowledge base
            knowledge = updateKnowledge((currX, currY), userGrid, knowledge)

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

        # check the knowledge base to see if we can infer anything (basic inference)
        for equation in knowledge:
            # if the number of unknown neighbors equals the clue, mark each neighbor as a mine
            if len(equation[0]) == equation[1]:
                hoodNeighbors = deepcopy(equation[0])
                for x,y in hoodNeighbors:
                    userGrid[x][y] = 'm'
                    cellsDict.pop((x,y))
                    knowledge = updateKnowledge((x,y), userGrid, knowledge)
            # if the clue is zero, we know all neighbors are safe, so add them to the queue
            elif equation[1] == 0:
                # Enqueue every cell
                for x,y in equation[0]:
                    if (x,y) not in queue:
                        queue.append((x,y))

        # visualizeBoard(userGrid, "basic agent")

        # if the queue is empty, there are no guaranteed safe cells, so pick randomly
        if len(queue)==0:
            # make sure cellsDict is not empty so there are still some uncovered cells left
            if len(cellsDict)!=0:
                # Pick a random index from dict that is not in the queue and enqueue it
                randIndex = random.choice(list(cellsDict.keys()))
                while randIndex in queue:
                    randIndex = random.choice(list(cellsDict.keys()))

                queue.append(randIndex)

    # if there is anything left uncovered in cellDict, mark it as a mine
    for x,y in cellsDict:
        userGrid[x][y] = 'm'
    # visualizeBoard(userGrid, "basic agent")
    
    return userGrid