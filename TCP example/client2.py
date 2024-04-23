# echo-client.py

"""
Test of tcp networking in smart water infastructure lab at AAU

Author: Lau Lauridsen
"""

import socket
import struct
import time
import numpy as np

#HOST = "192.168.100.24"  # The server's hostname or IP address
HOST = "127.0.0.1"
PORT = 6644  # The port used by the server
message = 5.2578

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))

"""

while True:
    s.sendall(struct.pack('f',message))
    print("Message sendt")
    data = s.recv(1024)
    returned_message = struct.unpack('f',data)[0]
    
    print("Received",returned_message)
    print(returned_message)
    time.sleep(20)
"""

while True:
    np.array([5,7,9])
    s.sendall(np.tobytes())
    data =0
    data = s.recv(1024)
    returned_message = np.frombuffer(data)
    
    print("Received",returned_message)
    time.sleep(10)