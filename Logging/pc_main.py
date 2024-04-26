import socket
import struct

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a port
server_address = ('localhost', 9999)
sock.bind(server_address)

while True:
    # Receive message
    print('Waiting to receive message...')
    data, address = sock.recvfrom(4096)
    print('Received {} bytes from {}'.format(len(data), address))
    print(struct.unpack('if',data))
