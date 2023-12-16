# main.py
import pygame
from src.tetris import Tetris
from src.configuraciones import WINDOW_WIDTH, WINDOW_HEIGHT, CONTROLS

pygame.init()

# Configura las dimensiones de la ventana del juego
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

def main():
    clock = pygame.time.Clock()
    
    # Pasa las dimensiones de la ventana al constructor de Tetris
    tetris = Tetris(WINDOW_WIDTH, WINDOW_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        for action, key in CONTROLS.items():
            tetris.key_pressed[action] = keys[key]

        tetris.update()
        tetris.draw(WIN)

        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()
