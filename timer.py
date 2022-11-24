import threading
import time

"""
class Timer:
    def __init__(self,stop_time,sleep_time=0.01,name="timer"):
        self.stop_time = stop_time
        self.sleep_time = sleep_time
        self.running = False
        self.queue = multiprocessing.Queue()
        self.delta = 0
        self.queue.put(self.delta)
        self.name = name

    def run(self):
        if not self.running:
            self.process = multiprocessing.Process(target=self.start,args=(self.queue,))
            self.process.start()
            #self.process.join()
            self.running = True

    def start(self,queue):
        self.t1 = time.time()
        while True:
            delta = time.time()-self.t1
            if self.stop_time and delta>=self.stop_time:
                self.delta = 0
                break
            else:
                self.delta = delta
                #print(f"{self.name} delta: {self.delta}")
            queue.put(self.delta)
            time.sleep(self.sleep_time)

    def get_delta(self):
        return self.queue.get()

    def stop(self):
        self.running = False
        self.process.terminate()
"""
class Timer(threading.Thread):
    def __init__(self,stop_time,sleep_time=0.01,name="timer",running_task=None,running_args=None,stop_task=None,stop_args=None):
        super().__init__()
        self.stop_time = stop_time
        self.name = name
        self.sleep_time = sleep_time
        self.running = False
        self.delta = 0
        self.running_task = running_task
        self.running_args = running_args
        self.stop_task = stop_task
        self.stop_args = stop_args

    def run(self):
        self.set_t1()
        while True:
            while self.running:
                delta = time.time()-self.t1
                if self.stop_time and delta>=self.stop_time: # Stop
                    self.delta = 0
                    self.execute_task(self.stop_task,self.stop_args)
                    break
                else: # Running
                    self.delta = delta
                    self.execute_task(self.running_task,self.running_args)
                    print(f"\r{self.name} delta: {self.delta}",end="                    ")
                time.sleep(self.sleep_time)

    def set_t1(self):
        self.t1 = time.time()

    def get_delta(self):
        return self.delta
    
    def get_remaining_time(self):
        return self.stop_time - self.delta
    
    def execute_task(self,task,args):
        if task:
            if args:
                if callable(args): args=args() # if args is function
                return task(args)
            else: return task() # if args is None

    def restart(self):
        self.set_t1()
        self.running = True
    def stop(self):
        self.execute_task(self.stop_task,self.stop_args)
        self.running = False