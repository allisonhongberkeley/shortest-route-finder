from math import sqrt
import pygame
from pygame.locals import *
from queue import PriorityQueue
import sys
import config
import time

class Button():
    button_width = 200
    button_height = 100

    def __init__ (self, x, y, color, text):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
    
    def draw(self, screen):
        rect = pygame.Rect((self.x, self.y), (Button.button_width, Button.button_height))
        pygame.draw.rect(screen, self.color, rect, 0, 2)

        font = pygame.font.SysFont('Calibri', 60)
        text= font.render(self.text, False, (0, 0, 0))
        screen.blit(text, (self.x + Button.button_width // 2 - text.get_width() // 2, self.y + Button.button_height // 2 - text.get_height() // 2))


def main():
    global screen, clock, game_grid, start_key, end, set_started, set_ended
    pygame.init() 
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_WIDTH))
    clock = pygame.time.Clock()
    screen.fill(config.BACKGROUND_COLOR)
    pygame.display.set_caption("Shortest Path Finding: Visualization")
    pygame.display.flip() 
    game_grid = drawAGrid(); 
    reset_button = Button(10, 10, config.TAN, 'reset')
    reset_button.draw(screen)

    playing = True
    start_key, end_key = None, None
    set_started, set_ended = False, False
    while playing: 

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                print(key)
                pos = pygame.mouse.get_pos() 
                clicked_node = click(pos)
                if key == 'r':
                    clicked_node.draw_and_act(clicked_node.reset, screen)
                elif not set_started and key == 's': 
                    start_key = clicked_node
                    clicked_node.draw_and_act(clicked_node.start, screen)
                    set_started = True
                elif set_started and clicked_node != start_key and not set_ended and key == 'e':
                    end = clicked_node 
                    clicked_node.draw_and_act(clicked_node.end, screen)
                    set_ended = True
                elif set_started and set_ended and key == 'b':
                    clicked_node.draw_and_act(clicked_node.obstacle, screen)
                elif key == 'a':
                    [y.draw_and_act(y.reset, screen) for x in game_grid for y in x]  
                    set_started, set_ended = False, False       
                if key == 'p':
                    a_star_search()
            if event.type == pygame.QUIT:
                playing = False
            
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

def drawAGrid():
    # here, initiate all the nodes and draw Nodes 
    # create 2D array grid of nodes
    grid = [[None] * config.TOTAL_COLS for i in range(config.TOTAL_ROWS)]
    for x in range(config.TOTAL_ROWS):
        for y in range(config.TOTAL_COLS):
            node = Node(x, y, config.width)
            grid[x][y] = node
            node.draw(screen)        
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
    clicked = game_grid[row][col]
    return clicked

def print_path(node):
    node.path()
    node.draw(screen)
    while node.parent is not None:
        node = node.parent
        node.path()
        node.draw(screen)

def a_star_search():
    queue = PriorityQueue()
    start_key.f, start_key.g, start_key.h = 0, 0, 0
    queue.put((start_key.f, start_key))
    scores_tracker = {}
    scores_tracker[start_key] = [start_key.f, start_key.g, start_key.h]
    visited = []

    while not queue.empty(): #while destination not reached
        node = queue.get()[1]
        node.close()
        #node.draw(screen)
        visited.append(node)
        if (node == end):
            print_path(node)
            return
        else:
            neighbors = node.find_neighbors()
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                #create f, g, h values
                neighbor.h = heuristic(neighbor, end)
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


class Node:
    def __init__(self, row, column, width):
        self.width = width
        self.column = column
        self.row = row
        self.x_coordinate = row * width
        self.y_coordinate = column * width
        self.color = config.WHITE
        # white -> empty, black -> obstacle, purple -> visited, blue -> path, green -> start node, red -> end
        self.neighbors = []
        self.parent = None
        self.f, self.g, self.h = float('inf'), float('inf'), float('inf')

    def position(self):
        return (self.row, self.column)
    
    def coordinates(self):
        return self.x_coordinate, self.y_coordinate

    def is_visited(self):
        return self.color == config.PURPLE
    
    def is_obstacle(self):
        return self.color == config.BLACK
    
    def is_start(self):
        return self.color == config.GREEN
    
    def is_end(self):
        return self.color == config.RED
    
    def reset(self):
        self.f, self.g, self.h = float('inf'), float('inf'), float('inf')
        self.neighbors = []
        self.parent = None
        self.color = config.WHITE
    
    def close(self):
        self.color = config.PURPLE
    
    def start(self):
        self.color = config.GREEN
    
    def obstacle(self):
        self.color = config.BLACK
    
    def end(self):
        self.color = config.RED
    
    def path(self):
        self.color = config.BLUE

    def draw(self, screen):
        rectangle = pygame.Rect(self.coordinates(), (self.width, self.width))
        pygame.draw.rect(screen, self.color, rectangle, (config.width // 2) - 1)

    def draw_and_act(self, func, screen):
        func()
        self.draw(screen)
    
    def find_neighbors(self):
        row, col = self.position()
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                print(i, j)
                # if it's outside the game boundaries
                if (i == row and j == col) or (i < 0) or (j < 0) or (i >= config.TOTAL_ROWS) or (j >= config.TOTAL_COLS):
                    continue
                # if it's a diagonal neighbor, don't add it
                elif (i == row - 1 and j == col - 1) or (i == row - 1 and j == col + 1) or (i == row + 1 and j == col - 1) or (i == row + 1 and j == col + 1):
                    continue
                # if it's an obstacle, don't add it
                neighbor_node = game_grid[i][j]
                if neighbor_node.is_obstacle() or neighbor_node.is_visited():
                    continue
                else:
                    self.neighbors.append(neighbor_node)
        return self.neighbors

    def __lt__(self, other):
        return self.f <= other.f 
    
    def __eq__(self, other):
        return self.position() == other.position()
    
    def __hash__(self):
        return hash(str(self.position()))

if __name__ == "__main__":
    main()