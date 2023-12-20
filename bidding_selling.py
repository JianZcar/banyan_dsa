import customtkinter as ctk
from CTkListbox import *
import login_screen
from pubsub import pub
import socket
import threading


class BiddingSellingScreen(ctk.CTkFrame):
    def __init__(self, master=None, username=None):
        super().__init__(master, fg_color="transparent")
        pub.subscribe(self.update_bid_lb, 'new_item')
        self.username = username
        self.master = master
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
        self.server.connect(('localhost', 12345))
        threading.Thread(target=self.listen_for_messages).start()  # Start a new thread to listen for messages
        self.pack()
        self.recently_selected = None

        # Frame 1
        self.frame1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame1.grid(row=0, column=0, padx=10, pady=10)

        # Frame 2
        self.frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame2.grid(row=1, column=0, padx=10, pady=10)

        self.item_name_entry = None
        self.item_price_entry = None

        # Sell button
        self.sell_button = ctk.CTkButton(self.frame1, text="Sell", command=self.sell)
        self.sell_button.grid(row=2, column=1, padx=10, pady=10)

        # Items for bid listbox
        self.bid_label = ctk.CTkLabel(self.frame1, text="Items for bid")
        self.bid_label.grid(row=0, column=0, padx=0, pady=0)

        self.bid_lb = CTkListbox(self.frame1, command=self.bid)
        self.bid_lb.grid(row=1, column=0, padx=10, pady=10)

        self.bid_lb.insert('end', "Item for bid: Item 1 | 100 | Seller 1")

        # Items you are selling listbox
        self.selling_label = ctk.CTkLabel(self.frame1, text="Items you are selling")
        self.selling_label.grid(row=0, column=1, padx=0, pady=0)

        self.selling_lb = CTkListbox(self.frame1, command=self.deselect)
        self.selling_lb.grid(row=1, column=1, padx=10, pady=10)

        self.selling_lb.insert('end', "Item for bid: Item 1 | 100 | Seller 1")

        # Logout button
        self.logout_button = ctk.CTkButton(self.frame1, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=3, padx=10, pady=10)

    def listen_for_messages(self):
        while True:
            try:
                message = self.server.recv(1024).decode()
                print(f"Received message: {message}")
                if message.startswith('new_item:'):
                    item = message.split(':', 1)[1]
                    pub.sendMessage('new_item', message=f'new_item:{item}')
            except socket.error:
                self.server.close()
                break

    def logout(self):
        self.destroy()
        self.master.login_screen = login_screen.LoginScreen(self.master, BiddingSellingScreen)
        self.master.login_screen.pack()

    def frame2_setup(self, enable_name_entry: bool, name_label_text: str, price_label_text: str, command=None):
        self.back()
        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=2, column=0, padx=10)
        # Item name frame
        frame_item = ctk.CTkFrame(self.frame2, fg_color="transparent")
        frame_item.pack(padx=5, pady=5)

        item_name_label = ctk.CTkLabel(frame_item, text=name_label_text)
        item_name_label.grid(row=0, column=0, padx=10, pady=10)
        if enable_name_entry:
            self.item_name_entry = ctk.CTkEntry(frame_item)
            self.item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        item_price_label = ctk.CTkLabel(frame_item, text=price_label_text)
        item_price_label.grid(row=1, column=0, padx=10, pady=10)
        self.item_price_entry = ctk.CTkEntry(frame_item)
        self.item_price_entry.grid(row=1, column=1, padx=10, pady=10)

        item_accept_button = ctk.CTkButton(self.frame2, text="Accept", command=command, width=30)
        item_accept_button.pack(padx=10, pady=15)

        x = ctk.CTkButton(frame_item, text="X", command=self.back, width=30)
        x.grid(row=0, column=2, padx=10, pady=10)

    def back(self):
        self.frame2.destroy()
        self.recently_selected = None

    def sell(self):
        self.frame2_setup(True, "Item Name", "Item Price",
                          self.avail_to_bidding)

    def bid(self, selected_option):
        self.frame2_setup(False, selected_option, "Bid Price", self.back)
        i = self.bid_lb.curselection()
        self.bid_lb.deactivate(i)

    def avail_to_bidding(self):
        item_name = self.item_name_entry.get()
        item_price = self.item_price_entry.get()
        item_string = f"Item for sale: {item_name} | {item_price} | {self.username}"
        self.selling_lb.insert('end', item_string)
        self.server.send(f'new_item:{item_string}'.encode())  # Modify this line
        pub.sendMessage('new_item', message=f'new_item:{item_string}')  # Add this line
        self.item_name_entry.delete(0, 'end')
        self.item_price_entry.delete(0, 'end')
        self.back()

    def update_bid_lb(self, message):
        print(f"Updating bid listbox with message: {message}")
        if message.startswith('new_item:'):
            item = message.split(':', 1)[1]
            if not (f"{self.username}" in item):
                self.bid_lb.insert('end', item)

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
