import customtkinter as ctk
import register_screen
import user
import data_save


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master=None, screen=None):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.pack()
        self.sign_up_screen = None
        screen = ctk.CTkFrame(self.master) if screen is None else screen
        self.screen = screen

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

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=10)

        # Sign up
        self.sign_up_button = ctk.CTkButton(self.frame, text="Go to Register", command=self.sign_up)
        self.sign_up_button.pack(padx=10, pady=50)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_ = data_save.get_user(username)  # Retrieve the User object from the database
        print(user_)
        if user_ and user_.username == username and user_.password == password:
            self.destroy()
            screen = self.screen(self.master, user_)
            screen.pack()

        # Here you would add your login logic
        print(f"Username: {username}, Password: {password}")

    def sign_up(self):
        self.destroy()
        self.sign_up_screen = register_screen.RegisterScreen(self.master)
        self.sign_up_screen.pack()


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
