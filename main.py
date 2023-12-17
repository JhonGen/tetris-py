# main.py
import pygame
from src.tetris import Tetris

pygame.init()

if __name__ == "__main__":
    tetris_game = Tetris()
    tetris_game.run()
