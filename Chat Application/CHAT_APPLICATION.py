import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.gui_done = False
        self.running = True

        self.username = None
        self.room = None

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tk.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tk.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tk.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.win, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.login_label = tk.Label(self.win, text="Login", bg="lightgray")
        self.login_label.pack(padx=20, pady=5)

        self.username_label = tk.Label(self.win, text="Username:", bg="lightgray")
        self.username_label.pack(padx=20, pady=5)

        self.username_entry = tk.Entry(self.win)
        self.username_entry.pack(padx=20, pady=5)

        self.room_label = tk.Label(self.win, text="Room:", bg="lightgray")
        self.room_label.pack(padx=20, pady=5)

        self.room_entry = tk.Entry(self.win)
        self.room_entry.pack(padx=20, pady=5)

        self.login_button = tk.Button(self.win, text="Login", command=self.login)
        self.login_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def login(self):
        self.username = self.username_entry.get()
        self.room = self.room_entry.get()
        self.client.send(self.username.encode())
        self.client.send(self.room.encode())
        self.username_entry.config(state='disabled')
        self.room_entry.config(state='disabled')
        self.login_button.config(state='disabled')

    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        self.client.send(message.encode())
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode()
                if self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', message)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("An error occurred!")
                self.client.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.client.close()
        exit(0)

client = ChatClient()
