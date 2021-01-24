import threading
import time


class Worker(threading.Thread):

    def __init__(self, task, wait_time):
        """
        Construct an object that performs a recurrent task in loop on a separate thread
        :param task: The task (a function) to execute
        :param wait_time: Seconds to wait between two consecutive executions
        """
        super().__init__()

        self.task = task
        self.wait_time = wait_time
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            start = time.time()
            self.task()
            end = time.time()
            time.sleep(max(self.wait_time - (end - start), 0.001))

    def set_wait_time(self, wait_time):
        self.wait_time = wait_time

    def stop(self):
        self._running = False
