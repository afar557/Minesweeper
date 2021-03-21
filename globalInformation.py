from basicagent import updateKnowledge, addEquationToKnowledge
from generateMine import generateMinesGrid, generateUserGrid
from visualizeBoard import visualizeBoard
from improvedAgent import calculateNewKnowledge, advancedInference 

from sympy import *
from collections import deque
import random
from copy import deepcopy

def globalImprovedAgent(realGrid, numOfMines):
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

    allCells = set(cellsDict.keys())
    knowledge.append([allCells, numOfMines])

    while queue:
        # Dequeue the cell
        currX, currY = queue.popleft()

        # Query the dequeued cell
        if realGrid[currX][currY] == 'M':
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

            # add to knowldege base
            knowledge = addEquationToKnowledge((currX, currY), userGrid, knowledge)

            # update knowledge base
            knowledge = updateKnowledge((currX, currY), userGrid, knowledge)

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

        while (true):
            inferredVars = advancedInference(deepcopy(knowledge))
            knowledge = calculateNewKnowledge(inferredVars, knowledge)
            for var in inferredVars:
                x,y = var
                if inferredVars[(x,y)] == 1:
                    userGrid[x][y] = 'm'
                    cellsDict.pop((x,y))
                elif inferredVars[(x,y)] == 0:
                    if (x,y) not in queue:
                        queue.append((x,y))
            if len(inferredVars) ==0:
                break

        # visualizeBoard(userGrid, "advanced agent")

        if len(queue)==0:
            if len(cellsDict)!=0:
                randIndex = random.choice(list(cellsDict.keys()))

                while randIndex in queue:
                    randIndex = random.choice(list(cellsDict.keys()))
                queue.append(randIndex)

    return userGrid

