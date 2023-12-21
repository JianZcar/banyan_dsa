import customtkinter as ctk
import login_screen
import bidding_selling


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        width = 1000
        height = 545

        self.title("Client")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode

        # Login screen
        self.login_screen = login_screen.LoginScreen(self, bidding_selling.BiddingSellingScreen)
        self.login_screen.pack()


if __name__ == "__main__":
    app1 = App()
    app1.mainloop()

