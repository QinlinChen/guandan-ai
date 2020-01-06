import time


class StopWatch():

    def __init__(self, name):
        self._name = name
        self._total_running_time = 0
        self._total_count = 0
        self._start_time = -1

    def begin(self):
        self._start_time = time.time()

    def end(self):
        if self._start_time == -1:
            return
        self._total_count += 1
        self._total_running_time += time.time() - self._start_time
        self._start_time = -1

    def average_running_time(self):
        return self._total_running_time * 1000 / self._total_count

    def __str__(self):
        return 'Repeat: {}; Average running time of {} is {:.4f}ms.'.format(
            self._total_count, self._name, self.average_running_time())
