import time
import socket
import numpy as np
from functions import ADMM_optimiser_WDN




if __name__ == '__main__':

    #Set up connecion to tower as client
    tower_IP = '192.168.100.32'
    tower_IP = "127.0.0.1"
    port_tower_pump2 = 5401
    s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tower.connect((tower_IP, port_tower_pump2))
    print("Connected to tower")

    #Set up connecion to pump 2 as client
    pump1_IP = '192.168.100.144'
    pump1_IP = "127.0.0.2"
    port_pump1_pump2 = 5402
    s_pump1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump1.connect((pump1_IP,port_pump1_pump2))
    print("Connected to pump 2, all TCP connecttions set up")
    
    optimiser = ADMM_optimiser_WDN(s_tower, s_pump1,150, 10, 3)

    while True:
            #Perform high level control
            stakeholder = 1
            water_level = 200
            U=optimiser.optimise(stakeholder, water_level)
            print(U)
            time.sleep(0.1)
