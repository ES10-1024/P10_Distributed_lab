import time
import multiprocessing
from pyModbusTCP.client import ModbusClient
from low_level_settings import settings_pump1


def low_level_controller(settings_pump: dict, q):
    #q is queue where new refrence can be put
    
    last_sample_time = time.time()
    ref = 0

    MB_flow = ModbusClient(host = settings_pump['ip_pipe'], port = 502, auto_open = True)
    MB_pump = ModbusClient(host = settings_pump['ip_pump'], port = 502, auto_open=True)
    MB_tower = ModbusClient(settings_pump['ip_tower'], port = 502, auto_open = True)

    while True:
        sleep_time = settings_pump['sampetime'] - (time.time() - last_sample_time)
        time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 

        flow = MB_flow.read_input_registers(settings_pump['index_flow_pipe'], 1)
        try:
            ref = q.get_nowait()
        except:
            pass

        error = ref - flow
        print(error)
        #Insert PID controller
        pump_precentage = 50

        #Perform supervisory level control and output actuation if ok
        pump_tank_level = MB_pump.read_input_registers(settings_pump['index_pump_tank'], 1)
        tower_tank_level = MB_tower.read_input_registers(settings_pump['index_tower_tank'], 1)
        if(pump_tank_level < settings_pump['tank_min'] or tower_tank_level > settings_pump['tank_max']):
            MB_pump.write_multiple_registers(settings_pump['index_pump'], 0)     #Turn off pump
        else:
            MB_pump.write_multiple_registers(settings_pump['index_pump'], pump_precentage)


if __name__ == '__main__':
    print("hallow world")
    refence_queue = multiprocessing.Queue(1)
    low_level_control_process = multiprocessing.Process(target = low_level_controller,args = (settings_pump1,refence_queue))

while True:
    #Perform high level control
    print("hi")
    time.sleep(5)

    