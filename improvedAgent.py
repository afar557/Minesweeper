from basicagent import updateKnowledge, addEquationToKnowledge
from sympy import *
from copy import deepcopy
from collections import OrderedDict

# always do advanced inference on knowledge before calling probability

# {A:,B:,C:,D:,E:,F:}

# stack: A
# {A:0,B:,C:1,D:1,E:,F:}

# stack:A,B
# {A:0,B:0,C:1,D:1,E:,F:}

def calculateNewKnowledge(inferredVars, knowledge):
    # print("Inferred Variables are:", inferredVars)
    # print("Knowledge base before inferring:")
    # for x in knowledge:
    #     print(x)
    # print()
    for eqn in knowledge:
        # print("Current eq:", eqn)
        eq0 = deepcopy(eqn[0])
        # print("Current eq0:", eq0)
        for var in eq0:
            # print("Current Var:", var)
            if var in inferredVars and inferredVars[var] != None:
                eqn[0].remove(var)
                eqn[1] -= inferredVars[var]
        # if len(eqn[0])==0:
        #     print("Removed eq:",eqn[0])
        #     knowledge.remove(eqn)
        # print()
    # print("Knowledge base before removing:")
    # for x in knowledge:
    #     print(x)
    # print()
    i = 0
    while i < len(knowledge):
        if len(knowledge[i][0]) == 0:
            knowledge.remove(knowledge[i])
        else:
            i+=1
    # print("Knowledge base after inferring:")
    # for x in knowledge:
    #     print(x)
    # print()
    return knowledge

def calculateprobability(knowledge):
    stack = []
    possibilities = []
    cellsInKnowledge = OrderedDict()
    inferredVars = {}

    for eqn in knowledge:
        # print("eqn outside while", eqn)
        for cell in eqn[0]:
            # print("cell outside while",cell)
            cellsInKnowledge[cell] = None

    count = 0
    knowledge2 = deepcopy(knowledge)
    # print("befor while",cellsInKnowledge)
    while(true):
        cellsInKnowledge2 = deepcopy(cellsInKnowledge)
        # print("im here again")
        for cell in cellsInKnowledge:
            # print("cell in for",cell)
            while(len(inferredVars)!=0):
                inferredVars = basicInference(knowledge2)
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
                for var in inferredVars:
                    cellsInKnowledge2[var] = inferredVars[var]

            # inferredVars = basicInference(knowledge2)
            # # print("Inferred Vars at 72:",inferredVars)

            # knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
            # # print("New Knowledge is at line 88:", knowledge2)
            
            # # print("this is inferred",inferredVars)
            # for var in inferredVars:
            #     # update the value in cellsInKnowledge
            #     cellsInKnowledge2[var] = inferredVars[var]
            # # print("CellsinKnowledge after inferrence:", cellsInKnowledge2)

            if cellsInKnowledge2[cell] == None:
                # print("Exploring : ", cell)
                stack.append((cell,deepcopy(cellsInKnowledge2)))
                # print("Appended to the stack :", stack)
                
                cellsInKnowledge2[cell] = 0
                # print("CellsinKnowledge here is : ", cellsInKnowledge2)

                inferredVars[cell] = 0
                # print("inferredVars after guess", inferredVars)
                # print("befor", knowledge2)
                knowledge2 = calculateNewKnowledge(inferredVars, knowledge2)
                # print("Guessing ", cell, "to be 0")
                # print("New Knowledge is:", knowledge2)
                # print()
                # inferredVars = runAdvanced
                # print("after", knowledge2)
                # inferredVars = {}
                
        possibilities.append(deepcopy(cellsInKnowledge2))
        # print("Poss",cellsInKnowledge2)

        # possibilities.append(cellsInKnowledge2)
        if len(stack)==0:
            break

        val,cellsInKnowledge = stack.pop()
        # print("Val is:", val)
        
        cellsInKnowledge[val] = 1
        # print("CellsinKnowledge is:", cellsInKnowledge)

        inferredVars[val] = 1
        # print("Old knowledge is:")
        # for x in knowledge:
        #     print(x)
        # print()
        knowledge2 = calculateNewKnowledge(cellsInKnowledge, deepcopy(knowledge))
        # print("New knowledge is:")
        # for x in knowledge2:
        #     print(x)
        # inferredVars = runAdvanced(knowledge2)
        inferredVars = basicInference(knowledge2)
        # print("Inferred Vars at 112: ", inferredVars)
        # print()
        
        # print("length of stack",len(stack))
        # for item in stack:
        #     print(item)
        # print()
        # print()
        # print()

        count+=1
        # if count == 10: break
    print("This is possibilities:")
    for poss in possibilities:
        print(poss)
    for cell in cellsInKnowledge:
        summ=0
        for poss in possibilities:
            if poss[cell]==1:
                summ+=1
        cellsInKnowledge[cell]= summ/len(possibilities)
    print()
    mini = 2
    ans = 0
    for x in cellsInKnowledge:
        print(x, ":", cellsInKnowledge[x])
        if cellsInKnowledge[x]<mini:
            mini = cellsInKnowledge[x]
            ans = x
    print("Answer is :", ans)
    return ans

