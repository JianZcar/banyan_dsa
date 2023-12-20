import customtkinter as ct
import login_screen
import bidding_selling


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        width = 780
        height = 420

        self.title("Client")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode

        # Login screen
        self.login_screen = login_screen.LoginScreen(self, bidding_selling.BiddingSellingScreen)
        self.login_screen.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
