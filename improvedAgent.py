from basicagent import updateKnowledge, addEquationToKnowledge
from sympy import *
from copy import deepcopy
from collections import OrderedDict
from generateMine import generateMinesGrid, generateUserGrid
from collections import deque
import random
from copy import deepcopy
from visualizeBoard import visualizeBoard

# always do advanced inference on knowledge before calling probability

# {A:,B:,C:,D:,E:,F:}

# stack: A
# {A:0,B:,C:1,D:1,E:,F:}

# stack:A,B
# {A:0,B:0,C:1,D:1,E:,F:}

def calculateNewKnowledge(inferredVars, knowledge):
    for eqn in knowledge:
        eq0 = deepcopy(eqn[0])
        for var in eq0:
            if var in inferredVars and inferredVars[var] != None:
                eqn[0].remove(var)
                eqn[1] -= inferredVars[var]

    i = 0
    while i < len(knowledge):
        if len(knowledge[i][0]) == 0:
            knowledge.remove(knowledge[i])
        else:
            i+=1

    return knowledge

def calculateprobability(knowledge):
    stack = []
    possibilities = []
    cellsInKnowledge = OrderedDict()
    inferredVars = {}

    for eqn in knowledge:
        for cell in eqn[0]:
            cellsInKnowledge[cell] = None

    count = 0
    knowledge2 = deepcopy(knowledge)

    while(true):

        cellsInKnowledge2 = deepcopy(cellsInKnowledge)

        for cell in cellsInKnowledge:

            while(len(inferredVars)!=0):
                inferredVars = basicInference(knowledge2)
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
                for var in inferredVars:
                    cellsInKnowledge2[var] = inferredVars[var]

            if cellsInKnowledge2[cell] == None:

                stack.append((cell,deepcopy(cellsInKnowledge2)))
                cellsInKnowledge2[cell] = 0
                inferredVars[cell] = 0
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
                
        possibilities.append(deepcopy(cellsInKnowledge2))

        if len(stack)==0:
            break

        val,cellsInKnowledge = stack.pop()
        
        cellsInKnowledge[val] = 1
        inferredVars[val] = 1

        knowledge2 = calculateNewKnowledge(cellsInKnowledge, deepcopy(knowledge))
        inferredVars = basicInference(knowledge2)

    # print("This is possibilities:")
    # for poss in possibilities:
    #     print(poss)
    for cell in cellsInKnowledge:
        summ=0
        for poss in possibilities:
            if poss[cell]==1:
                summ+=1
        cellsInKnowledge[cell]= summ/len(possibilities)
    # print()
    # mini = 2
    # ans = 0
    # for x in cellsInKnowledge:
    #     print(x, ":", cellsInKnowledge[x])
    #     if cellsInKnowledge[x]<mini:
    #         mini = cellsInKnowledge[x]
    #         ans = x
    # print("Answer is :", ans)
    # return ans
    return cellsInKnowledge

def basicInference(knowledge):
    inferredVars = {}

    for equation in knowledge:
        if len(equation[0]) == equation[1]:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 1

        elif equation[1] == 0:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 0

    return inferredVars

# advancedInference
#   create the matrix
#   intitial dict = {}
#   do rref on the matrix
#   for each row in rref(matrix)
#       do the inference rules
#   return None if you cant infer anything
#   return dict with safe and mine cells

