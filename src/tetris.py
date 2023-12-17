# tetris.py
import pygame
import random
from src.tetromino import Tetromino, I_piece, O_piece
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


    def _generate_random_piece(self):
        pieces = [O_piece, I_piece]
        piece_class = random.choice(pieces)
        shape = piece_class.shape
        color = piece_class.color
        return Tetromino(shape=shape, color=color, position=(3, 0))

    def _draw_grid(self, screen):
        cell_size = 30
        for row in range(20):
            for col in range(10):
                pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size, cell_size), 1)
                if self.grid[row][col] != 0:
                    pygame.draw.rect(screen, self.grid[row][col], (col * cell_size + 1, row * cell_size + 1, cell_size - 2, cell_size - 2))

        # Dibujar la pieza actual
        screen.blit(self.current_piece.surface, (self.current_piece.position[0] * cell_size, self.current_piece.position[1] * cell_size))

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

        if move_type == "Hard Drop":
            self.hard_drop_distance = self._calculate_hard_drop_distance()

        completed_lines = self._clear_lines()
        
        if completed_lines >= 1:
            perfect_clear = self._check_perfect_clear()
            self.score.update_score(completed_lines, move_type, perfect_clear, self.hard_drop_distance)
        else:
            self.score.update_score(completed_lines, move_type,  0, self.hard_drop_distance)
        
        self.current_piece = self._generate_random_piece()

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

        # Actualiza la posición de la pieza antes de llamar a _piece_lands
        self.current_piece.position = original_position

        self._piece_lands("Hard Drop")

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
            self.current_piece.rotate_counterclockwise()
        elif keys[self.controls['hold']]:
            self.hold()
        
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

            screen.fill((0, 0, 0))
            self._draw_grid(screen)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    tetris_game = Tetris()
    tetris_game.run()