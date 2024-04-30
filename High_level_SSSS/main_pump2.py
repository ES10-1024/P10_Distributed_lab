import time
import socket
import numpy as np
from functions import ADMM_optimiser_WDN
from constants import c_general
from SSSS import SSSS
from logging import logging 





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
    #File name for logging 
    filename="pump2" 
    #Setting up logging: 
    log=logging(filename) 
    print("Connected to pump 2, all TCP connecttions set up")
    #Loading in the classe, 125=iterations, 10=iterations with changing rho, 3=stakeholder number
    optimiser = ADMM_optimiser_WDN(s_tower, s_pump1,125, 10, 3,log)
    #setting time since last sample if 0, used determining input now, if time.time() waits the sample time
    last_sample_time = 0 #time.time() #unix time 
    #Setting the hour we start working with 
    hour = 1
    
    
    #secret=np.ones((48,1))*(-0.5)
    #ssss_instance = SSSS(conn1=s_tower, conn2=s_pump1,stakeholder=3)
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
