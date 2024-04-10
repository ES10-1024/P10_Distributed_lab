import socket
#Client

tcp_ip = '0.0.0.1'
tcp_port = 51451


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #Creating tcp socket
s.bind((tcp_ip,tcp_port))
print("Binded")
s.connect((tcp_ip,tcp_port))
print("Connected")
s.sendall(b"10")
print("Data sendt")
data = s.recv(1024)
print("Data recived")
print(data)
s.close()
print("Closed")