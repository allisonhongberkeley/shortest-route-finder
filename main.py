import pygame
from pygame.locals import *
from queue import PriorityQueue
import sys
import util.config as config
import time
from objs.button import Button
from util.utils import drawAGrid, click, heuristic, euclidean
from algorithm.a_star_search import a_star_search


def main():
    global clock, set_started, set_ended
    pygame.init() 
    config.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_WIDTH))
    clock = pygame.time.Clock()
    config.screen.fill(config.BACKGROUND_COLOR)
    pygame.display.set_caption("Route Finder: Visualization")
    pygame.display.flip()

    config.game_grid = drawAGrid(); 
    playing = True
    config.start_key, config.end = None, None
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
                    clicked_node.draw_and_act(clicked_node.reset, config.screen)
                elif not set_started and key == 's': 
                    config.start_key = clicked_node
                    clicked_node.draw_and_act(clicked_node.start, config.screen)
                    set_started = True
                elif set_started and clicked_node != config.start_key and not set_ended and key == 'e':
                    config.end = clicked_node 
                    clicked_node.draw_and_act(clicked_node.end, config.screen)
                    set_ended = True
                elif set_started and set_ended and key == 'b':
                    clicked_node.draw_and_act(clicked_node.obstacle, config.screen)
                elif key == 'a':
                    [y.draw_and_act(y.reset, config.screen) for x in config.game_grid for y in x]  
                    set_started, set_ended = False, False       
                if key == 'p':
                    a_star_search()
            if event.type == pygame.QUIT:
                playing = False
            
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()