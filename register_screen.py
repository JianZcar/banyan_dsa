import customtkinter as ctk
import login_screen
import bidding_selling
import user
import data_save


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.pack()
        self.login_screen = None

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

        # Password frame 2
        self.frame_password_1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_password_1.pack(padx=10, pady=10)
        self.password_label_1 = ctk.CTkLabel(self.frame_password_1, text="Re-enter Password")
        self.password_label_1.pack()
        self.password_entry_1 = ctk.CTkEntry(self.frame_password_1, show="*")
        self.password_entry_1.pack()

        self.register_button = ctk.CTkButton(self.frame, text="Register", command=self.register_button)
        self.register_button.pack(padx=10, pady=10)

        self.login_button = ctk.CTkButton(self.frame, text="Go to Login", command=self.login_button)
        self.login_button.pack(padx=10, pady=50)

    def register_button(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_1 = self.password_entry_1.get()
        users = data_save.load_users()

        # Here you would add your login logic
        if password != password_1:
            print("Passwords do not match")
        elif any(user_.username == username for user_ in users):
            print("Username already taken")
        else:
            data_save.save_user(user.User(username, password))
            print(f"Username: {username}, Password: {password}")

    def login_button(self):
        self.destroy()
        self.login_screen = login_screen.LoginScreen(self.master, bidding_selling.BiddingSellingScreen)
        self.login_screen.pack()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        width = 780
        height = 420

        self.title("Client")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode

        self.register_screen = RegisterScreen(self)
        self.register_screen.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
