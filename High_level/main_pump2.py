import time
import socket




if __name__ == '__main__':

    #Set up connecion to tower as client
    tower_IP = '192.168.100.34'
    port_tower_pump2 = 5461
    s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tower.connect((tower_IP, port_tower_pump2))
    print("Connected to tower")

    #Set up connecion to pump 2 as client
    pump1_IP = '192.168.100.144'
    port_pump1_pump2 = 5462
    s_pump1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_pump1.connect((pump1_IP,port_pump1_pump2))
    print("Connected to pump 2, all TCP connecttions set up")
    
    while True:
        #Perform high level control
        print("High level hi")
        time.sleep(5)
        #refence_queue.put(i)
        