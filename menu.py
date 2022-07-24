from tkinter import UNDERLINE
import pygame
import pygame_menu 
import pygame_menu.utils as util
import util.config as config 
from main import main

pygame.init()
surface = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_WIDTH))

theme = pygame_menu.Theme(
    background_color=config.PINK, 
    title=True, 
    title_background_color=config.LIGHT_PINK,
    title_font_color=config.BLACK, 
    title_close_button_background_color=config.BLACK, 
    border_color=config.RED, 
    border_width=50, 
    widget_font=pygame_menu.font.FONT_OPEN_SANS, 
    widget_font_color=config.BLACK,
    widget_margin=(0, 20))

rules_theme=theme.copy()

theme.widget_border_width=2

menu = pygame_menu.Menu(
    title='', 
    width=config.WINDOW_WIDTH, 
    height=config.WINDOW_WIDTH, 
    mouse_motion_selection=True, 
    mouse_visible=True, 
    theme=theme)

menu_rules = pygame_menu.Menu(
    title='',
    height=config.WINDOW_WIDTH,
    width=config.WINDOW_WIDTH,
    mouse_motion_selection=True,
    theme=rules_theme
)

menu_rules.add.label(
    'instructions',
    font_name=pygame_menu.font.FONT_OPEN_SANS_BOLD
    )
    
menu_rules.add.vertical_margin(20)
text = "set a start point: hover over a grid point and press 's'. \n"
text += "set an end point: hover over a different grid point and press 'e'. \n"
text += "set barriers: hover over any number of grid points and press 'b'. \n"
text += "press 'p' to find the optimal route. \n"
text += "press 'a' to restart."
text_widget = menu_rules.add.label(
    text,
    font_size=20,
)

menu.center_content()

label = menu.add.label(
    'shortest route: visualizer',
    font_size=32,
    background_color=config.LIGHT_PINK,
    margin=(0, 100)
)

menu.add.vertical_margin(20)

start_button = menu.add.button(
    'play',
    main,
    button_id='play'
)

rules_button = menu.add.button(
    'rules', 
    menu_rules,
    button_id='rules'
)
quit_button = menu.add.button(
    'quit',
    pygame.quit,
    button_id="quit"
)

menu.mainloop(surface)
