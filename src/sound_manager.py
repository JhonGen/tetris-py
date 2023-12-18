# sound_manager.py

import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.tetris_music = pygame.mixer.Sound("src/music/tetris.mp3")
        self.game_over_music = pygame.mixer.Sound("src/music/game_over.mp3")
        self.tetris_music.set_volume(0.5)  # Ajusta el volumen según sea necesario
        self.game_over_music.set_volume(0.5)  # Ajusta el volumen según sea necesario
        self.game_over_played = False

    def play_tetris_music(self, loop=True):
        pygame.mixer.music.load("src/music/tetris.mp3")
        pygame.mixer.music.play(-1 if loop else 0)

    def play_game_over_music(self):
        pygame.mixer.music.stop()  # Detiene la música de Tetris
        self.game_over_music.play()
        self.game_over_played = True

    def stop_music(self):
        pygame.mixer.music.stop()

    def reset(self):
        self.game_over_played = False