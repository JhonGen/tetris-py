# tetris.py
import pygame
import random
import sys
from collections import deque

from src.tetromino import Tetromino, I_piece, O_piece, T_piece, Z_piece, J_piece, L_piece, S_piece
from src.score import Score
from src.settings import CONTROLS
from src.sound_manager import SoundManager

class Tetris:
    def __init__(self):
        self.controls = CONTROLS
        self.grid = [[0] * 10 for _ in range(20)]
        self.next_pieces_queue = deque(maxlen=3) 
        self._fill_next_pieces_queue()
        self.current_piece = self.next_pieces_queue.popleft()
        self.next_pieces_queue.append(self._generate_random_piece())
        self.clock = pygame.time.Clock()
        self.FALL_SPEED = 500
        pygame.time.set_timer(pygame.USEREVENT + 1, self.FALL_SPEED)
        self.score = Score()
        self.score.load_high_scores()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Tetris')
        self.hard_drop_distance = 0
        self.border_size = 1
        self.game_over_flag = False
        self.held_piece = None
        self.can_hold = True  # Permite retener solo una vez por turno
        self.frame_counter = 0
        self.last_key_process_time = pygame.time.get_ticks()
        self.sound_manager = SoundManager()
        self.sound_manager.play_tetris_music(loop=True)
        self.game_over_music_played = False
        self.new_high_score_flag = False

    def _generate_random_piece(self):
        pieces = [O_piece, I_piece, T_piece, Z_piece, J_piece, L_piece, S_piece]
        piece_class = random.choice(pieces)
        shape = piece_class.shape
        color = piece_class.color
        return Tetromino(shape=shape, color=color, position=(3, 0))
    
    def _fill_next_pieces_queue(self):
        for _ in range(3):
            self.next_pieces_queue.append(self._generate_random_piece())

    def hold(self):
        if self.can_hold:
            if self.held_piece is None:
                self.held_piece = self.current_piece
                self.current_piece = self.next_pieces_queue.popleft()
                self.next_pieces_queue.append(self._generate_random_piece())
            else:
                # Intercambia la pieza actual con la pieza en espera
                self.current_piece, self.held_piece = self.held_piece, self.current_piece
                self.current_piece.reset_position()  # Reinicia la posición de la pieza actual
            self.can_hold = False  # Evita retener más de una vez por turno
    
    def _draw_grid(self, screen):
        cell_size = 30
        grid_x, grid_y = 0, 0
        grid_width, grid_height = 10 * cell_size, 20 * cell_size

        # Dibuja un borde alrededor del área de la grilla
        pygame.draw.rect(screen, (255, 255, 255), (grid_x - self.border_size, grid_y - self.border_size, grid_width + 2 * self.border_size, grid_height + 2 * self.border_size), self.border_size)

        for row in range(20):
            for col in range(10):
                pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size, cell_size), 1)
                if self.grid[row][col] != 0:
                    pygame.draw.rect(screen, self.grid[row][col], (col * cell_size + 1, row * cell_size + 1, cell_size - 2, cell_size - 2))

        # Dibujar la pieza actual
        screen.blit(self.current_piece.draw_tetromino(), (self.current_piece.position[0] * cell_size, self.current_piece.position[1] * cell_size))

        # Dibujar las tres piezas siguientes
        next_pieces_surface = pygame.Surface((6 * cell_size, 18 * cell_size))  # Ajusta el tamaño del cuadro
        # Añade el título "Next Pieces"
        font = pygame.font.Font(None, 24)
        next_pieces_title = font.render("Next Pieces:", True, (255, 255, 255))
        screen.blit(next_pieces_title, (320, 40))  # Ajusta la posición según sea necesario

        for i, next_piece in enumerate(list(self.next_pieces_queue)[:3]):
            next_piece_x = 320 + (3 * cell_size) - (next_piece.width * cell_size // 2 if hasattr(next_piece, 'width') else len(next_piece.shape[0]) * cell_size // 2)  # Centra la pieza en el cuadro
            next_piece_y = 150 + i * 120 + (3 * cell_size) - (next_piece.height * cell_size // 2 if hasattr(next_piece, 'height') else len(next_piece.shape) * cell_size // 2)

            for row_offset, row in enumerate(next_piece.shape):
                for col_offset, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(next_pieces_surface, next_piece.color, (col_offset * cell_size, (row_offset + i * 4) * cell_size, cell_size, cell_size))

        screen.blit(next_pieces_surface, (320, 70))

        # Dibujar la pieza retenida
        if self.held_piece:
            held_piece_surface = pygame.Surface((6 * cell_size, 6 * cell_size))
            # Añade el título "Held Piece"
            font = pygame.font.Font(None, 24)
            held_piece_title = font.render("Held Piece:", True, (255, 255, 255))
            screen.blit(held_piece_title, (520, 40))  # Ajusta la posición según sea necesario
            # Dibuja un borde alrededor del área de la pieza retenida
            pygame.draw.rect(screen, (255, 255, 255), (540 - self.border_size, 60 - self.border_size, 6 * cell_size + 2 * self.border_size, 6 * cell_size + 2 * self.border_size), self.border_size)

            held_piece_x = 540 + (3 * cell_size) - (self.held_piece.width * cell_size // 2 if hasattr(self.held_piece, 'width') else len(self.held_piece.shape[0]) * cell_size // 2)
            held_piece_y = 70 + (3 * cell_size) - (self.held_piece.height * cell_size // 2 if hasattr(self.held_piece, 'height') else len(self.held_piece.shape) * cell_size // 2)

            for row_offset, row in enumerate(self.held_piece.shape):
                for col_offset, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(held_piece_surface, self.held_piece.color, (col_offset * cell_size, row_offset * cell_size, cell_size, cell_size))

            screen.blit(held_piece_surface, (held_piece_x, held_piece_y))

        # Dibujar la sombra
        shadow_position = self.calculate_hard_drop_position()
        shadow_color = (100, 100, 100)  # Puedes ajustar el color de la sombra según tus preferencias
        for row_offset, row in enumerate(self.current_piece.shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    shadow_x = (shadow_position[0] + col_offset) * cell_size
                    shadow_y = (shadow_position[1] + row_offset) * cell_size
                    pygame.draw.rect(screen, shadow_color, (shadow_x, shadow_y, cell_size, cell_size))

        # Mostrar información del score, nivel, combo y total de líneas completadas en la pantalla
        font = pygame.font.Font(None, 36)
        level_font = pygame.font.Font(None, 50)
        score_text = font.render(f"Score: {self.score.total_score}", True, (255, 255, 255))
        level_text = level_font.render(f"Level: {self.score.current_level}", True, (255, 255, 255))
        combo_text = font.render(f"Combo: {self.score.combo_counter}", True, (255, 255, 255))
        lines_text = font.render(f"Lines: {self.score.total_lines_cleared}", True, (255, 255, 255))
        max_score_text = font.render(f"Max Score: { self.score.max_score}", True, (255,255,255))
        screen.blit(score_text, (500, 400))
        screen.blit(level_text, (500, 350))
        screen.blit(combo_text, (500, 450))
        screen.blit(lines_text, (650, 450))
        screen.blit(max_score_text, (500, 550))

        if self.game_over_flag:
            self._draw_game_over(screen)

    def _draw_game_over(self, screen):
        font_large = pygame.font.Font("src/fonts/tetris-block-regular.ttf", 50)
        font_small = pygame.font.Font("src/fonts/tetris-block-regular.ttf", )

        text_large = font_large.render("Game Over", True, (255, 255, 255))
        text_small1 = font_small.render("Press 'R' to restart", True, (255, 255, 255))
        text_small2 = font_small.render("Press 'ESC' to exit", True, (255, 255, 255))

        screen.blit(text_large, (100, 150))
        screen.blit(text_small1, (150, 300))
        screen.blit(text_small2, (150, 340))
        
        if self.new_high_score_flag:
            self.handle_input_game_over(screen) 
        
    def handle_input_game_over(self, screen):
        input_text = ""
        input_rect = pygame.Rect(400, 350, 200, 50)  # Ajusta la posición del cuadro
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 36)  # Agrega una fuente para el título

        # Agrega el título
        title_text = title_font.render("Enter your name", True, (255, 255, 255))
        screen.blit(title_text, (input_rect.x, input_rect.y - 30))  # Ajusta la posición del título

        text = font.render(input_text, True, color)
        width = max(200, text.get_width() + 10)
        input_rect.w = width

        while self.new_high_score_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Guarda el nuevo récord con el nombre del jugador
                        updated = self.score.update_high_scores(input_text, self.score.total_score)
                        if updated:
                            self.score.save_high_scores()
                        self.new_high_score_flag = False  # Desactiva la flag después de guardar
                        self.go_to_menu()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                    text = font.render(input_text, True, color)
                    width = max(200, text.get_width() + 10)
                    input_rect.w = width

            pygame.draw.rect(screen, color, input_rect, 2)
            screen.blit(text, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()
            self.clock.tick(30)


    def game_over(self):
        if not self.game_over_music_played:
            self.sound_manager.play_game_over_music()
            self.game_over_music_played = True

        # Verificar si el total_score es mayor que algún puntaje en la lista de high scores
        if any(self.score.total_score > score for _, score in self.score.high_scores):
            print("¡Nuevo récord!")
            self.new_high_score_flag = True  # Activa la flag de nuevo récord
            # Puedes realizar acciones adicionales si se supera un récord, si es necesario
        else:
            print("No superaste ningún récord.")


        self.game_over_flag = True

    def go_to_menu(self):
        pygame.mixer.quit()  # Cierra el sistema de mezcla para evitar conflictos con pygame.mixer en MainMenu
        from src.main_menu import MainMenu  # Importa aquí para evitar la dependencia circular
        main_menu = MainMenu()
        main_menu.show_menu()

    def _update_grid(self):
        for row_offset, row in enumerate(self.current_piece.shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    new_row = self.current_piece.position[1] + row_offset
                    new_col = self.current_piece.position[0] + col_offset
                    if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                        self.grid[new_row][new_col] = 0

        for row_offset, row in enumerate(self.current_piece.shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    new_row = self.current_piece.position[1] + row_offset
                    new_col = self.current_piece.position[0] + col_offset
                    if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                        self.grid[new_row][new_col] = self.current_piece.color

    def _handle_piece_landing(self, move_type):
        self._update_grid()
        completed_lines = self._clear_lines()

        if any(cell for cell in self.grid[0]):
            self.game_over()
            return

        if completed_lines >= 1:
            perfect_clear = self._check_perfect_clear()
            self.score.update_score(completed_lines, move_type, perfect_clear, self.hard_drop_distance)
        else:
            self.score.update_score(completed_lines, move_type, 0, self.hard_drop_distance)


        self.current_piece = self.next_pieces_queue.popleft()  # Obtiene la siguiente pieza de la cola
        self.next_pieces_queue.append(self._generate_random_piece())  # Agrega una nueva pieza a la cola
        self.can_hold = True

    def _check_perfect_clear(self):
        return all(all(cell == 0 for cell in row) for row in self.grid)

    def _clear_lines(self):
        completed_lines = [row for row in self.grid if all(cell != 0 for cell in row)]

        for row in completed_lines:
            self.grid.remove(row)
            self.grid.insert(0, [0] * 10)

        return len(completed_lines)
    
    def hard_drop(self):
        original_position = self.current_piece.position

        while self.current_piece.move_down(self.grid):
            pass

        final_position = self.current_piece.position
        self.hard_drop_distance = final_position[1] - original_position[1]
        # Asegura que la pieza se coloque correctamente después del "Hard Drop"
        self._handle_piece_landing("Hard Drop")

    def _calculate_hard_drop_distance(self):
        # Calcular la distancia de la caída al realizar un "Hard Drop"
        initial_row = self.current_piece.position[1]
        final_row = self.current_piece.get_previous_position()[1]
        return final_row - initial_row

    def calculate_hard_drop_position(self):
        original_position = self.current_piece.position
        while self.current_piece.move_down(self.grid):
            pass
        final_position = self.current_piece.position
        self.current_piece.position = original_position  # Restaura la posición original
        return final_position

    def handle_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_key_process_time < 120:  # Ajusta el valor según sea necesario
            return
        
        keys = pygame.key.get_pressed()
        if keys[self.controls['move_left']]:
            self.current_piece.move_left(self.grid)
        elif keys[self.controls['move_right']]:
            self.current_piece.move_right(self.grid)
        elif keys[self.controls['move_down']]:
            if not self.current_piece.move_down(self.grid):
                self._handle_piece_landing("Soft Drop")
        elif keys[self.controls['rotate_clockwise']]:
            self.current_piece.rotate_clockwise(self.grid)
        elif keys[self.controls['hard_drop']]:
            self.hard_drop()
        elif keys[self.controls['rotate_anticlockwise']]:
            self.current_piece.rotate_counterclockwise(self.grid)
        elif keys[self.controls['hold']]:
            self.hold()
        elif keys[self.controls['restart']]:
            # Reiniciar el juego al presionar 'R' en cualquier momento
            self.__init__()
            self.game_over_flag = False
        elif keys[self.controls['exit']]:
            # Salir del juego si se presiona 'ESC'
            pygame.quit()
            sys.exit()
        elif keys[self.controls['go_to_menu']]:  # Agrega la lógica para ir al menú principal
            self.go_to_menu()
        
        self.last_key_process_time = current_time

    def _update_fall_speed(self):
        # Actualiza la velocidad de caída en función del nivel
        level = self.score.current_level
        self.frames_per_drop = int((0.8 - ((level - 1) * 0.007)) ** (level - 1) * 60)  # Asume 60 FPS

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Tetris')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT + 1:
                    if not self.current_piece.move_down(self.grid):
                        self._handle_piece_landing("Soft Drop")

            self.handle_input()

            screen.fill((0, 0, 0))  # Limpia la pantalla antes de dibujar

            if not self.game_over_flag:
                self._draw_grid(screen)
            else:
                self._draw_game_over(screen)

                
            pygame.display.flip()
            self.clock.tick(30)  # Mantiene la velocidad constante

            # Actualiza la velocidad de caída y realiza la caída según el contador de frames
            self._update_fall_speed()
            self.frame_counter += 1
            if self.frame_counter >= self.frames_per_drop:
                self.frame_counter = 0
                if not self.game_over_flag:
                    if not self.current_piece.move_down(self.grid):
                        self._handle_piece_landing("Soft Drop")

        pygame.quit()

if __name__ == "__main__":
    tetris_game = Tetris()
    tetris_game.run()