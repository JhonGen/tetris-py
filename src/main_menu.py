# main_menu.py
import sys
import pygame
import tkinter as tk
from src.controls_frame import ControlsFrame
from src.tetris import Tetris
from src.sound_manager import SoundManager

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Main Menu')
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        
    def show_menu(self):
        self.sound_manager.play_menu_music()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if 300 < event.pos[0] < 500 and 200 < event.pos[1] < 300:
                            self.sound_manager.stop_music()
                            self.start_game()
                        elif 300 < event.pos[0] < 500 and 400 < event.pos[1] < 500:
                            self.show_controls()
                        elif 275 < event.pos[0] < 525 and 500 < event.pos[1] < 600:
                            self.exit_game()  # Llama a la función exit_game al presionar el botón "Exit"

            self.screen.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def show_controls(self):
        controls_window = tk.Tk()
        controls_window.title("Keypad")  # Cambia el título de la ventana emergente
        controls_frame = ControlsFrame(controls_window)
        controls_frame.pack()
        controls_window.mainloop()

    def draw_menu(self):
        font = pygame.font.Font("src/fonts/Tetris.ttf", 74)
        title_font = pygame.font.Font("src/fonts/tetris-block-regular.ttf", 74)

        text_surface = title_font.render("TETRIS", True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 50))  # Ajusta la posición del título

        # Incrementa el ancho de los botones horizontalmente
        button_width, button_height = 375, 100

        # Botón "Play"
        play_button = pygame.Rect(200, 200, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 255, 0), play_button)
        pygame.draw.rect(self.screen, (0, 200, 0), play_button, border_radius=15)  # Bordes redondeados

        play_text = font.render("Play", True, (0, 0, 0))
        self.screen.blit(play_text, (play_button.x + 60, play_button.y + 35))

        # Botón "Controls"
        controls_button = pygame.Rect(200, 350, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 255, 0), controls_button)
        pygame.draw.rect(self.screen, (0, 200, 0), controls_button, border_radius=15)  # Bordes redondeados

        controls_text = font.render("Keypad", True, (0, 0, 0))
        self.screen.blit(controls_text, (controls_button.x + 25, controls_button.y + 35))

        # Botón "Exit"
        exit_button = pygame.Rect(200, 500, button_width, button_height)
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        pygame.draw.rect(self.screen, (200, 0, 0), exit_button, border_radius=15)  # Bordes redondeados

        exit_text = font.render("Exit", True, (0, 0, 0))
        self.screen.blit(exit_text, (exit_button.x + 60, exit_button.y + 35))


    def start_game(self):
        pygame.mixer.quit()
        tetris_game = Tetris()
        tetris_game.run()
    
    def exit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.show_menu()
