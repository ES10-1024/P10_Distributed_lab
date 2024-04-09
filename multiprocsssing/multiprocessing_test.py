import time
import multiprocessing

def do_something():
    print("I'm going to sleep")
    time.sleep(1)
    print("I'm awake") 

if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=do_something)
    process_1.start()