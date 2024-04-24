import time
import socket
import numpy as np
from functions import ADMM_optimiser_WDN



if __name__ == '__main__':


    #Set up connection to tower as client 
    tower_IP = '192.168.100.32'
    tower_IP = "127.0.0.1"
    port_tower_pump1 = 5400
    s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tower.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_tower.connect((tower_IP, port_tower_pump1))
    print("Connected to tower")

    #Set up connecion to pump 2 as server
    pump1_IP = '192.168.100.144'
    pump1_IP = "127.0.0.2"
    port_pump2 = 5402
    s_pump2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_pump2.bind((pump1_IP, port_pump2))
    s_pump2.listen()
    conn_pump2, addr_pump1 = s_pump2.accept()
    print("Connected to pump 2, all TCP connections setup")


    optimiser = ADMM_optimiser_WDN(s_tower, conn_pump2,150, 10, 2)

    while True:
            #Perform high level control
            stakeholder = 1
            water_level = 200
            U=optimiser.optimise(stakeholder, water_level)
            print(U)
            time.sleep(0.1)

            
            
            




