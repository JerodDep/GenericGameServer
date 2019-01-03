"""
@File: ClientMain.py

@author: Jerod D'Epifanio

File to handle the main process of the client game
"""


import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 25565
BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))


def SendMessage(message):
    sock.send(message.encode())
    
while True:
    x = input()
    SendMessage(x)
    if x == "q":
        sock.close()
        break;