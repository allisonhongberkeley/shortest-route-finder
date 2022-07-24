import helper.config as config
import pygame

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
        pygame.draw.rect(config.screen, self.color, rectangle, (config.width // 2) - 1)

    def draw_and_act(self, func, screen):
        func()
        self.draw(config.screen)
    
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
                neighbor_node = config.game_grid[i][j]
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