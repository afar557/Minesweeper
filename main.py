import random
import pygame
from time import time
from collections import deque
from generateMine import generateMinesGrid
from visualizeBoard import visualizeBoard
from basicagent import basicAgent, finalScore

def main():

    dimension = 5
    mines = 3
    grid = generateMinesGrid(dimension, mines)
    usergrid = basicAgent(grid)
    visualizeBoard(usergrid, "final basic agent")
    visualizeBoard(grid, "actual grid")
    score = finalScore(grid, usergrid)
    print("Final Score is: ", score, " out of: ",mines)
    
    
if __name__ == "__main__":
    main()