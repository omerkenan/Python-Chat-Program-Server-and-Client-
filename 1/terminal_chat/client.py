import sys, socket, json,threading
from threading import Thread

print("hey welcome")

e = threading.Event()

class Client():

    def __init__(self):
        HOST = "127.0.0.1"
        PORT = 32000
        self.LIM = 2048
        self.ADDR = (HOST, PORT)
        self.messages = ""
        a = input("try")
        if a == "start":
            print("do you have and account? if you have write yes, else write no")
            user_stuation = input()
            if user_stuation == "yes":
                self.log_in()
            else:
                self.sign_in()
            while True:
                self.press_enter()

    def log_in(self):
        print("please write your nick name")
        nick = str(input())
        print("please write your password")
        password = str(input())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        Thread(target=self.recieve).start()
        self.client_socket.send(bytes(nick + "," + password, "utf-8"))

    def sign_in(self):
        print("please, pick and write a nick name")
        nick = str(input())
        print("please, pick write a password")
        password = str(input())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        Thread(target=self.recieve).start()
        self.client_socket.send(bytes(nick + "," + password, "utf-8"))

    def press_enter(self):
        msg = str(input())
        self.client_socket.send(bytes(msg, "utf-8"))

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.LIM).decode("utf-8")
                print(msg)
            except OSError:
                break


chat = Client()



