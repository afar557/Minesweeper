from basicagent import updateKnowledge, addEquationToKnowledge
from generateMine import generateMinesGrid, generateUserGrid
from visualizeBoard import visualizeBoard

from sympy import *
from collections import deque
import random
from copy import deepcopy

# NOTE: The improved agent uses an external library to calculate the rref of the matrix in order to get
# a simplified system of equations for the knowledge base. The professor said it is okay to use an 
# external library for this as long as it runs faster than our own implementation

# FIXME isnt this function the same as updateKnowledge except it takes a dict instead of an index? 
# ANS: yes it is actually lol just realized

# function to update the knowledge base given a set of inferred variables
def calculateNewKnowledge(inferredVars, knowledge):
    # for each equation in knowledge base
    for eqn in knowledge:
        # make deepcopy of LHS of equation in knowledge
        eq0 = deepcopy(eqn[0])
        # for each variable in the equation
        for var in eq0:
            # if var is in inferred and has a value
            if var in inferredVars and inferredVars[var] != None:
                # remove that var from LHS and update RHS with inference
                # ??? will this also skip because of the remove? 
                # no i dont think so
                eqn[0].remove(var)
                eqn[1] -= inferredVars[var]

    # use while loop to remove equations w empty LHS
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

# NOTE: This function is not used in improved agent. It is only used for extra credit purposes, see betterDecisions.py
# function finds all valid possibilities of all cells and returns a dict of cells with their probability of being a mine
def calculateprobability(knowledge):
    # initialize vars
    stack = []
    possibilities = []
    # NOTE replace cellsInKnowledge w normal dict
    cellsInKnowledge = {}
    inferredVars = {}

    # create dict to hold all cellsInKnowledge with value of None
    # cellsInKnowledge identifies if a cell has previously been visited
    for eqn in knowledge:
        for cell in eqn[0]:
            cellsInKnowledge[cell] = None

    # create deepcopy of original knowledge, so knowledge is maintained
    knowledge2 = deepcopy(knowledge)

    # calculates all possibilities by trying 0 then 1 at each terminal node and inferring the remaining vars
    while(true):

        #NOTE can be replaced w dict.copy() for faster processing
        cellsInKnowledge2 = deepcopy(cellsInKnowledge)

        # guesses 0 at every terminal node and infers what other variables would be based on that assignment
        for cell in cellsInKnowledge:
            while(len(inferredVars)!=0):
                # update inferred using basic inference
                inferredVars = basicInference(knowledge2)
                # update knowledge using new inferred vars
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)

                # update value of cellsInKnowledge to whats inferred
                for var in inferredVars:
                    cellsInKnowledge2[var] = inferredVars[var]

            # nothing has been inferred about that cell, or this cell has not been guessed before
            if cellsInKnowledge2[cell] == None:

                # add element we are guessing on to the stack along with inferences at that point (cellsInKnowledge2)
                # NOTE can be replaced w dict.copy() for faster processing
                stack.append((cell,deepcopy(cellsInKnowledge2)))

                # guess 0, since this is initial guess on this index
                cellsInKnowledge2[cell] = 0

                # add current guess to inferred vars and update knowledge 
                inferredVars[cell] = 0
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
                
        # add the assumed possibility to list of possibilities 
        # NOTE can be replaced w dict.copy() for faster processing  
        possibilities.append(deepcopy(cellsInKnowledge2))

        # if every valid possibility has been explored, then exit while loop
        if len(stack)==0:
            break

        # pop the last guessed element  
        val,cellsInKnowledge = stack.pop()
        
        # guess 1, since 0 was guessed on this element beofre 
        cellsInKnowledge[val] = 1

        # add current guess to inferred vars and update knowledge
        inferredVars[val] = 1
        knowledge2 = calculateNewKnowledge(cellsInKnowledge, deepcopy(knowledge))

        # try to infer using updated knowledge
        inferredVars = basicInference(knowledge2)
    
    # calculate probability of each cell being a mine
    for cell in cellsInKnowledge:
        summ=0
        for poss in possibilities:
            # if in any possibility a cell is a mine update sum
            if poss[cell]==1:
                summ+=1
        # divide sum by the number of possibilities
        cellsInKnowledge[cell]= summ/len(possibilities)

    # return dict of every cell and their probability 
    return cellsInKnowledge

# function that uses basic inference rules to get inferences
def basicInference(knowledge):
    # initialize empty dictionary of inferredVars
    inferredVars = {}
    # for each equation in knowledge base
    for equation in knowledge:
        # if the number of neighbors equals the clue, all neighbors are mines
        if len(equation[0]) == equation[1]:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 1
        # if the clue is 0, all the neighbors are safe
        elif equation[1] == 0:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 0

    return inferredVars

