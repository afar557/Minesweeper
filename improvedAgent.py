from basicagent import updateKnowledge, addEquationToKnowledge
from sympy import *

# import updateKnowledge()

# import addEquationToKnowledge()

# always do advanced inference on knowledge before calling probability


# {A:,B:,C:,D:,E:,F:}

# stack: A
# {A:0,B:,C:1,D:1,E:,F:}

# stack:A,B
# {A:0,B:0,C:1,D:1,E:,F:}

# calculate probability(knowledge)
# stack = []
# cellsInKnowledge = {}

# for every eqn in knowledge:
#   for cell:
#       cellsInKnowledge[cell] = None
# 
# for cell in cellsInKnowledge:
#   if cellsInKnowledge[cell] == None:
#       stack.append(cell)
#       cellsInKnowledge[cell] = 0
#       for every eqn in knowledge:
#           if eqn[1] == 0:
#               for cell2 in eqn[0]:
#                   if cell2 != cell1 
#                       if cellsInKnowledge[cell2] == None:
#                           cellsInKnowledge[cell2] = 0
#                       elif cellsInKnowledge[cell2] == 1:
#                           stack.pop()
#                           
#           elif :  to calculate sum of unknown cells                     
#           

# advancedInference
#   create the matrix
#   intitial dict = {}
#   do rref on the matrix
#   for each row in rref(matrix)
#       do the inference rules
#   return None if you cant infer anything
#   return dict with safe and mine cells
knowledge=[ [{'A','B','C'},1],
            [{'A','C','D'},2],
            [{'B','C','D','E','F'},3] ]

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
            for j in range(M_rref.shape[1]-1):
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

    # print(M_rref[2, M_rref.shape[1]-1])

    # print(M_rref[2,6])
    # print(M_rref.shape)

advancedInference(knowledge)

# improved agent
#   while (true):
#       inferredVars = advancedInference(knowledge)
#       if len(inferredVars) == 0:
#           break
#       else:
#           update knowledge to remove all of the inferred variables

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