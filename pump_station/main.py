import time
import multiprocessing
from pyModbusTCP.client import ModbusClient
from low_level_settings import settings_pump1
from multiprocess_test import multiprocess_test


def low_level_controller(settings_pump, q):
    #q is queue where new refrence can be put
    print("low level hallow world")
    last_sample_time = time.time()
    ref = 0

    MB_flow = ModbusClient(host = settings_pump['ip_pipe'], port = 502, auto_open = True)
    MB_pump = ModbusClient(host = settings_pump['ip_pump'], port = 502, auto_open=True)
    MB_tower = ModbusClient(settings_pump['ip_tower'], port = 502, auto_open = True)

    while True:
        sleep_time = last_sample_time + settings_pump['sampletime']  - time.time()
        time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 

        flow = MB_flow.read_input_registers(settings_pump['register_flow_pipe'], 1)[0] #Some unit
        try:
            ref = q.get_nowait() # m^3/h
        except:
            pass

        print(ref)

        error = ref - flow
        print(error)
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
            MB_pump.write_single_register(6, 100*pump_precentage) 


def example():
    print("Hi low level")

if __name__ == '__main__':
    refence_queue = multiprocessing.Queue(1)
    low_level_control_process = multiprocessing.Process(target = low_level_controller,args = (settings_pump1,refence_queue))
    low_level_control_process.start()
    refence_queue.put(0)
    print("hallow world")
    i=0

    while True:
        #Perform high level control
        print("High level hi")
        time.sleep(5)
        refence_queue.put(i)
        i=i+0.1


