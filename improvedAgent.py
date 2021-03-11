from basicagent import updateKnowledge, addEquationToKnowledge

# import updateKnowledge()

# import addEquationToKnowledge()

# always do advanced inference on knowledge before calling probability


{A:,B:,C:,D:,E:,F:}

stack: A
{A:0,B:,C:1,D:1,E:,F:}

stack:A,B
{A:0,B:0,C:1,D:1,E:,F:}

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


A+B+C=1
A+C+D=2
B+C+D+E+F=3

[1][1][1][0][0][0]|[1]
[1][0][1][1][0][0]|[2] -> 
[0][1][1][1][1][1]|[3]

[1][1][1][0][0][0]|[1]
[0][-1][0][1][0][0]|[1] ->
[0][1][1][1][1][1]|[3]

A-D-E-F=-2     |  -A+E+F=1
B-D=-1         |   D-B=1     -> D=1, B=0
C+2D+E+F=4     |   C+E+F=2

A
{A:0,B:,C:1,D:1,E:,F:}
A, B
{A:0,B:0,C:1,D:1,E:,F:}
A,B,E
# {A:0,B:0,C:1,D:1,E:0,F:1}

A,B
#{A:0,B:0,C:1,D:1,E:1,F:0}

A
{A:0,B:1,C:1,D:1,E:,F:} -> not a terminal bc nonsatisfactory

pop A 
{A:1,B:,C:,D:,E:,F:}