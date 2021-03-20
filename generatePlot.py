import matplotlib.pyplot as plt
import numpy as np

from basicagent import basicAgent, finalScore
from improvedAgent import improvedAgent
from generateMine import generateMinesGrid
from betterDecisions import betterImprovedAgent
from globalInformation import globalImprovedAgent

def improvedPlot():
    dimension = 20
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, 400, 10):
        mines = x.item()
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        grid = generateMinesGrid(dimension, mines)

        for i in range(10):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, improvedAgent(grid))

            if (basicScore != 0):
                basicSum += finalScore(grid, basicAgent(grid))/mines
            else: 
                basicSum += finalScore(grid, basicAgent(grid))

            if (improvedScore != 0):
                improvedSum += finalScore(grid, improvedAgent(grid))/mines
            else: 
                improvedSum += finalScore(grid, improvedAgent(grid))
            
            
        basicSuccess.append(basicSum/10)
        advancedSuccess.append(improvedSum/10)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

def betterImprovedPlot():
    dimension = 20
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, 400, 10):
        mines = x.item()
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        grid = generateMinesGrid(dimension, mines)

        for i in range(10):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, betterImprovedAgent(grid))

            if (basicScore != 0):
                basicSum += finalScore(grid, basicAgent(grid))/mines
            else: 
                basicSum += finalScore(grid, basicAgent(grid))

            if (improvedScore != 0):
                improvedSum += finalScore(grid, betterImprovedAgent(grid))/mines
            else: 
                improvedSum += finalScore(grid, betterImprovedAgent(grid))
            
            
        basicSuccess.append(basicSum/10)
        advancedSuccess.append(improvedSum/10)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Better Decisions Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

def globalImprovedPlot():
    dimension = 20
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, 400, 10):
        mines = x.item()
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        grid = generateMinesGrid(dimension, mines)

        for i in range(10):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, globalImprovedAgent(grid, mines))

            if (basicScore != 0):
                basicSum += finalScore(grid, basicAgent(grid))/mines
            else: 
                basicSum += finalScore(grid, basicAgent(grid))

            if (improvedScore != 0):
                improvedSum += finalScore(grid, globalImprovedAgent(grid, mines))/mines
            else: 
                improvedSum += finalScore(grid, globalImprovedAgent(grid, mines))
            
            
        basicSuccess.append(basicSum/10)
        advancedSuccess.append(improvedSum/10)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Global Info Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

improvedPlot()