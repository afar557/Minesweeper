def generateMinesGrid(dimension, numMines):
    grid = [['?' for x in range(dimension)] for y in range(dimension)]
    while numMines >0:
        xVal = random.randint(0,dimension-1)
        yVal = random.randint(0,dimension-1)
        if grid[xVal][yVal]=='?':
            grid[xVal][yVal]='M'
            numMines-=1

    for x in range(dimension):
        for y in range(dimension):
            if grid[x][y]!='M':
                surroundingMines = 0
                for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1, y+1),(x+1, y-1), (x-1, y+1), (x-1, y-1)):
                    if 0 <= x2 < dimension and 0 <= y2 < dimension and grid[x2][y2]=='M':
                        surroundingMines+=1
                grid[x][y]= surroundingMines
    for row in grid:
        print(row)
    return grid
