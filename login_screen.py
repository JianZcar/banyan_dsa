import customtkinter as ctk


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.pack()

        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(padx=10, pady=10)

        # Username frame
        self.frame_username = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_username.pack(padx=10, pady=10)
        self.username_label = ctk.CTkLabel(self.frame_username, text="Username")
        self.username_label.pack()
        self.username_entry = ctk.CTkEntry(self.frame_username)
        self.username_entry.pack()

        # Password frame
        self.frame_password = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_password.pack(padx=10, pady=10)
        self.password_label = ctk.CTkLabel(self.frame_password, text="Password")
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self.frame_password, show="*")
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self.master, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Here you would add your login logic
        print(f"Username: {username}, Password: {password}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        width = 780
        height = 420

        self.title("Client")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode

        self.login_screen = LoginScreen(self)
        self.login_screen.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
