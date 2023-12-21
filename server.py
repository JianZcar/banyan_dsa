import socket
import threading
from pubsub import pub
import customtkinter as ctk
from CTkListbox import *
import pickle


class ServerGUI(ctk.CTk):
    def __init__(self, server_):
        super().__init__()
        self.server = server_
        self.title("Server")
        self.geometry("500x700")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.time_left = 0

        self.listbox = CTkListbox(self, width=500, height=500)
        self.listbox.pack()

        self.timer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.timer_frame.pack()

        # Timer input
        self.timer_input = ctk.CTkEntry(self.timer_frame)
        self.timer_input.grid(row=1, column=0, padx=10, pady=10)

        # Timer label
        self.timer_label = ctk.CTkLabel(self.timer_frame, text="")
        self.timer_label.grid(row=0, column=1, padx=10, pady=10)

        # Start button
        self.start_button = ctk.CTkButton(self.timer_frame, text="Start Timer", command=self.start_timer)
        self.start_button.grid(row=1, column=1, padx=10, pady=10)

        # Reset button
        self.reset_button = ctk.CTkButton(self.timer_frame, text="Reset Timer", command=self.reset_timer)
        self.reset_button.grid(row=1, column=2, padx=10, pady=10)

    def update_listbox(self, message):
        self.listbox.insert('end', message)

    def start_timer(self):
        self.time_left = int(self.timer_input.get())
        self.update_timer()

    def reset_timer(self):
        self.time_left = 0
        self.timer_label.configure(text="")  # Set the text to an empty string

    def update_timer(self):
        if self.time_left > 0:
            minute, secs = divmod(self.time_left, 60)
            time_format = f"Time left: {'{:02d}:{:02d}'.format(minute, secs)}"
            self.timer_label.configure(text=time_format)  # Use 'configure' instead of 'config'
            self.server.send_time()  # Send the time to all connected clients
            self.time_left -= 1
            self.after(1000, self.update_timer)
        elif self.time_left == 0 and self.timer_label.cget('text') != "":
            self.timer_label.configure(text="Countdown finished!")

    def on_closing(self):
        self.server.stop()
        self.quit()  # Stop the mainloop
        self.destroy()  # Destroy the window


class AuctionServer:
    def __init__(self, gui=None):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 12345))  # Bind to 0.0.0.0
        self.server.listen()  # Start listening for connections
        self.clients = []  # Define the clients attribute here
        self.gui = gui
        self.running = True

        threading.Thread(target=self.accept_clients).start()
        threading.Thread(target=self.send_time).start()

    def accept_clients(self):
        print("Server is ready to accept clients")  # Add this line
        while self.running:
            try:
                client, _ = self.server.accept()
                self.clients.append(client)
                threading.Thread(target=self.handle_client, args=(client,)).start()
            except OSError as e:
                if self.running:
                    print(f"An exception occurred: {e}")  # Add this line
                break

    def broadcast(self, message, sender):
        print(f"Broadcasting message: {message}")
        for client in self.clients:
            if client != sender:  # Don't send the message to the sender
                client.send(message.encode())

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                print(f"Received message: {message}")

                if message == 'get_users':
                    users = self.get_users()  # Get the list of users
                    data = pickle.dumps(users)  # Serialize the list of users
                    client.send(data)  # Send the serialized list of users

                elif message == 'new_user:':
                    data_length = int(client.recv(16).strip())  # Get the length of the data
                    user_data = b""
                    while len(user_data) < data_length:
                        to_read = data_length - len(user_data)
                        user_data += client.recv(4096 if to_read > 4096 else to_read)
                    user_ = pickle.loads(user_data)  # Unpickle the user data
                    self.save_user(user_)  # Save the user data
                elif message.startswith('new_item:'):
                    item = message.split(':', 1)[1]
                    pub.sendMessage('new_item', item=item)
                    self.broadcast(message, client)  # Pass the sender's client socket to the broadcast method
                else:
                    bid = message
                    pub.sendMessage('new_bid', bid=bid)
            except OSError:
                self.clients.remove(client)
                client.close()
                break

    @staticmethod
    def get_users():
        try:
            with open('user.pickle', 'rb') as f:
                users = pickle.load(f)
        except FileNotFoundError:
            users = []
        return users

    def save_user(self, user):
        users = self.get_users()
        users.append(user)
        with open('user.pickle', 'wb') as f:
            pickle.dump(users, f)

    def stop(self):
        self.running = False
        for client in self.clients:
            if client.fileno() != -1:  # Check if the client socket is still open
                client.close()
        if self.server.fileno() != -1:  # Check if the server socket is still open
            self.server.close()
        print("Server has stopped")

    def send_time(self):
        if self.gui is not None:
            time_left = str(self.gui.time_left)
            for client in self.clients:
                client.send(time_left.encode())


if __name__ == "__main__":
    server = AuctionServer()
    app = ServerGUI(server)
    server.gui = app
    app.mainloop()
