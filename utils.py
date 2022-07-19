import pygame
import config
from a_node import Node
from math import sqrt

def drawAGrid():
    # here, initiate all the nodes and draw Nodes 
    # create 2D array grid of nodes
    grid = [[None] * config.TOTAL_COLS for i in range(config.TOTAL_ROWS)]
    for x in range(config.TOTAL_ROWS):
        for y in range(config.TOTAL_COLS):
            node = Node(x, y, config.width)
            grid[x][y] = node
            node.draw(config.screen)        
    return grid

def heuristic(node_one, node_two):
    x_1, y_1 = node_one.position()
    x_2, y_2 = node_two.position()
    return abs(x_2-x_1) + abs(y_2-y_1)

def euclidean(node_one, node_two):
    x_1, y_1 = node_one.position()
    x_2, y_2 = node_two.position()
    return sqrt(abs(x_1-x_2)**2 + abs(y_1-y_2)**2)

def click(pos): 
    row, col = tuple(coord // config.width for coord in pos)
    clicked = config.game_grid[row][col]
    return clicked