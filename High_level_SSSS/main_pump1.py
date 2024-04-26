#import time
import socket
import time
import numpy as np
from functions import ADMM_optimiser_WDN
from constants import c_general
from SSSS import SSSS


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

    #Loading in the classe, 125=iterations, 10=iterations with changing rho, 2=stakeholder number
    optimiser = ADMM_optimiser_WDN(s_tower, conn_pump2,125, 10, 2)
    #setting time since last sample if 0, used determining input now, if time.time() waits the sample time
    last_sample_time =0 #time.time() #unix time 
    #Setting the hour we start working with 
    hour = 1
    
    
    secret=np.ones((48,1))*3.4 
    ssss_instance = SSSS(conn1=s_tower, conn2=conn_pump2,stakeholder=2)
    summedSecret=ssss_instance.DoSSSS(secret)      
    print(summedSecret)

    time.sleep(1000)


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

     

            
            
            




