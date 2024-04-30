from pyModbusTCP.client import ModbusClient
from low_level_settings import *
import time

MB_tower = ModbusClient(host = settings_pump2['ip_tower'], port = 502, auto_open = True)    #Connection to read water level in tower
MB_pump1 = ModbusClient(host = settings_pump1['ip_pump'], port = 502, auto_open=True)
MB_pump2 = ModbusClient(host = settings_pump2['ip_pump'], port = 502, auto_open=True)
MB_cons = ModbusClient(host= "192.168.100.32", port= 502, auto_open= True)

tank_pump_max = 530 #[mm]
tank_consumer_min = 75
tank_consumer_max = 570
tank_pump_ref = 520
aux_pump_switch_time = 10 # [s]
last_turn_on_time = time.time()

last_sample_time = time.time()

while True: 
    #Perform return water control
    tank_consumer = MB_cons.read_input_registers(settings_pump1['register_tower_tank'],1)[0]
    tank_pump1 = MB_pump1.read_input_registers(settings_pump1['register_pump_tank'], 1)[0]
    tank_pump2 = MB_pump2.read_input_registers(settings_pump2['register_pump_tank'], 1)[0]
    print(tank_consumer)
    print(tank_pump1)
    print(tank_pump2)

    if(tank_consumer > tank_consumer_max):           #Set both aux pumps max power
        MB_pump1.write_single_register(8, 100*100)
        MB_pump1.write_single_register(9, 100*100)
        MB_pump2.write_single_register(8, 100*100)
        MB_pump2.write_single_register(9, 100*100)
        print("Consumer overfull")
        
    elif(tank_consumer < tank_consumer_min):        #Turn off both pumps
        MB_pump1.write_single_register(8, 0)
        MB_pump1.write_single_register(9, 0)
        MB_pump2.write_single_register(8, 0)
        MB_pump2.write_single_register(9, 0)
        print("Consumer empty")

    elif( tank_pump1 > tank_pump_max and tank_pump2 > tank_pump_max):
        MB_pump1.write_single_register(8, 0)
        MB_pump1.write_single_register(9, 0)
        MB_pump2.write_single_register(8, 0)
        MB_pump2.write_single_register(9, 0)
        print("Pump stations overfull")

    elif( tank_pump1 < tank_pump_ref or tank_pump2 < tank_pump_ref):
        if(time.time() > last_turn_on_time + aux_pump_switch_time):     #if below refrence and long time since settings change
            last_turn_on_time= time.time()
            if(tank_pump1 < tank_pump2):
                MB_pump1.write_single_register(8, 100*100)
                MB_pump1.write_single_register(9, 100*100)
                MB_pump2.write_single_register(8, 0)
                MB_pump2.write_single_register(9, 0)
                print("Return water to pump 1")
            else:                                        
                MB_pump1.write_single_register(8, int(0))
                MB_pump1.write_single_register(9, 0)
                MB_pump2.write_single_register(8, 100*100)
                MB_pump2.write_single_register(9, 100*100)
                print("Return water to pump 2")

    #PID controller for consumer unit
    time.sleep(1)
