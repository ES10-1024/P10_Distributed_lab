import time
import multiprocessing
from pyModbusTCP.client import ModbusClient


def low_level_controller(sample_time: int, proportiaonl_gain: float, integral_gain: float, ip_pump: str, index_pump: int, index_pump_tank: int, ip_tower: str, index_tower_tank: int, ip_pipe: str, index_flow_pipe,  tank_min: float, tank_max: float,q):
    #q is queue where new refrence can be put
    
    last_sample_time = time.time()
    ref=0

    MB_flow = ModbusClient(host=ip_pipe, port=502, auto_open=True)
    MB_pump = ModbusClient(host=ip_pump, port=502, auto_open=True)
    MB_tower = ModbusClient(host=ip_tower, port=502, auto_open=True)

    while True:
        sleep_time = sample_time - (time.time()-last_sample_time)
        time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 

        flow = MB_flow.read_input_registers(index_flow_pipe,1)
        try:
            ref = q.get_nowait()
        except:
            pass

        error = ref-flow
        #Insert PID controller
        pump_precentage = 0

        #Perform supervisory level control and output actuation if ok
        pump_tank_level = MB_pump.read_input_registers(index_pump_tank,1)
        tower_tank_level = MB_tower.read_input_registers(index_tower_tank,1)
        if(pump_tank_level < tank_min or tower_tank_level > tank_max):
            MB_pump.write_multiple_registers(index_pump, 0)     #Turn off pump
        else:
            MB_pump.write_multiple_registers(index_pump, pump_precentage)


if __name__ == '__main__':
    refence_queue = multiprocessing.Queue(1)
    low_level_control_process = multiprocessing.Process(target=low_level_controller,args=())

while True:
    #Perform high level control
        

    