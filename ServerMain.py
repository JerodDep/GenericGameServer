"""
@File: ServerMain.py

@author: Jerod D'Epifanio

File to handle the main process of the game server
"""

import threading
import socket
import queue


# Set constants
IP = "127.0.0.1"
PORT = 25565
TICK_LENGTH = 0.1
SERVER_SIZE = 5

# Other vars
clients = []                # List of client sockets
recieverThreads = []        # List of reciever threads for clients
preParsedList = []          # List of queues that contain client messages
parsedList = queue.Queue()  # Queue of messages to send to client


"""
HandleConnection(sock, clients)

Adds new clients to the client list

@param sock Network server socket to accept new clients from
@param clients List of client sockets to add to
@param preParsedList List of queues to add new client message queues to
"""
def HandleConnection(sock, clients, preParsedList):
    
    # Accept new connections
    client_socket, address = sock.accept()
    
    print ('New client: ', address)
    
    # Send welcome message
    client_socket.send('Welcome!'.encode())

    # Add client to list
    clients.append(client_socket)
    
    # Make new queue for client
    q = queue.Queue()
    
    # Add queue to list
    preParsedList.append(q)
    
    # Start reciever thread for client
    t = threading.Thread(target=Reciever, args=(client_socket,q,))
    t.start()
    t.join()

    

"""
Reciever(sock)

Waits for new messages from client, then adds them to queue

@param sock Client socket to recieve messages from 
@param preParsedQueue queue to add messages to
"""
def Reciever(sock, preParsedQueue):
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        
        print ("Received message:", data.decode())
        
        preParsedQueue.put(data.decode())
        
        # Used to exit reciever thread if necessary
        if "exit" in data.decode():
            sock.close()
            break
    return

            
"""
Parser(commands)

Parses messages sent from clients and prepares responses

@param commands Queue of commands to issue
"""
def Parser(commands):
    return


"""
Tick(commands)

Sends messages to clients that are in the commands queue.
Runs once every ticklength.

@param sock Network socket to send messages on
@param commands List of Queues of commands to send
"""
def Tick(sock, commands): 
    # Halt reciever threads
    
    # Send out messages
    return
    
    
    # TODO: START MAKING TICKS WORK
if __name__ == '__main__':
    
    # Initialize server on socket
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # UDP
    sock.bind((IP, PORT))
    sock.listen(SERVER_SIZE)
    
    
    # Start connection handler
    t = threading.Thread(target=HandleConnection, args=(sock,
                                                        clients,
                                                        preParsedList,))
    t.start()
    t.join()
    
    # Close server
    sock.close()
    
    
    