# controls_frame.py
import tkinter as tk

class ControlsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        controls_text = (
            "Move Left: Left Arrow\n"
            "Move Right: Right Arrow\n"
            "Move Down: Down Arrow\n"
            "Rotate Clockwise: Up Arrow\n"
            "Rotate Anticlockwise: Z\n"
            "Hard Drop: Space\n"
            "Hold: C\n"
            "Exit: ESC\n"
            "Menu: M\n"
        )

        controls_label = tk.Label(self, text=controls_text, font=("Helvetica", 14))
        controls_label.pack(padx=20, pady=20)
