import socket
#Client

tcp_ip = '127.0.0.1'
tcp_port = 51451


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #Creating tcp socket
s.bind((tcp_ip,tcp_port))
print("Binded")
s.listen()
print("listen")
cliet_connection, client_port = s.accept()
print("Accepted")
data = cliet_connection.recv(1024)
print("recived")
print(data)
cliet_connection.sendall(data+1)
print("End")
s.recv(1024)