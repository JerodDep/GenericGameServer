"""
@File: ClientMain.py

@author: Jerod D'Epifanio

File to handle the main process of the client game
"""


import socket
import threading


TCP_IP = '127.0.0.1'
TCP_PORT = 25565
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send("test".encode())

def Reciever(sock, e):
    while not e.isSet():
        data = sock.recv(BUFFER_SIZE)
        print ("System: ", data)
    return


def SendMessage(message):
    sock.send(message.encode())
    return
    

# Create threading event
e = threading.Event()

# Start reciver thread
t = threading.Thread(target=Reciever, args=(sock, e,))
t.start()

while True:
    x = input("> ")
    SendMessage(x)
    if x == "exit()":
        sock.close()
        e.set()
        break