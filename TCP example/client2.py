#Client
import socket

import time
import numpy as np
import pickle


HOST = "127.0.0.1"  #Servers IP
PORT = 6644         #Servers port

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Setup TCP socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #If port is in use, steal the port
s.connect((HOST, PORT))     #Connect to server


while True:
    a= np.array([5,7,9])    #Data to send
    s.sendall(a.tobytes())  #Pack data to bytes
    print("Message sent")
    retuned_data = s.recv(1024)
    print(retuned_data)
    returned_message = np.frombuffer(retuned_data, dtype=a.dtype)   #Unpack data
    
    print("Received",returned_message)
    time.sleep(60)