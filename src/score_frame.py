#score_frame.py
import tkinter as tk
from tkinter import ttk
from src.score import Score

class ScoreFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.score = Score()
        self.create_widgets()

    def create_widgets(self):
        tree = ttk.Treeview(self, columns=("Player", "Score"), show="headings", height=10)
        tree.heading("Player", text="Player")
        tree.heading("Score", text="Score")

        for player, score in self.score.high_scores:
            tree.insert("", "end", values=(player, score))

        tree.pack(expand=True, fill="both")

