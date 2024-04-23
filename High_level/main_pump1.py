import time
import socket
import numpy as np



if __name__ == '__main__':


    #Set up connection to tower as client 
    tower_IP = '192.168.100.34'
    port_tower_pump1 = 5460
    s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tower.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_tower.connect((tower_IP, port_tower_pump1))
    print("Connected to tower")

    #Set up connecion to pump 2 as server
    pump1_IP = '192.168.100.144'
    port_pump2 = 5462
    s_pump2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_pump2.bind((pump1_IP, port_pump2))
    s_pump2.listen()
    conn_pump2, addr_pump1 = s_pump2.accept()
    print("Connected to pump 2, all TCP connections setup")


        
    while True:
        #Perform high level control
        print("High level hi")
        for i in range(0,100):
            #Perform some opimisation where result is
            a = np.array([1,2,3])

            #Send the number to other units

            
            




