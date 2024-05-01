import numpy as np

c_pump1 = {
    "Q_min":0,                  #Minimum daily limit[m^3/day]
    "Q_max":3.6,                 #TYEL [m^3/day]
    "q_min":0,                  #Minimum mass flow [m^3/h]
    "q_max":0.3,                #Maximum mass flow[m^3/h]
    "eta":0.909,                #Efficincy of pump
    "r_f":0.35*(10**5),         #Pipe resistance
    "h":2                       #Pipe elevation
}

c_pump2 = {
    "Q_min":0,                  #Minimum daily limit[m^3/day]
    "Q_max":3.6,                 #TYEL [m^3/day]
    "q_min":0,                  #Minimum mass flow [m^3/h]
    "q_max":0.3,                #Maximum mass flow[m^3/h]
    "eta":0.796,                #Efficincy of pump
    "r_f":0.42*(10**5),         #Pipe resistance
    "h":1.5                     #Pipe elevation
}

c_tower = {
    "h_V_min":0.1,              #Minimum height in water tower [m]
    "h_V_max":0.55,             #Maximum height in water tower [m]
    "V_min":28/1000,            #Minimum volume of water in tower [m^3]
    "V_max":155/1000,           #Maximum volume of water in tower [m^3]
    "A_t":0.283,                #Water surface area in tower [m^2]
    "rho_w":997,                #Density of water [kg/m^3]
    "g_0":9.82,                 #Gravitational acceleration [m/s^2]
    "kappa":0#900                 #Volume cost
}

c_general = {
    "r_fsigma":0.29*(10**5),    #Combined pipe resistance
    "N_q":2,                    #Number of pump stations
    "N_d":1,                    #Number of consumption groups
    "N_c":24,                   #Control horizon
    "t_s":600,                   #Sample time [s]
    "acc_time":6,               #Number of accelerated hours in one real-life hour
    "condition_scaling":10000,  #Scaling variable for conditioning
    "hours_to_seconds":1/3600   #Use when going from m^3/h to m^3/s
}