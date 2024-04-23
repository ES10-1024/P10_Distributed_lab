
"""
Test of tcp networking in smart water infastructure lab at AAU

Author: Lau Lauridsen
"""

import socket
import time
print("Script started")

#HOST = "192.168.100.24"  # Its own IP adress
HOST = "127.0.0.1"
PORT = 6644  # Port to listen on (non-privileged ports are > 1023)
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print("Connected by", addr)
conn.settimeout(1) #Maybe connection
while True:
    try: 
        data = conn.recv(1024)
        print(data)
        conn.sendall(data)
    except:
        print("Going to sleep")
        time.sleep(5)
        print("Awake")
    
s.close()
print("script end")
            
