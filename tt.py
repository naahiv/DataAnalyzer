import threading
from time import sleep

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self):
        for i in range(10):
            if self.is_stopped():
                return
            sleep(1)
            print(f'stock {i+1} generated')


if __name__ == '__main__':
    thread = CustomThread()
    thread.start()
    sleep(3)
    thread.stop()
    thread.join()
    print('is this separate??')
