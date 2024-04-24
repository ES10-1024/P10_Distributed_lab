import socket
import numpy as np
import time
from functions import ADMM_optimiser_WDN


tower_IP = '192.168.100.34'
tower_IP = "127.0.0.1"
port_pump1 = 5400
port_pump2 = 5401


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


optimiser = ADMM_optimiser_WDN(conn_pump1, conn_pump2,150, 10, 1)

while True:
        #Perform high level control
        stakeholder = 1
        water_level = 200
        U=optimiser.optimise(stakeholder, water_level)
        print(U)
        time.sleep(0.1)


