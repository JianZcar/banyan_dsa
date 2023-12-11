import tkinter as tk
import customtkinter as ct


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        width = 780
        height = 420

        self.title("Client")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode


if __name__ == "__main__":
    app = App()
    app.mainloop()

