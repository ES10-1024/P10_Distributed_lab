
"""
Test of tcp networking in smart water infastructure lab at AAU

Author: Lau Lauridsen
"""

import socket
import time
print("Script started")
print("Script started")

HOST = "192.168.100.24"  # Standard loopback interface address (localhost)
PORT = 6644  # Port to listen on (non-privileged ports are > 1023)
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        time.sleep(10)
        print("Awake")
    
s.close()
print("script end")
            