# funciton that does advancedInference by combining clues using RREF 
# NOTE: Using rref to calculate a simplified version of system of equations my cause there to be minimal error
# because there is a step in rref that divides an entire row by a coefficient to get a leading 1
# therefor when we are equating the sum to the RHS, there might be a decimal issue
# however, we decided that this is a vary small edge case and it didn't seem to be an issue overall.
def advancedInference(knowledge):
    # creates a dictionary with every variable and the col number they will be in the matrix
    colOfVars = {}
    count = 0
    for eqn in knowledge:
        for var in eqn[0]:
            if var not in colOfVars:
                colOfVars[var] = count
                count += 1

    # initialize matrix
    matrix = Matrix()
    # print(len(knowledge))
    row = 0

    # populate matrix with either 0 or 1, last column is the clue
    for equation in knowledge:
        matrixRow = [0]*(len(colOfVars)+1)
        for var in equation[0]:
            if var in colOfVars:
                matrixRow[colOfVars[var]] = 1
        matrixRow[-1] = equation[1]
        matrix = matrix.row_insert(row, Matrix([matrixRow]))
        row += 1
    # calculate the rref of the matrix
    M_rref = matrix.rref()
    M_rref = M_rref[0]

    sumOfVars = 0
    inferredVars = {}
    # traverse through the matrix to see if we can infer anything
    for i in range(M_rref.shape[0]):
        # if the RHS is 0, see if all the variables are positive or all negative
        if M_rref[i, M_rref.shape[1]-1] == 0:
            negativeSign = None
            safe = True

            for j in range(M_rref.shape[1]-1):
                if M_rref[i,j] > 0 and negativeSign == None:
                    negativeSign = False
                elif M_rref[i,j] < 0 and negativeSign == None:
                    negativeSign = True
                else:    
                    if (M_rref[i,j] > 0 and negativeSign == True) or (M_rref[i,j] < 0 and negativeSign == False):
                        safe = False
                        break
            # if the values are all positive or all negative, mark them all as safe cells
            if safe == True:
                for j in range(M_rref.shape[1]-1):
                    if M_rref[i,j] != 0:
                        keys = list(colOfVars.keys())
                        values = list(colOfVars.values())
                        position = values.index(j)
                        # add all cells to inferredVars with a value of 0 to say they are safe
                        inferredVars[ keys[position] ] = 0
        # otherwise if RHS is not 0, sum all the coefficients to see if it equals RHS
        else:
            for j in range(M_rref.shape[1]-1):
                # only sum the values on LHS if they have the same sign as RHS
                if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                    sumOfVars += M_rref[i,j]
            # if the sum equals RHS, we know all values with same sign as RHS are mines and values with opposite sign are safe cells
            if sumOfVars == M_rref[i, M_rref.shape[1]-1]:
                for j in range(M_rref.shape[1]-1):
                    keys = list(colOfVars.keys())
                    values = list(colOfVars.values())
                    position = values.index(j)
                    # mars all values with same sign as RHS as mines
                    if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                        inferredVars[ keys[position] ] = 1
                    # mark all values with opposite sign as safe cells
                    elif M_rref[i,j] != 0:
                        inferredVars[ keys[position] ] = 0
            sumOfVars = 0

    return inferredVars

# function for improved agent
def improvedAgent(realGrid):
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

        # continuosly call advancedInference until it returns nothing
        while (true):
            # call advanced inference
            inferredVars = advancedInference(deepcopy(knowledge))
            # break out of loop if there are no inferred vars
            if len(inferredVars) == 0:
                break
            # update the knowledge base with the new inferred Vars
            knowledge = calculateNewKnowledge(inferredVars, knowledge)
            # update user grid with inferred vars
            for var in inferredVars:
                x,y = var
                if inferredVars[(x,y)] == 1:
                    userGrid[x][y] = 'm'
                    cellsDict.pop((x,y))
                elif inferredVars[(x,y)] == 0:
                    if (x,y) not in queue:
                        queue.append((x,y))
            
        # visualizeBoard(userGrid, "advanced agent")

        # if the queue is empty and nothing is left to be inferred pick a random cell
        if len(queue)==0:
            if len(cellsDict)!=0:
                randIndex = random.choice(list(cellsDict.keys()))

                while randIndex in queue:
                    randIndex = random.choice(list(cellsDict.keys()))
                queue.append(randIndex)

    # visualizeBoard(userGrid, "basic agent")
    return userGrid
