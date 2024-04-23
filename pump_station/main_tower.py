import socket

tower_IP = '192.168.100.34'
port_pump1 = 5400
port_pump2 = 5401

try:
    s_pump1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump1.bind((tower_IP, port_pump1))
    s_pump2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump2.bind((tower_IP, port_pump2))
    print("Binded to both pumps")
   
    s_pump1.listen()
    conn_pump1, addr_pump1 = s_pump1.accept()
    print("Connected to pump 1")

    s_pump2.listen()
    conn_pump2, addr_pump2 = s_pump2.accept()
    print("Connected to pump 2, all TCP connections setup")

except KeyboardInterrupt:
    s_pump1.close()
    s_pump2.close()
    print("Connections closed")
    
except:
    s_pump1.close()
    s_pump2.close()
    print("Connections closed")



