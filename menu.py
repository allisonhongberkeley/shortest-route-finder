import pygame
import pygame_menu 
import pygame_menu.utils as util
import config 
from main import main

pygame.init()
surface = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_WIDTH))
#class Menu():

theme = pygame_menu.Theme(background_color=config.PINK, title=False, border_color=config.RED, border_width=50,
        widget_font=pygame_menu.font.FONT_OPEN_SANS, widget_font_color=config.BLACK, widget_margin=(0, 20), 
        widget_border_width=2)
menu = pygame_menu.Menu(title='Shortest Route Finder', width=config.WINDOW_WIDTH, height=config.WINDOW_WIDTH, 
        mouse_motion_selection=True, mouse_visible=True, theme=theme)

menu.center_content()

label = menu.add.label(
    'Shortest Path: Visualizer',
    font_size=32,
    background_color=config.LIGHT_PINK,
    margin=(0, 100)
)

start_button = menu.add.button(
    'Play',
    main,
    button_id='play'
)

rules_button = menu.add.button(
    'Rules', 
    button_id='rules'
)
quit_button = menu.add.button(
    'Quit',
    pygame.quit,
    button_id="quit"
)

menu.mainloop(surface)
