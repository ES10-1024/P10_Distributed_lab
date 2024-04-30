import socket
import numpy as np
import time
from functions import ADMM_optimiser_WDN
from constants import c_general
from SSSS import SSSS
from logging import logging 



tower_IP = '192.168.100.32'
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
#Name of fil for logging
filename='main_tower'
#Setting up logging: 
log=logging(filename) 

#Loading in the classe, 125=iterations, 10=iterations with changing rho, 1=stakeholder number
optimiser = ADMM_optimiser_WDN(conn_pump1, conn_pump2,125, 10, 1,log)
#setting time since last sample if 0, used determining input now, if time.time() waits the sample time
last_sample_time = 0 #time.time() #unix time 
#Setting the hour we start working with
hour = 1

#secret=np.ones((48,1))*2.5 
#ssss_instance = SSSS(conn1=conn_pump1, conn2=conn_pump2,stakeholder=1)
#summedSecret=ssss_instance.DoSSSS(secret) 
#print(summedSecret)

#time.sleep(1000)



while True:
        #Determine the time to next sample, and sleeping if time remains
        sleep_time = last_sample_time + c_general["t_s"] - time.time()
        if sleep_time>0:  
                time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 
        #Perform high level control
        water_level = 300
        U=optimiser.optimise(hour, water_level)
        print(U)
        #Another hour has gone by
        hour=hour+1 


