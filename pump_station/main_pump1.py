import time
import socket
import multiprocessing
from pyModbusTCP.client import ModbusClient
from low_level_settings import settings_pump1
import low_level_controller



if __name__ == '__main__':

    try:
        refence_queue = multiprocessing.Queue(1)
        low_level_control_process = multiprocessing.Process(target = low_level_controller,args = (settings_pump1,refence_queue))
        low_level_control_process.start()
        refence_queue.put(0)
        print("Low level controller started")

        tower_IP = '192.168.100.34'
        port_tower_pump1 = 5401
        s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tower.connect((tower_IP, port_tower_pump1))
        print("Connected to tower")
        
        while True:
            #Perform high level control
            print("High level hi")
            time.sleep(5)
            refence_queue.put(i)
            i=i+0.1
            
    except KeyboardInterrupt:
        s_tower.close()

