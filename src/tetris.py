# tetris.py
import pygame
import random
from src.configuraciones import WINDOW_WIDTH, WINDOW_HEIGHT, CONTROLS

class Tetris:
    def __init__(self, window_width, window_height):
        self.width = 10  # Ancho de la grilla
        self.height = 20  # Altura de la grilla
        self.block_size = min(window_width // self.width, window_height // self.height)  # Tamaño del bloque
        self.grid = [[0] * self.width for _ in range(self.height)]  # Cuadrícula 10x20
        self.current_block = self.generate_block()
        self.current_block_x = 0  # Posición en el eje x
        self.current_block_y = 0  # Posición en el eje y
        self.key_pressed = {}  # Diccionario para rastrear las teclas presionadas
        self.level = 1
        self.score = 0
        self.lines = 0

        # Calcula la posición de la grilla en el centro de la ventana
        self.grid_x = (window_width - self.width * self.block_size) // 2
        self.grid_y = (window_height - self.height * self.block_size) // 2

    def generate_block(self):
        # Implementa la lógica para generar bloques aleatorios
        block_types = [
            [[1, 1, 1, 1]],  # Linea
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1], [1, 1]],  # Cuadrado
        ]
        block = random.choice(block_types)
        return block

    def check_collision(self):
        for row in range(len(self.current_block)):
            for col in range(len(self.current_block[0])):
                if self.current_block[row][col]:
                    x = col + self.current_block_x
                    y = row + self.current_block_y
                    if not (0 <= x < 10 and 0 <= y < 20) or (y >= 0 and self.grid[y][x]):
                        return True
        return False

    def place_block(self):
        for row in range(len(self.current_block)):
            for col in range(len(self.current_block[0])):
                if self.current_block[row][col]:
                    x = col + self.current_block_x
                    y = row + self.current_block_y
                    if 0 <= y < 20 and 0 <= x < 10:
                        self.grid[y][x] = 1
                    else:
                        print(f"Attempted to place block outside grid at ({x}, {y})")
                        self.current_block_y = min(20 - len(self.current_block), self.current_block_y)

    def update(self):
        self.handle_keys()
        self.current_block_y += 1
        if self.check_collision():
            print("Block landed or collided")
            self.place_block()
            self.clear_lines()
            self.current_block = self.generate_block()
            self.current_block_x = 0
            self.current_block_y = 0

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0] * 10)

    def draw(self, window):
        window.fill((255, 255, 255))
        
        # Dibuja el borde de la grilla
        pygame.draw.rect(window, (0, 0, 0), (self.grid_x - 1, self.grid_y - 1, self.width * self.block_size + 2, self.height * self.block_size + 2), 1)

        # Dibuja la grilla en el centro
        self.draw_grid(window)

        # Dibuja la pieza actual
        self.draw_block(window, self.current_block)

        # Dibuja el borde de la tabla de información
        pygame.draw.rect(window, (0, 0, 0), (self.grid_x + self.width * self.block_size + 19, self.grid_y + 19, 182, 142), 1)

        # Dibuja la información del juego en el costado derecho
        self.draw_info(window)

        # Actualiza la pantalla después de dibujar todo
        pygame.display.update()

    def draw_info(self, window):
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Nivel: {self.level}", True, (0, 0, 0))
        score_text = font.render(f"Puntaje: {self.score}", True, (0, 0, 0))
        lines_text = font.render(f"Líneas: {self.lines}", True, (0, 0, 0))

        # Posición del texto en el costado derecho, ajustado según grid_x y grid_y
        text_x = self.grid_x + self.width * self.block_size + 20
        text_y = self.grid_y + 20

        # Dibuja el borde de la tabla de información
        pygame.draw.rect(window, (0, 0, 0), (text_x - 1, text_y - 1, 184, 142), 1)

        # Dibuja la información en el costado derecho
        window.blit(level_text, (text_x, text_y))
        window.blit(score_text, (text_x, text_y + 40))
        window.blit(lines_text, (text_x, text_y + 80))

    def draw_grid(self, window):
        # Dibuja los bordes exteriores de la grilla
        pygame.draw.rect(window, (0, 0, 0), (self.grid_x - 1, self.grid_y - 1, self.width * self.block_size + 2, self.height * self.block_size + 2), 1)

        # Dibuja la grilla sin bordes en las celdas
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col]:
                    pygame.draw.rect(window, (0, 128, 255), (self.grid_x + col * self.block_size, self.grid_y + row * self.block_size, self.block_size, self.block_size), 0)


    def draw_block(self, window, block):
        for row in range(len(block)):
            for col in range(len(block[0])):
                if block[row][col]:
                    x = self.grid_x + (self.current_block_x + col) * self.block_size
                    y = self.grid_y + (self.current_block_y + row) * self.block_size
                    pygame.draw.rect(window, (255, 0, 0), (x, y, self.block_size, self.block_size), 0)

    def handle_keys(self):
        for action, key in CONTROLS.items():
            if self.key_pressed.get(action, False):
                if action == 'move_left':
                    self.move_left()
                elif action == 'move_right':
                    self.move_right()
                elif action == 'move_down':
                    self.move_down()
                elif action == 'rotate_clockwise':
                    self.rotate_clockwise()
                elif action == 'hard_drop':
                    self.hard_drop()
                elif action == 'rotate_anticlockwise':
                    self.rotate_anticlockwise()
                elif action == 'hold':
                    self.hold()

    def move_left(self):
        self.current_block_x -= 1
        if self.check_collision():
            self.current_block_x += 1

    def move_right(self):
        self.current_block_x += 1
        if self.check_collision():
            self.current_block_x -= 1

    def move_down(self):
        self.current_block_y += 1
        if self.check_collision():
            self.current_block_y -= 1

    def rotate_clockwise(self):
        rotated_block = list(zip(*reversed(self.current_block)))
        if not self.check_collision_with_rotated(rotated_block):
            self.current_block = rotated_block

    def rotate_anticlockwise(self):
        rotated_block = list(zip(*self.current_block[::-1]))
        if not self.check_collision_with_rotated(rotated_block):
            self.current_block = rotated_block

    def check_collision_with_rotated(self, rotated_block):
        for row in range(len(rotated_block)):
            for col in range(len(rotated_block[0])):
                if rotated_block[row][col]:
                    x = col + self.current_block_x
                    y = row + self.current_block_y
                    if not (0 <= x < 10 and 0 <= y < 20) or (y >= 0 and self.grid[y][x]):
                        return True
        return False

    def hard_drop(self):
        while not self.check_collision():
            self.current_block_y += 1
        self.current_block_y -= 1
        self.place_block()  # Coloca la pieza en su posición final
        self.clear_lines()
        self.current_block = self.generate_block()
        self.current_block_x = 0
        self.current_block_y = 0

    def hold(self):
        # Implementa la lógica para retener la pieza
        pass
