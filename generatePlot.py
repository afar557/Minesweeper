import matplotlib.pyplot as plt
import numpy as np

from basicagent import basicAgent, finalScore
from improvedAgent import improvedAgent
from generateMine import generateMinesGrid

def getPlot():
    dimension = 20
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(1, 400, 10):
        mines = x.item()
        mineDensity.append(mines)
        basicSum=0
        improvedSum=0

        grid = generateMinesGrid(dimension, mines)

        for i in range(10):
            grid = generateMinesGrid(dimension, mines)
            basicSum += finalScore(grid, basicAgent(grid))
            improvedSum += finalScore(grid, improvedAgent(grid))
            
        basicSuccess.append(basicSum/10)
        advancedSuccess.append(improvedSum/10)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('mine density')
    plt.ylabel('avg rate of success')
    # plt.title('# of nodes explored by BFS - # of nodes explored by A*  VS  obstacle density p ')
    plt.legend()
    plt.show()

getPlot()