def basicInference(knowledge):
    inferredVars = {}
    # for eqn in knowledge:
    #     print(eqn)
    # print()
    for equation in knowledge:
        if len(equation[0]) == equation[1]:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 1
                # print((x,y), ":", 1)
        elif equation[1] == 0:
            for x,y in equation[0]:
                inferredVars[(x,y)] = 0
                # print((x,y), ":", 0)
    # print("inferredVars:", inferredVars)
    return inferredVars

# advancedInference
#   create the matrix
#   intitial dict = {}
#   do rref on the matrix
#   for each row in rref(matrix)
#       do the inference rules
#   return None if you cant infer anything
#   return dict with safe and mine cells


knowledge=[ [{(0,1),(1,0),(1,1)},1],
            [{(0,1),(1,1),(1,2)},2],
            [{(1,0),(1,1),(1,2),(2,0),(2,2)},3] ]

# knowledge=[ [{(0,1),(1,0),(1,1)},1],
#             [{(1,1),(1,2)},2],
#             [{(1,0),(1,1),(1,2),(2,0),(2,2)},3] ]

# knowledge = [   [{(0,0), (1,0), (1,1), (1,2), (0,2)}, 1], 
#                 [{(2,0), (1,0), (1,1), (1,2), (2,2)}, 2]  ]

# inf = basicInference(knowledge)
# for eq in knowledge:
#     print(eq)
# print()

# print("Inference is:",inf)
# print()
calculateprobability(knowledge)

# newknow = calculateNewKnowledge(inf, knowledge)
# for eq in newknow:
#     print(eq)

def advancedInference(knowledge):
    colOfVars = {}
    count = 0
    for eqn in knowledge:
        for var in eqn[0]:
            if var not in colOfVars:
                colOfVars[var] = count
                count += 1
    print("befor",colOfVars)
    matrix = Matrix()
    # print(len(knowledge))
    row = 0
    for equation in knowledge:
        matrixRow = [0]*(len(colOfVars)+1)
        # print(matrixRow)
        print(colOfVars)
        for var in equation[0]:
            if var in colOfVars:
                print('variable', var, 'col', colOfVars[var])
                matrixRow[colOfVars[var]] = 1
        # print(matrixRow)
        matrixRow[-1] = equation[1]
        print(matrixRow)
        matrix = matrix.row_insert(row, Matrix([matrixRow]))
        row += 1
    print("Matrix : {}".format(matrix)) 

    # for some reason the order of the variables changes in the dict because sets are unordered

    M_rref = matrix.rref()
    M_rref = M_rref[0]

    print("Matrix : {}".format(M_rref)) 
    sumOfVars = 0
    inferredVars = {}
    for i in range(M_rref.shape[0]):
        if M_rref[i, M_rref.shape[1]-1] == 0:
            # change this
            for j in range(M_rref.shape[1]-1):
                if M_rref[i,j] != 0:
                    inferredVars[ M_rref[i,j] ] = 0
        else:
            for j in range(M_rref.shape[1]-1):
                if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                    sumOfVars += M_rref[i,j]
            if sumOfVars == M_rref[i, M_rref.shape[1]-1]:
                print("helloooooo")
                for j in range(M_rref.shape[1]-1):
                    keys =list(colOfVars.keys())
                    values = list(colOfVars.values())
                    position = values.index(j)
                    if (M_rref[i, M_rref.shape[1]-1] > 0 and M_rref[i,j] > 0) or (M_rref[i, M_rref.shape[1]-1] < 0 and M_rref[i,j] < 0):
                        # make colOfVars an array maybe to improve runtime???
                        inferredVars[ keys[position] ] = 1
                    elif M_rref[i,j] != 0:
                        inferredVars[ keys[position] ] = 0
            sumOfVars = 0

    print("INFERRED VARS",inferredVars)
    return inferredVars

    # print(M_rref[2, M_rref.shape[1]-1])

    # print(M_rref[2,6])
    # print(M_rref.shape)

# advancedInference(knowledge)

# def runAdvanced(knowledge):
#     while (true):
#         inferredVars = advancedInference(knowledge)
#         if len(inferredVars) == 0:
#             return knowledge
#         else:
#             # update knowledge to remove all of the inferred variables

# A+B+C=1
# A+C+D=2
# B+C+D+E+F=3

# [1][1][1][0][0][0]|[1]
# [1][0][1][1][0][0]|[2] -> 
# [0][1][1][1][1][1]|[3]

# [1][1][1][0][0][0]|[1]
# [0][-1][0][1][0][0]|[1] ->
# [0][1][1][1][1][1]|[3]

# A-D-E-F=-2     |  -A+E+F=1
# B-D=-1         |   D-B=1     -> D=1, B=0
# C+2D+E+F=4     |   C+E+F=2

# A
# {A:0,B:,C:1,D:1,E:,F:}
# A, B
# {A:0,B:0,C:1,D:1,E:,F:}
# A,B,E
# # {A:0,B:0,C:1,D:1,E:0,F:1}

# A,B
# #{A:0,B:0,C:1,D:1,E:1,F:0}

# A
# {A:0,B:1,C:1,D:1,E:,F:} -> not a terminal bc nonsatisfactory

# pop A 
# {A:1,B:,C:,D:,E:,F:}