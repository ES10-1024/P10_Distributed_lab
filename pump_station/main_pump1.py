import time
import socket
import multiprocessing
from pyModbusTCP.client import ModbusClient
from low_level_settings import settings_pump1


def low_level_controller(settings_pump,q):
    #q is queue where new refrence can be put
    print("low level hallow world")
    last_sample_time = time.time() #unix time 
    ref = 0

    MB_flow = ModbusClient(host = settings_pump['ip_pipe'], port = 502, auto_open = True)
    MB_pump = ModbusClient(host = settings_pump['ip_pump'], port = 502, auto_open=True)
    MB_tower = ModbusClient(host = settings_pump['ip_tower'], port = 502, auto_open = True)

    while True:
        sleep_time = last_sample_time + settings_pump['sampletime']  - time.time()
        time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 

        flow = MB_flow.read_input_registers(settings_pump['register_flow_pipe'], 1)[0] #Some unit
        try:
            ref = q.get_nowait() # m^3/h
        except:
            pass

        #print(ref)

        error = ref - flow
        # print(error)
        #Insert PID controller
        pump_precentage = 100

        #Perform supervisory level control and output actuation if ok
        pump_tank_level = MB_pump.read_input_registers(settings_pump['register_pump_tank'], 1)[0]
        tower_tank_level = MB_tower.read_input_registers(settings_pump['register_tower_tank'], 1)[0]

        if(pump_tank_level < settings_pump['pump_tank_min'] or tower_tank_level > settings_pump['consumer_tank_max']):
            MB_pump.write_single_register(settings_pump['register_pump'], 0)     #Turn off pump
            print("Safty level control active")
        else:
            MB_pump.write_single_register(settings_pump['register_pump'], 100*pump_precentage) 


if __name__ == '__main__':

    try:
        #Start low level controller
        refence_queue = multiprocessing.Queue(1)
        refence_queue.put(0)
        low_level_control_process = multiprocessing.Process(target = low_level_controller,args = (settings_pump1,refence_queue,))
        low_level_control_process.start()
        print("Low level controller started")

        #Set up connection to tower as client 
        tower_IP = '192.168.100.34'
        port_tower_pump1 = 5400
        s_tower=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tower.connect((tower_IP, port_tower_pump1))
        print("Connected to tower")

        #Set up connecion to pump 2 as server
        pump1_IP = '192.168.100.144'
        port_pump2 = 5402
        s_pump2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_pump2.bind((pump1_IP, port_pump2))
        s_pump2.listen()
        conn_pump2, addr_pump1 = s_pump2.accept()
        print("Connected to pump 2, all TCP connections setup")


        
        while True:
            #Perform high level control
            i=0
            print("High level hi")
            time.sleep(5)
            refence_queue.put(i)
            
    except KeyboardInterrupt:
        refence_queue.put(0)
        time.sleep(10)
        s_pump2.close()
        print("Connections closed")






