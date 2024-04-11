"""
04 may 2024
Author: Lau Lauridsen

Test modbus communication in smart water infastructur lab at Aalborg university department of Electronic Systems
"""

from pyModbusTCP.client import ModbusClient
import numpy as np
import time

ip_addr = '192.168.100.20'  #Module IP adress

MB = ModbusClient(host=ip_addr, port=502, auto_open=True)
time.sleep(1)
if MB.open():
    print("Modbus open")
else:
    print("Modbus not open")

while True:

    data = MB.read_input_registers(0,25)
    print(data)
    time.sleep(2)

"""
MB.write_single_register(6,50*100)
time.sleep(5) # [s]
MB.write_single_register(6,0)
time.sleep(5)
"""
