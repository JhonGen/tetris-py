# score.py
class Score:
    def __init__(self):
        self.points = 0
        self.total_lines_cleared = 0
        self.current_level = 1
        self.total_score = 0
        self.combo_flag = 0
        self.combo_counter = 0
        self.max_score = 0
        
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

        # Print statements for verification
        print(f"Completed Lines: {completed_lines}")
        print(f"Move Type: {move_type}")
        print(f"Perfect Clear: {perfect_clear}")
        print(f"Hard Drop Distance: {hard_drop_distance}")
        print(f"Level Multiplier: {level_multiplier}")
        print(f"Points: {self.points}")
        print(f"Total Score: {self.total_score}")
        print(f"Total Lines Cleared: {self.total_lines_cleared}")
        print(f"Combo Flag: {self.combo_flag}")
        print(f"Combo Counter: {self.combo_counter}")
        print(f"Current Level: {self.current_level}")
        print("\n")

    def get_score(self):
        return self.points
