import random
import pygame
from time import time
from collections import deque
from generateMine import generateMinesGrid
from visualizeBoard import visualizeBoard
from basicagent import basicAgent, finalScore
from improvedAgent import improvedAgent

def main():

    dimension = 20
    mines = 30
    grid = generateMinesGrid(dimension, mines)
    # print(grid)
    # grid = [[2, 'M', 'M', 'M', 'M'], ['M', 3, 4, 5, 'M'], [2, 2, 2, 'M', 2], [2, 'M', 3, 2, 1], ['M', 3, 'M', 1, 0]]
    # grid = [[0, 1, 'M', 1, 0], [1, 2, 2, 1, 0], [3, 'M', 2, 0, 0], ['M', 'M', 3, 2, 2], ['M', 3, 2, 'M', 'M']]
    # usergrid = basicAgent(grid)
    usergrid = improvedAgent(grid)
    visualizeBoard(usergrid, "final basic agent")
    visualizeBoard(grid, "actual grid")
    score = finalScore(grid, usergrid)
    print("Final Score is: ", score, " out of: ",mines)
    
    
if __name__ == "__main__":
    main()