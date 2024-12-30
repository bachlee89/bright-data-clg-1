import threading
from model.log import Log
from model.thread.spinner import Spinner
import sys
import time


class ThreadConnector(threading.Thread):
    def __init__(self, name, connector, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.connector = connector
        self.log = Log()
        self.delay = delay

    def run(self):
        connector = self.connector
        print(self.get_current_time() + "Starting " + self.name)
        spinner = Spinner()
        spinner.start()
        # Get lock to synchronize threads
        threadLock = threading.Lock()
        threadLock.acquire()
        try:
            connector.execute()
        except:
            self.log.log(str(sys.exc_info()), 'debug')
            print(str(sys.exc_info()))
        # Free lock to release next thread
        threadLock.release()
        spinner.stop()
        # try:
        #     if connector.driver !=False:
        #         connector.driver.close()
        #         connector.driver.quit()
        # except:
        #     pass
        print(self.get_current_time() + "Ending " + self.name)
        time.sleep(self.delay)

    def get_current_time(self):
        return "[" + time.strftime("%Y-%m-%d %H:%M:%S") + "]"
