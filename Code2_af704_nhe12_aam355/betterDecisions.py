from basicagent import updateKnowledge, addEquationToKnowledge
from generateMine import generateMinesGrid, generateUserGrid
from visualizeBoard import visualizeBoard
from improvedAgent import calculateNewKnowledge, calculateprobability, advancedInference 

from sympy import *
from collections import deque
import random
from copy import deepcopy

def betterImprovedAgent(realGrid):
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
            # TRY TO SEE IF IT IS POSSIBLE TO PUT A CAP ON THE PROBABILITY SO IF PROB>0.3 PICK RANDOMLY
            if len(cellsDict)!=0:                
                # Find the probablity that the cells in knowledge to be a mine
                probabilityOfCells = calculateprobability(deepcopy(knowledge))
                mini = 2
                ans = 0
                for (x,y) in probabilityOfCells:
                    if probabilityOfCells[(x,y)] == 1 and userGrid[x][y] == '?':
                        userGrid[x][y] = 'm'
                        knowledge = updateKnowledge((x,y), userGrid, knowledge)
                        cellsDict.pop((x,y))
                    elif probabilityOfCells[(x,y)] == 0 and userGrid[x][y] == '?':
                        if (x,y) not in queue:
                            queue.append((x,y))
                    else:
                        if probabilityOfCells[(x,y)] < mini:
                            mini = probabilityOfCells[(x,y)]
                            ans = (x,y)
                if (ans == 0 or mini>0.3) and len(queue) == 0 :
                    cellsInKnowledge = set()
                    for eq in knowledge: 
                        for var in eq[0]: 
                            cellsInKnowledge.add(var)
                    if (len(cellsInKnowledge) != len(cellsDict)):    
                        randIndex = random.choice(list(cellsDict.keys()))

                        while randIndex in queue or randIndex in cellsInKnowledge:
                            randIndex = random.choice(list(cellsDict.keys()))
                        queue.append(randIndex)
                if len(queue) == 0 and ans!= 0:
                    if ans not in queue:
                        queue.append(ans)

    return userGrid
