# tetromino.py
import pygame

class Tetromino:
    def __init__(self, shape, color, position=(0, 0)):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.position = position
        self.surface = self._create_surface()
        self.prev_position = position
        self.original_position = position 

    def reset_position(self):
        self.position = self.original_position

    def _create_surface(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        surface = pygame.Surface((cols * 30, rows * 30), pygame.SRCALPHA)
        for row in range(rows):
            for col in range(cols):
                if self.shape[row][col] == 1:
                    pygame.draw.rect(surface, self.color, (col * 30, row * 30, 30, 30))
        return surface

    def draw_tetromino(self):
        cell_size = 30
        block_size = cell_size - 2  # Ajusta según sea necesario
        surface = pygame.Surface((len(self.shape[0]) * cell_size, len(self.shape) * cell_size), pygame.SRCALPHA)

        for row_offset, row in enumerate(self.shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    block_x, block_y = col_offset * cell_size, row_offset * cell_size
                    pygame.draw.rect(surface, self.color, (block_x, block_y, block_size, block_size))
                    
                    # Dibuja líneas negras en los bordes del bloque
                    pygame.draw.line(surface, (0, 0, 0), (block_x, block_y), (block_x + block_size, block_y), 2)
                    pygame.draw.line(surface, (0, 0, 0), (block_x, block_y), (block_x, block_y + block_size), 2)
                    pygame.draw.line(surface, (0, 0, 0), (block_x + block_size, block_y), (block_x + block_size, block_y + block_size), 2)
                    pygame.draw.line(surface, (0, 0, 0), (block_x, block_y + block_size), (block_x + block_size, block_y + block_size), 2)

        return surface

    def rotate_clockwise(self, grid):
        rotated_shape = self._rotate_matrix(self.shape)
        if self._check_collision(grid, offset=(0, 0), new_shape=rotated_shape):
            self.rotation = (self.rotation + 1) % 4
            self.shape = rotated_shape
            self.surface = self._create_surface()

    def rotate_counterclockwise(self, grid):
        rotated_shape = self._rotate_matrix(self.shape, clockwise=False)
        if self._check_collision(grid, offset=(0, 0), new_shape=rotated_shape):
            self.rotation = (self.rotation - 1) % 4
            self.shape = rotated_shape
            self.surface = self._create_surface()

    def _rotate_matrix(self, matrix, clockwise=True):
        if clockwise:
            return [list(row) for row in zip(*reversed(matrix))]
        else:
            return [list(row) for row in reversed(list(zip(*matrix)))]

    def move_left(self, grid):
        # Antes de mover la pieza, guarda la posición actual como previa
        self.prev_position = self.position
        if self._check_collision(grid, offset=(-1, 0)):
            self.position = (self.position[0] - 1, self.position[1])

    def move_right(self, grid):
        # Antes de mover la pieza, guarda la posición actual como previa
        self.prev_position = self.position
        if self._check_collision(grid, offset=(1, 0)):
            self.position = (self.position[0] + 1, self.position[1])

    def move_down(self, grid):
        # Antes de mover la pieza, guarda la posición actual como previa
        self.prev_position = self.position
        if self._check_collision(grid, offset=(0, 1)):
            self.position = (self.position[0], self.position[1] + 1)
            return True
        else:
            return False

    def get_previous_position(self):
        # Retorna la posición anterior de la pieza
        return self.prev_position


    def _check_collision(self, grid, offset=(0, 0), new_shape=None):
        if new_shape is None:
            new_shape = self.shape
        for row_offset, row in enumerate(new_shape):
            for col_offset, cell in enumerate(row):
                if cell:
                    new_row = self.position[1] + row_offset + offset[1]
                    new_col = self.position[0] + col_offset + offset[0]
                    if (
                        new_row >= len(grid) or
                        new_col < 0 or
                        new_col >= len(grid[0]) or
                        (new_row >= 0 and grid[new_row][new_col] != 0)
                    ):
                        return False
        return True

    def get_previous_position(self):
        # Retorna la posición anterior de la pieza
        return self.prev_position
    
# Define las piezas (formas) y colores
I_SHAPE = [[1, 1, 1, 1]]
O_SHAPE = [[1, 1], [1, 1]]
T_SHAPE = [[0, 1, 0], [1, 1, 1]]
S_SHAPE = [[0, 1, 1], [1, 1, 0]]
Z_SHAPE = [[1, 1, 0], [0, 1, 1]]
L_SHAPE = [[1, 0, 0], [1, 1, 1]]
J_SHAPE = [[0, 0, 1], [1, 1, 1]]

# Colores en formato RGB
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)

# Crea instancias de Tetromino con las piezas y colores definidos
I_piece = Tetromino(I_SHAPE, LIGHT_BLUE)
O_piece = Tetromino(O_SHAPE, YELLOW)
T_piece = Tetromino(T_SHAPE, MAGENTA)
S_piece = Tetromino(S_SHAPE, GREEN)
Z_piece = Tetromino(Z_SHAPE, RED)
L_piece = Tetromino(L_SHAPE, ORANGE)
J_piece = Tetromino(J_SHAPE, DARK_BLUE)

