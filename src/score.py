# score.py
import json

class Score:
    def __init__(self):
        self.points = 0
        self.total_lines_cleared = 0
        self.current_level = 1
        self.total_score = 0
        self.combo_flag = 0
        self.combo_counter = 0
        self.max_score = 0
        self.load_high_scores()

    def load_high_scores(self):
        try:
            with open("src/high_scores.json", "r") as file:
                data = json.load(file)

            # Extrae la lista de puntajes del diccionario
            scores_list = data.get("scores", [])

            # Convierte cada elemento a una tupla con nombre y puntaje como enteros
            self.high_scores = [(entry["player"], int(entry["score"])) for entry in scores_list]

        except (json.JSONDecodeError, FileNotFoundError, KeyError, ValueError) as e:
            print(f"Error al cargar puntajes: {e}")
            # Si hay un error al cargar, establece la lista de puntajes en vacío
            self.high_scores = []

    def save_high_scores(self):
        # Ordena los puntajes antes de guardar solo los 10 mejores
        sorted_scores = sorted(self.high_scores, key=lambda x: x[1], reverse=True)
        self.high_scores = sorted_scores[:10]

        # Guarda los puntajes en el archivo
        with open('src/high_scores.json', 'w') as file:
            json.dump({"scores": [{"player": name, "score": score} for name, score in self.high_scores]}, file, indent=2)

    def update_high_scores(self, player_name, player_score):
        # Actualiza la lista de high scores con el nuevo puntaje y nombre del jugador
        for i, (name, score) in enumerate(self.high_scores):
            if player_score > score:
                self.high_scores.insert(i, (player_name, player_score))
                self.high_scores.pop()  # Elimina el último elemento para mantener solo los 10 mejores puntajes
                return True  # Retorna True si se actualizó la lista
        return False  # Retorna False si el puntaje no entra en la lista de high scores


    def update_score(self, completed_lines, move_type, perfect_clear, hard_drop_distance):
        level_multiplier = self.current_level

        if completed_lines == 1:
            if perfect_clear:
                self.points += 800 * level_multiplier
            else:
                self.points += 100 * level_multiplier
        elif completed_lines == 2:
            if perfect_clear:
                self.points += 1200 * level_multiplier
            else:
                self.points += 300 * level_multiplier
        elif completed_lines == 3:
            if perfect_clear:
                self.points += 1800 * level_multiplier
            else:
                self.points += 500 * level_multiplier
        elif completed_lines == 4:
            if perfect_clear:
                self.points += 2000 * level_multiplier
            else:
                self.points += 800 * level_multiplier

        if perfect_clear:
            # Bonus for perfect clear
            self.points += 200 * level_multiplier

        if completed_lines >= 1:
            if self.combo_flag:
                # Combo points
                self.points += 50 * self.combo_counter * level_multiplier
                self.combo_counter += completed_lines
            else:
                self.combo_flag = 1
        else:
            self.combo_flag = 0
            self.combo_counter = 0
        # Additional logic for move types
        if move_type == "Soft Drop":
            self.points += 1
        elif move_type == "Hard Drop":
            # Hard drop points
            self.points += 2 * hard_drop_distance

        self.total_score += self.points
        self.total_lines_cleared += completed_lines

        # Update current level based on total lines cleared
        self.current_level = (self.total_lines_cleared // 10) +1


    def get_score(self):
        return self.points
