from pyModbusTCP.client import ModbusClient
import time

ip_addr = '192.168.100.20'  #Module IP adress

MB = ModbusClient(host=ip_addr, port=502, auto_open=True)
#Setup connection to module, 

if MB.open():
    print("Modbus open")
else:
    print("Modbus not open")    #Some bug, e.g. ethernet
    quit()   #End script

data = MB.read_input_registers(0,25)
print(data)


MB.write_single_register(6,50*100)
time.sleep(5) 
MB.write_single_register(6,0)
time.sleep(5)