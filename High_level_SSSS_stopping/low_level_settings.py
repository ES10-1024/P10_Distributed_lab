settings_pump1 = {  #Module 144
    "sampletime":1,
    "proportional_gain":6.5/2,      #6.5 in repot 
    "integral_gain":3.5,
    "initial_integral_value":50/3.5,
    "lower_saturation_limit":0,
    "upper_saturation_limit":100,
    "ip_pump":"192.168.100.42",
    "register_pump":5,
    "register_aux_pump1":8,
    "register_aux_pump2":9,
    "register_pump_tank":4,
    "ip_tower":'192.168.100.34',
    "register_tower_tank":7,
    "ip_pipe":'192.168.100.20',
    "register_flow_pipe":1,
    "pump_tank_min":100,
    "consumer_tank_max":575
}


settings_pump2 = { #Module 43
    "sampletime":1,
    "proportional_gain":16/2, #16 in report
    "integral_gain":3,
    "initial_integral_value":44/3,
    "lower_saturation_limit":0,
    "upper_saturation_limit":100,
    "ip_pump":"192.168.100.43",
    "register_pump":7,
    "register_aux_pump1":8,
    "register_aux_pump2":9,
    "register_pump_tank":4,
    "ip_tower":'192.168.100.34',
    "register_tower_tank":7,
    "ip_pipe":'192.168.100.20',
    "register_flow_pipe":2,
    "pump_tank_min":100,
    "consumer_tank_max":575
}

settings_consumer = {
    "ip_consumer":"192.168.100.32",
    "register_valve1":1,
    "register_valve2":2,
    "register_flow1":16,  
    "register_flow2":17,  
    "register_tank":7,
    "tank_min": 70,
    "tank_max": 575,
    "switching_limit":0.275 #0.2 in report
}
