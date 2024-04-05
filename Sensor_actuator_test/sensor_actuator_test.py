from pyModbusTCP.client import ModbusClient
import time
ip_addr = '192.168.100.43'

MB = ModbusClient(host=ip_addr, port=502, auto_open=True)
time.sleep(3)
if MB.open():
    print("Modbus open")
else:
    print("Modbus not open")

MB.local.write_multipe_registers(5,100*100)
time.sleep(5) # [s]
MB.write_multipe_registers(5,0)
time.sleep(5)

MB.write_multipe_registers(5,100*100)
time.sleep(5)
MB.write_multipe_registers(5,0)
time.sleep(5)

MB.write_multipe_registers(5,100*100)
time.sleep(5)
MB.write_multipe_registers(5,0)
time.sleep(5)