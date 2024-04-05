"""
04 may 2024
Author: Lau Lauridsen

Test modbus communication in smart water infastructur lab at Aalborg university department of Electronic Systems
"""

from pyModbusTCP.client import ModbusClient
import numpy as np
import time

ip_addr = '192.168.100.43'  #Module IP adress

MB = ModbusClient(host=ip_addr, port=502, auto_open=True)
time.sleep(3)
if MB.open():
    print("Modbus open")
else:
    print("Modbus not open")

data = MB.read_input_registers(1,18)
print(data)

print(MB.read_input_registers(1,1)[0])
print(MB.read_input_registers(2,1)[0])
print(MB.read_input_registers(3,1)[0])
print(MB.read_input_registers(4,1)[0])
print(MB.read_input_registers(5,1)[0])
print(MB.read_input_registers(6,1)[0])
print(MB.read_input_registers(7,1)[0])

pump_setting1 = np.array([0, 50*100, 0])
pump_setting2 = np.array([0, 0, 0])

MB.write_multiple_registers(5,list(pump_setting1))
time.sleep(5) # [s]
MB.write_multiple_registers(5,list(pump_setting2))
time.sleep(5)