def advancedInference(knowledge):
    # print("knowledge in advance")
    # for eqn in knowledge:
    #     print(eqn)
    # print()

    colOfVars = {}
    count = 0
    for eqn in knowledge:
        for var in eqn[0]:
            if var not in colOfVars:
                colOfVars[var] = count
                count += 1
    # print("befor",colOfVars)
    matrix = Matrix()
    # print(len(knowledge))
    row = 0
    for equation in knowledge:
        matrixRow = [0]*(len(colOfVars)+1)
        # print(matrixRow)
        # print(colOfVars)
        for var in equation[0]:
            if var in colOfVars:
                # print('variable', var, 'col', colOfVars[var])
                matrixRow[colOfVars[var]] = 1
        # print(matrixRow)
        matrixRow[-1] = equation[1]
        # print(matrixRow)
        matrix = matrix.row_insert(row, Matrix([matrixRow]))
        row += 1
    # print("Matrix : {}".format(matrix)) 

    # for some reason the order of the variables changes in the dict because sets are unordered

    M_rref = matrix.rref()
    M_rref = M_rref[0]

    # print("Matrix : {}".format(M_rref)) 
    sumOfVars = 0
    inferredVars = {}
    for i in range(M_rref.shape[0]):
        if M_rref[i, M_rref.shape[1]-1] == 0:
            # change this
            for j in range(M_rref.shape[1]-1):
                if M_rref[i,j] != 0:
                    keys = list(colOfVars.keys())
                    values = list(colOfVars.values())
                    position = values.index(j)
                    inferredVars[ keys[position] ] = 0
                    # inferredVars[ M_rref[i,j] ] = 0
        else:
            for j in range(M_rref.shape[1]-1):
                if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                    sumOfVars += M_rref[i,j]
            if sumOfVars == M_rref[i, M_rref.shape[1]-1]:
                # print("helloooooo")
                for j in range(M_rref.shape[1]-1):
                    keys = list(colOfVars.keys())
                    values = list(colOfVars.values())
                    # print("keys contains ", keys)
                    # print("values contains ", values)
                    position = values.index(j)
                    if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                        # make colOfVars an array maybe to improve runtime???
                        inferredVars[ keys[position] ] = 1
                    elif M_rref[i,j] != 0:
                        inferredVars[ keys[position] ] = 0
            sumOfVars = 0

    # print("INFERRED VARS",inferredVars)
    return inferredVars

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
            visualizeBoard(userGrid, "basic agent")

            # Remove the index from the dictionary
            cellsDict.pop((currX,currY))

            # Update knowledge base so that it removes the mine
            knowledge = updateKnowledge((currX,currY), userGrid, knowledge)
        
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

        # run advanced inference
        # NOTE: might need to run advance in a while loop until it returns no inferred Vars
        inferredVars = advancedInference(knowledge)
        knowledge = calculateNewKnowledge(inferredVars, knowledge)
        for var in inferredVars:
            # print(var)
            x,y = var
            if inferredVars[(x,y)] == 1:
                userGrid[x][y] = 'm'
                cellsDict.pop((x,y))
            elif inferredVars[(x,y)] == 0:
                if (x,y) not in queue:
                    queue.append((x,y))

        visualizeBoard(userGrid, "advanced agent")

        if len(queue)==0:
            if len(cellsDict)!=0:
                print("queue is empty")
                
                # Find the probablity that the cells in knowledge to be a mine
                probabilityOfCells = calculateprobability(knowledge)
                print("Calculating probability:", probabilityOfCells)
                mini = 2
                ans = 0
                for (x,y) in probabilityOfCells:
                    if probabilityOfCells[(x,y)] == 1 and userGrid[x][y] == '?':
                        print("should have been caught in advanced inference")
                        userGrid[x][y] = 'm'
                        knowledge = updateKnowledge((x,y), userGrid, knowledge)
                        cellsDict.pop((x,y))
                    elif probabilityOfCells[(x,y)] == 0 and userGrid[x][y] == '?':
                        if (x,y) not in queue:
                            print("should have been caught in advanced inference")
                            queue.append((x,y))
                    else:
                        if probabilityOfCells[(x,y)] < mini:
                            mini = probabilityOfCells[(x,y)]
                            ans = (x,y)
                if ans == 0 and len(queue) == 0:
                    print("picking from random")
                    print("Knowledge is :", knowledge)
                    randIndex = random.choice(list(cellsDict.keys()))
                    while randIndex in queue:
                        randIndex = random.choice(list(cellsDict.keys()))
                    queue.append(randIndex)
                elif len(queue) == 0:
                    print("picking from probability")
                    if ans not in queue:
                        queue.append(ans)

    # for x,y in cellsDict:
    #     userGrid[x][y] = 'm'
    # visualizeBoard(userGrid, "basic agent")
    return userGrid

# def runAdvanced(knowledge):
#     while (true):
#         inferredVars = advancedInference(knowledge)
#         if len(inferredVars) == 0:
#             return knowledge
#         else:
#             # update knowledge to remove all of the inferred variables

# knowledge=[ [{(0,1),(1,0),(1,1)},1],
#             [{(0,1),(1,1),(1,2)},2],
#             [{(1,0),(1,1),(1,2),(2,0),(2,2)},3] ]

knowledge = [   [{(2, 4), (3, 4), (4, 3), (4, 2), (2, 3), (2, 2), (3, 2)}, 1],
                [{(3, 4), (4, 3)}, 0]  ]

# knowledge=[ [{(0,1),(1,0),(1,1)},1],
#             [{(1,1),(1,2)},2],
#             [{(1,0),(1,1),(1,2),(2,0),(2,2)},3] ]

# knowledge = [   [{(0,0), (1,0), (1,1), (1,2), (0,2)}, 1], 
#                 [{(2,0), (1,0), (1,1), (1,2), (2,2)}, 2]  ]

# inf = basicInference(knowledge)

# calculateprobability(knowledge)

# print("heyy",advancedInference(knowledge))
