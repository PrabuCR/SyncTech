import socket
import threading
import sqlite3

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}
        self.rooms = {}

    def broadcast(self, message, room):
        for client in self.rooms[room]:
            client.send(message)

    def handle_client(self, client, username, room):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message, room)
                self.save_message(room, username, message.decode())
            except:
                self.rooms[room].remove(client)
                client.close()
                break

    def save_message(self, room, username, message):
        conn = sqlite3.connect('chat_app.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (room, username, message) VALUES (?, ?, ?)", (room, username, message))
        conn.commit()
        conn.close()

    def run(self):
        print("Server running...")
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {addr}")
            client.send("USERNAME".encode())
            username = client.recv(1024).decode()
            client.send("ROOM".encode())
            room = client.recv(1024).decode()

            if room not in self.rooms:
                self.rooms[room] = []

            self.rooms[room].append(client)
            thread = threading.Thread(target=self.handle_client, args=(client, username, room))
            thread.start()

def setup_database():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room TEXT NOT NULL,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

setup_database()
server = ChatServer()
server.run()
