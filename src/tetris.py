# tetris.py
import pygame
import random
import sys
from src.tetromino import Tetromino, I_piece, O_piece, T_piece, Z_piece, J_piece, L_piece, S_piece
from src.score import Score
from src.settings import CONTROLS

class Tetris:
    def __init__(self):
        self.controls = CONTROLS
        self.grid = [[0] * 10 for _ in range(20)]
        self.current_piece = self._generate_random_piece()
        self.clock = pygame.time.Clock()
        self.FALL_SPEED = 500
        pygame.time.set_timer(pygame.USEREVENT + 1, self.FALL_SPEED)
        self.score = Score()
        self.hard_drop_distance = 0
        self.next_piece = self._generate_random_piece()
        self.border_size = 2
        self.game_over_flag = False



    def _generate_random_piece(self):
        pieces = [O_piece, I_piece, T_piece, Z_piece, J_piece, L_piece, S_piece]
        piece_class = random.choice(pieces)
        shape = piece_class.shape
        color = piece_class.color
        return Tetromino(shape=shape, color=color, position=(3, 0))

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

        # Dibujar la siguiente pieza
        next_piece_surface = pygame.Surface((6 * cell_size, 6 * cell_size))  # Ajusta el tamaño del cuadro

        # Dibuja un borde alrededor del área de la pieza siguiente
        pygame.draw.rect(screen, (255, 255, 255), (500 - self.border_size, 250 - self.border_size, 6 * cell_size + 2 * self.border_size, 6 * cell_size + 2 * self.border_size), self.border_size)

        next_piece_x = 500 + (3 * cell_size) - (self.next_piece.width * cell_size // 2 if hasattr(self.next_piece, 'width') else len(self.next_piece.shape[0]) * cell_size // 2)  # Centra la pieza en el cuadro
        next_piece_y = 250 + (3 * cell_size) - (self.next_piece.height * cell_size // 2 if hasattr(self.next_piece, 'height') else len(self.next_piece.shape) * cell_size // 2)

        for row_offset, row in enumerate(self.next_piece.shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(next_piece_surface, self.next_piece.color, (col_offset * cell_size, row_offset * cell_size, cell_size, cell_size))

        screen.blit(next_piece_surface, (next_piece_x, next_piece_y))

        # Mostrar información del score, nivel, combo y total de líneas completadas en la pantalla
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score.total_score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.score.current_level}", True, (255, 255, 255))
        combo_text = font.render(f"Combo: {self.score.combo_counter}", True, (255, 255, 255))
        lines_text = font.render(f"Lines: {self.score.total_lines_cleared}", True, (255, 255, 255))

        screen.blit(score_text, (500, 50))
        screen.blit(level_text, (500, 100))
        screen.blit(combo_text, (500, 150))
        screen.blit(lines_text, (500, 200))

        if self.game_over_flag:
            self._draw_game_over(screen)

    def _draw_game_over(self, screen):
        font_large = pygame.font.Font(None, 74)
        font_small = pygame.font.Font(None, 36)

        text_large = font_large.render("Game Over", True, (255, 255, 255))
        text_small1 = font_small.render("Press 'R' to restart", True, (255, 255, 255))
        text_small2 = font_small.render("Press 'ESC' to exit", True, (255, 255, 255))

        screen.blit(text_large, (200, 250))
        screen.blit(text_small1, (250, 350))
        screen.blit(text_small2, (250, 400))

    def game_over(self):
        self.game_over_flag = True


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

        print(f"Move type: {move_type}")
        print(f"Hard drop distance: {self.hard_drop_distance}")
        print(f"Lines cleared: {completed_lines}")

        self.current_piece = self.next_piece  # Asigna la siguiente pieza como la pieza actual
        self.next_piece = self._generate_random_piece()  # Genera una nueva pieza siguiente


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
        print(f"hard_drop_distance obtenida: {self.hard_drop_distance}")

        # Asegura que la pieza se coloque correctamente después del "Hard Drop"
        self._handle_piece_landing("Hard Drop")

    def _calculate_hard_drop_distance(self):
        # Calcular la distancia de la caída al realizar un "Hard Drop"
        initial_row = self.current_piece.position[1]
        final_row = self.current_piece.get_previous_position()[1]
        return final_row - initial_row
        
    def handle_input(self):
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
                elif event.type == pygame.KEYDOWN:
                    if self.game_over_flag:
                        if event.key == self.controls['restart']:
                            # Reiniciar el juego al presionar 'R' en la pantalla de Game Over
                            self.__init__()
                            self.game_over_flag = False
                        elif event.key == self.controls['exit']:
                            # Salir del juego si se presiona 'ESC' en la pantalla de Game Over
                            pygame.quit()
                            sys.exit()

            self.handle_input()

            screen.fill((0, 0, 0))  # Limpia la pantalla antes de dibujar

            if not self.game_over_flag:
                self._draw_grid(screen)
            else:
                self._draw_game_over(screen)

            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    tetris_game = Tetris()
    tetris_game.run()