import time
from pyModbusTCP.client import ModbusClient


def low_level_controller(settings, refrence_queue):
    #q is queue where new refrence can be put
    print("low level hallow world")
    last_sample_time = time.time() #unix time 
    pump_percentage = 0
    ref = 0
    integral = settings['initial_integral_value']

    MB_flow = ModbusClient(host = settings['ip_pipe'], port = 502, auto_open = True)
    MB_pump = ModbusClient(host = settings['ip_pump'], port = 502, auto_open=True)
    MB_tower = ModbusClient(host = settings['ip_tower'], port = 502, auto_open = True)

    #try:
    while True:
        sleep_time = last_sample_time + settings['sampletime']  - time.time()
        time.sleep(sleep_time)
        last_sample_time = time.time()      #unix time 

        try:
                ref = refrence_queue.get_nowait() # m^3/h
        except:
            pass

        #Perform supervisory level control run controller if ok
        pump_tank_level = MB_pump.read_input_registers(settings['register_pump_tank'], 1)[0]
        tower_tank_level = MB_tower.read_input_registers(settings['register_tower_tank'], 1)[0]

        if(pump_tank_level < settings['pump_tank_min'] or tower_tank_level > settings['consumer_tank_max']):
            MB_pump.write_single_register(settings['register_pump'], 0)     #Turn off pump
            print("Safety level control active")
        else:

            flow = 0.06/100*MB_flow.read_input_registers(settings['register_flow_pipe'], 1)[0] #Some unit
        
            print("Flow:", flow)
            
            error = ref - flow
            integral = integral + error*settings["sampletime"]

            if(integral*settings['integral_gain'] > settings["upper_saturation_limit"]):
                integral = settings["upper_saturation_limit"]/settings['integral_gain']
                print("Integral saturated")

            if(integral*settings['integral_gain'] < settings["lower_saturation_limit"]):
                integral = settings["lower_saturation_limit"]/settings['integral_gain']

            PI_output = settings['proportional_gain']*error + settings['integral_gain']*integral

            if(PI_output>settings["upper_saturation_limit"]):
                pump_percentage = settings["upper_saturation_limit"]
                print("Controller saturated")
            elif(PI_output < settings["lower_saturation_limit"]):
                pump_percentage = settings["lower_saturation_limit"]
                print("Controller saturated")
            else:
                pump_percentage = PI_output
                print("Pump", pump_percentage)
        
            MB_pump.write_single_register(settings['register_pump'], int(100*pump_percentage))

'''
    #except Exception as error:
        print("Low level error:")
        print(error)
        MB_pump.write_single_register(settings['register_pump'], int(0))
        print("Low level controller have turned off pump due to above error")
'''





