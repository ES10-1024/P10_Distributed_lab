import time
import multiprocessing
from low_level_settings import settings_pump2
from low_level_control import low_level_controller

if __name__ == '__main__':
    refence_queue = multiprocessing.Queue(1)
    low_level_control_pump2 = multiprocessing.Process(target = low_level_controller,args = (settings_pump2,refence_queue))
    low_level_control_pump2.start()
    refence_queue.put(0)
    print("hallow world")
    i=0

    while True:
        #Perform high level control
        print("High level hi")
        i=0.05
        refence_queue.put(i)
        time.sleep(5)