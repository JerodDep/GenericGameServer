"""
@File: ServerMain.py

@author: Jerod D'Epifanio

File to handle the main process of the game server
"""

import threading
import socket
import queue
import time


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
@param recieverThreads List of reciever threads
@param e Event to halt thread
"""
def HandleConnection(sock, clients, preParsedList, recieverThreads, e):
    
    while True:
        while not e.isSet():
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
            t = threading.Thread(target=Reciever, args=(client_socket,q,e,))
            t.start()
            
            # Add reciever to list
            recieverThreads.append(t)

            #TODO: remove closed sockets

    return

    

"""
Reciever(sock)

Waits for new messages from client, then adds them to queue

@param sock Client socket to recieve messages from 
@param preParsedQueue queue to add messages to
@param e Event to halt thread
"""
def Reciever(sock, preParsedQueue, e):
    holdQueue = queue.Queue()   # Queue used to hold messages while we are ticking
    isConnected = True          # Used to only run this if the client is connected
    while isConnected:
        while not e.isSet():
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            
            #Check for dropped connection
            if data.decode() == "exit()":
                print ("Client: ", sock.getpeername(), " has disconnected")
                sock.close()
                isConnected = False
                break
            
            # Display message
            print ("Received message:", data.decode(), " | From: ", sock.getpeername())
            
            # Add message to queue
            preParsedQueue.put(data.decode())
        
        while e.isSet():
            # While we are ticking, hold all input and add it 
            # to the preParsedList when we are done
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            
            #Check for dropped connection
            if data.decode() == "exit()":
                print ("Client: ", sock.getpeername(), " has disconnected")
                sock.close()
                isConnected = False
                break
            
            # Display message
            print ("Received message:", data.decode(), " | From: ", sock.getpeername())
            
            # Add message to queue
            holdQueue.put(data.decode())
        
        # Add holdQueue to preParsedQueue
        if holdQueue.qsize() > 0:
            holdQueue.put(None)
            for message in iter(holdQueue.get, None):
                preParsedQueue.put(message)
            with holdQueue.mutex:
                holdQueue.queue.clear()

    return


"""
Tick(commands)

Sends messages to clients that are in the commands queue.
Runs once every ticklength.

@param clients List of client sockets
@param commands List of Queues of commands to send
@param e Event to halt reciever threads
"""
def Tick(clients, commands, e): 
    # Halt handler and reciever threads
    e.set()
    
    # Send out messages
    for commandQueue in commands:
        commandQueue.put(None)
        for command in iter(commandQueue.get, None):
            for client in clients:
                try:
                    client.send(command.encode())
                except socket.error:
                    pass
                    
                
        # Clear queue
        with commandQueue.mutex:
            commandQueue.queue.clear()
    
    # Resume handler and reciever threads
    e.clear()
    
    return
    
    
if __name__ == '__main__':
    
    # Initialize server on socket
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # TCP
    sock.bind((IP, PORT))
    sock.listen(SERVER_SIZE)
    
    # Create threading event
    e = threading.Event()
    
    # Start connection handler
    t = threading.Thread(target=HandleConnection, args=(sock,
                                                        clients,
                                                        preParsedList,
                                                        recieverThreads,
                                                        e,))

    t.start()
    
    # Tick cycle
    while True:
        time.sleep(TICK_LENGTH)
        Tick(clients, preParsedList, e)
    
    # Close server
    sock.close()
    
    
    