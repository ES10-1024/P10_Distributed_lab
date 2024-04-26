import socket
import struct

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
server_address = ('localhost', 9999)

# Send data
message = 52.1
sensor = 10
sent = sock.sendto(struct.pack("if", sensor, message), server_address)


