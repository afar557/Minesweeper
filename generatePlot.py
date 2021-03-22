import matplotlib.pyplot as plt
import numpy as np

from basicagent import basicAgent, finalScore
from improvedAgent import improvedAgent
from generateMine import generateMinesGrid
from betterDecisions import betterImprovedAgent
from globalInformation import globalImprovedAgent

def improvedPlot():
    dimension = 20
    average =10
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, dimension**2, 10):
        mines = x.item()
        # print("num of mines is ", mines)
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        if mines ==0: 
            basicSuccess.append(1)
            advancedSuccess.append(1)
            continue

        grid = generateMinesGrid(dimension, mines)

        for i in range(average):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, improvedAgent(grid))

            if (basicScore != 0):
                basicSum += basicScore/mines
            else: 
                basicSum += basicScore

            if (improvedScore != 0):
                improvedSum += improvedScore/mines
            else: 
                improvedSum += improvedScore

            
            
        basicSuccess.append(basicSum/average)
        # print("basic sum is", basicSum/average)
        advancedSuccess.append(improvedSum/average)
        # print("advanced sum is ", improvedSum/average)


    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

def betterImprovedPlot():
    dimension = 20
    average =10
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, dimension**2, 10):
        mines = x.item()
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        if mines ==0: 
            basicSuccess.append(1)
            advancedSuccess.append(1)
            continue

        grid = generateMinesGrid(dimension, mines)

        if mines ==0: 
            basicSuccess.append(1)
            advancedSuccess.append(1)
            continue

        for i in range(average):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, betterImprovedAgent(grid))

            if (basicScore != 0):
                basicSum += basicScore/mines
            else: 
                basicSum += basicScore

            if (improvedScore != 0):
                improvedSum += improvedScore/mines
            else: 
                improvedSum += improvedScore
            
            
        basicSuccess.append(basicSum/average)
        advancedSuccess.append(improvedSum/average)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Better Decisions Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

def globalImprovedPlot():
    dimension = 20
    average =10
    
    basicSuccess = []
    advancedSuccess = []
    mineDensity = []

    for x in np.arange(0, dimension**2, 10):
        mines = x.item()
        mineDensity.append(mines/(dimension*dimension))
        basicSum=0
        improvedSum=0

        if mines ==0: 
            basicSuccess.append(1)
            advancedSuccess.append(1)
            continue

        grid = generateMinesGrid(dimension, mines)

        for i in range(average):
            grid = generateMinesGrid(dimension, mines)
            basicScore = finalScore(grid, basicAgent(grid))
            improvedScore = finalScore(grid, globalImprovedAgent(grid, mines))

            if (basicScore != 0):
                basicSum += basicScore/mines
            else: 
                basicSum += basicScore

            if (improvedScore != 0):
                improvedSum += improvedScore/mines
            else: 
                improvedSum += improvedScore
            
            
        basicSuccess.append(basicSum/average)
        advancedSuccess.append(improvedSum/average)

    plt.plot(mineDensity, basicSuccess, label = "Basic Algorithm")
    plt.plot(mineDensity, advancedSuccess, label = "Improved Algorithm")
    plt.xlabel('percentage of mine density')
    plt.ylabel('avg rate of success')
    plt.title('Success rate of Global Info Improved Algorithm v Basic Algorithm')
    plt.legend()
    plt.show()

improvedPlot()