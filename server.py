import socket
import threading
from pubsub import pub
import pickle


class AuctionServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 12345))  # Bind to 0.0.0.0
        self.server.listen()  # Start listening for connections
        self.clients = []  # Define the clients attribute here

        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self):
        print("Server is ready to accept clients")  # Add this line
        while True:
            try:
                client, _ = self.server.accept()
                print("Accepted a new client")  # Add this line
                self.clients.append(client)
                threading.Thread(target=self.handle_client, args=(client,)).start()
            except Exception as e:  # Modify this line
                print(f"An exception occurred: {e}")  # Add this line

    def broadcast(self, message, sender):
        print(f"Broadcasting message: {message}")
        for client in self.clients:
            if client != sender:  # Don't send the message to the sender
                client.send(message.encode())

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    break  # Break the loop if no data is received
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
            except:
                self.clients.remove(client)
                client.close()
                break

    def get_users(self):
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
        for client in self.clients:
            client.close()
        self.server.close()
        print("Server has stopped")


if __name__ == "__main__":
    server = AuctionServer()
