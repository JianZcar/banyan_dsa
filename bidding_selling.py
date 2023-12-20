import customtkinter as ctk
from CTkListbox import *
import login_screen


class BiddingSellingScreen(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.pack()
        self.recently_selected = None

        # Frame 1
        self.frame1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame1.grid(row=0, column=0, padx=10, pady=10)

        # Frame 2
        self.frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame2.grid(row=1, column=0, padx=10, pady=10)

        # Sell button
        self.sell_button = ctk.CTkButton(self.frame1, text="Sell", command=self.sell)
        self.sell_button.grid(row=2, column=1, padx=10, pady=10)

        # Items for bid listbox
        self.bid_label = ctk.CTkLabel(self.frame1, text="Items for bid")
        self.bid_label.grid(row=0, column=0, padx=0, pady=0)

        self.bid_lb = CTkListbox(self.frame1, command=self.bid)
        self.bid_lb.grid(row=1, column=0, padx=10, pady=10)

        self.bid_lb.insert(0, "Option 0")
        self.bid_lb.insert(1, "Option 1")
        self.bid_lb.insert(2, "Option 2")
        self.bid_lb.insert(3, "Option 3")
        self.bid_lb.insert(4, "Option 4")
        self.bid_lb.insert(5, "Option 5")
        self.bid_lb.insert(6, "Option 6")
        self.bid_lb.insert(7, "Option 7")
        self.bid_lb.insert("END", "Option 8")

        # Items you are selling listbox
        self.selling_label = ctk.CTkLabel(self.frame1, text="Items you are selling")
        self.selling_label.grid(row=0, column=1, padx=0, pady=0)

        self.selling_lb = CTkListbox(self.frame1, command=self.deselect)
        self.selling_lb.grid(row=1, column=1, padx=10, pady=10)

        self.selling_lb.insert(0, "Option 0")
        self.selling_lb.insert(1, "Option 1")
        self.selling_lb.insert(2, "Option 2")
        self.selling_lb.insert(3, "Option 3")
        self.selling_lb.insert(4, "Option 4")
        self.selling_lb.insert(5, "Option 5")
        self.selling_lb.insert(6, "Option 6")
        self.selling_lb.insert(7, "Option 7")
        self.selling_lb.insert("END", "Option 8")

        # Logout button
        self.logout_button = ctk.CTkButton(self.frame1, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=3, padx=10, pady=10)

    def logout(self):
        self.destroy()
        self.master.login_screen = login_screen.LoginScreen(self.master, BiddingSellingScreen)
        self.master.login_screen.pack()

    def frame2_setup(self, enable_name_entry: bool, name_label_text: str, price_label_text: str):
        self.back()
        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=2, column=0, padx=10)
        # Item name frame
        frame_item = ctk.CTkFrame(self.frame2, fg_color="transparent")
        frame_item.pack(padx=5, pady=5)

        item_name_label = ctk.CTkLabel(frame_item, text=name_label_text)
        item_name_label.grid(row=0, column=0, padx=10, pady=10)
        if enable_name_entry:
            item_name_entry = ctk.CTkEntry(frame_item)
            item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        item_price_label = ctk.CTkLabel(frame_item, text=price_label_text)
        item_price_label.grid(row=1, column=0, padx=10, pady=10)
        item_price_entry = ctk.CTkEntry(frame_item)
        item_price_entry.grid(row=1, column=1, padx=10, pady=10)

        item_accept_button = ctk.CTkButton(self.frame2, text="Accept", command=self.back, width=30)
        item_accept_button.pack(padx=10, pady=15)

        x = ctk.CTkButton(frame_item, text="X", command=self.back, width=30)
        x.grid(row=0, column=2, padx=10, pady=10)

    def back(self):
        self.frame2.destroy()
        self.recently_selected = None

    def sell(self):
        self.frame2_setup(True, "Item Name", "Item Price")

    def bid(self, selected_option):
        self.frame2_setup(False, selected_option, "Bid Price")
        i = self.bid_lb.curselection()
        self.bid_lb.deactivate(i)

    def deselect(self, selected_option):
        print(selected_option)
        i = self.selling_lb.curselection()
        self.selling_lb.deactivate(i)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        width = 780
        height = 420

        self.title("Selling and Bidding")
        self.geometry(f"{width}x{height}")
        self.ctk_theme = "dark"  # Set the theme to dark mode

        self.selling_bidding_screen = BiddingSellingScreen(self)
        self.selling_bidding_screen.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
