import socket
import threading
from pubsub import pub


class AuctionServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 12345))  # Bind to 0.0.0.0
        self.server.listen()  # Start listening for connections
        self.clients = [] # Define the clients attribute here

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
                print(f"Received message: {message}")
                if message.startswith('new_item:'):
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


if __name__ == "__main__":
    server = AuctionServer()
