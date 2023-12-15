# tetris.py
import pygame
import random
from src.configuraciones import WIDTH, HEIGHT, CONTROLS

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * 10 for _ in range(20)]  # Cuadrícula 10x20
        self.current_block = self.generate_block()
        self.current_block_x = 0  # Posición en el eje x
        self.current_block_y = 0  # Posición en el eje y
        self.key_pressed = {}  # Diccionario para rastrear las teclas presionadas

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
        self.draw_grid(window)
        self.draw_block(window, self.current_block)

    def draw_grid(self, window):
        block_size = self.width // 10
        for row in range(20):
            for col in range(10):
                if self.grid[row][col]:
                    pygame.draw.rect(window, (0, 128, 255), (col * block_size, row * block_size, block_size, block_size), 0)

    def draw_block(self, window, block):
        block_size = self.width // 10
        for row in range(len(block)):
            for col in range(len(block[0])):
                if block[row][col]:
                    x = col + self.current_block_x
                    y = row + self.current_block_y
                    if 0 <= x < 10 and 0 <= y < 20:
                        pygame.draw.rect(window, (255, 0, 0), (x * block_size, y * block_size, block_size, block_size), 0)

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