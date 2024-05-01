from pyModbusTCP.client import ModbusClient
from low_level_settings import *
from functions import consumer_valve_controller
import time
import scipy.io

MB_tower = ModbusClient(host = settings_pump2['ip_tower'], port = 502, auto_open = True)    #Connection to read water level in tower
MB_pump1 = ModbusClient(host = settings_pump1['ip_pump'], port = 502, auto_open=True)
MB_pump2 = ModbusClient(host = settings_pump2['ip_pump'], port = 502, auto_open=True)
MB_cons = ModbusClient(host= settings_consumer['ip_consumer'], port= 502, auto_open= True)

valve1 = consumer_valve_controller(settings_consumer['register_flow1']) 
valve2 = consumer_valve_controller(settings_consumer['register_flow2']) 

demand_temp = scipy.io.loadmat('ADMM_controller/Data/average_scaled_consumption.mat')
demand_vector = demand_temp['average_scaled_consumption']



tank_tower_min = 75
tank_pump_max = 530 #[mm]
tank_consumer_min = 75
tank_consumer_max = 570
tank_pump_ref = 380
aux_pump_switch_time = 60 # [s]
last_turn_on_time = time.time()

last_sample_time = time.time()

try:
    while True: 
        #Perform return water control
        tank_consumer = MB_cons.read_input_registers(settings_consumer['register_tank'],1)[0]
        tank_pump1 = MB_pump1.read_input_registers(settings_pump1['register_pump_tank'], 1)[0]
        tank_pump2 = MB_pump2.read_input_registers(settings_pump2['register_pump_tank'], 1)[0]

        MB_cons.write_single_register(3,10000)    #Open bootom valve
        MB_tower.write_single_register(3,10000)   #Open bootom valve

        #MB_cons.write_single_register(1,10000)    #Open bootom valve
        #MB_cons.write_single_register(2,10000)    #Open bootom valve


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
        demand_ref = demand_vector[simulated_hour]

        tower_tank_level = MB_tower.read_input_registers(settings_pump1['register_tower_tank'], 1)[0]
        
        flow_valve1 = 0.06/100*MB_cons.read_input_registers(settings_consumer['register_flow1'], 1)[0]
        flow_valve2 = 0.06/100*MB_cons.read_input_registers(settings_consumer['register_flow2'], 1)[0]

        #Safety control, close valves if the consumer is too full or the tower too empty. Otherwise, initiate control
        if(tank_consumer > settings_consumer['tank_max'] or tower_tank_level < tank_tower_min):
            MB_cons.write_single_register(settings_consumer['register_valve1'], 0)     
            MB_cons.write_single_register(settings_consumer['register_valve2'], 0)     
            print("Safety level control active")
        else:
            #Determine whether one or two valves should be operating based on a switching limit
            if(demand_ref > settings_consumer['switching_limit']):
                OD_valve1 = valve1.consumption_PI(demand_ref/2, flow_valve1)
                OD_valve2 = valve2.consumption_PI(demand_ref/2, flow_valve2)
            else:
                OD_valve1 = valve1.consumption_PI(demand_ref, flow_valve1)
                OD_valve2 = valve2.consumption_PI(0, flow_valve2)
            
            
            #Write to the registers
            MB_cons.write_single_register(settings_consumer['register_valve1'], int(100*OD_valve1))
            MB_cons.write_single_register(settings_consumer['register_valve2'], int(100*OD_valve2))

        time.sleep(1)

except:
    MB_pump1.write_single_register(8, 0)
    MB_pump1.write_single_register(9, 0)
    MB_pump2.write_single_register(8, 0)
    MB_pump2.write_single_register(9, 0)

    MB_cons.write_single_register(3,0)    #Close bootom valve 
    MB_tower.write_single_register(3,0)    #Close bootom valve 
  
    MB_cons.write_single_register(1,0)    #Open bootom valve
    MB_cons.write_single_register(2,0)    #Open bootom valve

    print("Pumps turned off, valves closed due to exception")




























        
