import time

class StopWatch():

    def __init__(self, client_type,):
        self._client_type = client_type
        self._total_running_time = 0
        self._total_times = 0
        self._last = 0
        self._cur = 0
    
    def begin(self):
        self._last = time.clock()
    
    def end(self):
        self._cur = time.clock()
        self._total_times += 1
        self._total_running_time += self._cur - self._last

    def print(self):
        if self._total_times != 0:
            print('Times: {}; Average running time of {} is {:.4f}ms.'.format(self._total_times, \
                self._client_type, self._total_running_time * 1000.0 / self._total_times))