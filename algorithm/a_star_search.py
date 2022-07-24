import util.config as config
import pygame
from queue import PriorityQueue
from util.utils import drawAGrid, click, heuristic, euclidean


def print_path(node):
    while node.parent is not None:
        node = node.parent
        if node == config.start_key:
            return
        node.path()
        node.draw(config.screen)

def a_star_search():
    queue = PriorityQueue()
    config.start_key.f, config.start_key.g, config.start_key.h = 0, 0, 0
    queue.put((config.start_key.f, config.start_key))
    scores_tracker = {}
    scores_tracker[config.start_key] = [config.start_key.f, config.start_key.g, config.start_key.h]
    visited = []

    while not queue.empty(): #while destination not reached
        node = queue.get()[1]
        node.close()
        #node.draw(screen)
        visited.append(node)
        if (node == config.end):
            print_path(node)
            return
        else:
            neighbors = node.find_neighbors()
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                #create f, g, h values
                neighbor.h = heuristic(neighbor, config.end)
                neighbor.g = node.g + euclidean(neighbor, node)
                neighbor.f = neighbor.g + neighbor.h
                # if neighbor is already in the queue and its g score is > than its current g score, don't update
                if neighbor in scores_tracker and neighbor.g > scores_tracker[neighbor][1]:
                    #figure out how to not update f, g, h here
                    #neighbor.f, neighbor.g, neighbor.h = scores_tracker[neighbor][0], scores_tracker[neighbor][1], scores_tracker[neighbor][2]
                    continue
                neighbor.parent = node            
                scores_tracker[neighbor] = [neighbor.f, neighbor.g, neighbor.h]
                queue.put((neighbor.f, neighbor))
        
    print('destination not found')
    