#Server
import socket
import time

HOST = "127.0.0.1"  #Own IP 
PORT = 6644         #Port to listen on (non-privileged ports are > 1023)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #Setup TCP socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #If port is in use, steal the port
s.bind((HOST, PORT))            #Bind to port
s.listen()                      #Start listening for incoming connections
conn, addr = s.accept()         #Accept connection
print("Connected by", addr)

while True:
    data = conn.recv(1024) #Receive up to the specified amount of bytes
    print(data)
    conn.sendall(data)
    
            
