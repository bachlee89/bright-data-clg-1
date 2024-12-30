import sys
import time
import threading


class Spinner:
    busy = False
    delay = 0.1

    def spinning_cursor(self):
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner = 1
        if self.spinner == 1:
            self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        if self.spinner == 1:
            self.busy = True
            threading.Thread(target=self.spinner_task).start()

    def stop(self):
        if self.spinner == 1:
            self.busy = False
            time.sleep(self.delay)
