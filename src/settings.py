# settings.py
import pygame

# Dimensiones de la ventana del juego
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

CONTROLS = {
    'move_left': pygame.K_LEFT,
    'move_right': pygame.K_RIGHT,
    'move_down': pygame.K_DOWN,
    'rotate_clockwise': pygame.K_UP,
    'hard_drop': pygame.K_SPACE,
    'rotate_anticlockwise': pygame.K_z,
    'hold': pygame.K_c,
    'restart': pygame.K_r,
    'exit': pygame.K_ESCAPE,
    'go_to_menu': pygame.K_m
}