import multiprocessing
import time


def process_func(q):
    while True:
        print("Process")
        print(q.get())
        time.sleep(2)

if __name__ == '__main__':
    q = multiprocessing.Queue(10)
    q.put(1)
    process = multiprocessing.Process(target=process_func, args=(q,))
    process.start()
    while True: 
        print("Main")
        time.sleep(1.5)
        q.put(1)

