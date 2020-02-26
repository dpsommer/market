import threading
import time

from abc import ABC, abstractmethod


class BaseThread(threading.Thread, ABC):

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.setDaemon(True)

    def run(self):
        while not self._stop_event.is_set():
            self._run()

    @abstractmethod
    def _run(self):
        pass

    def stop(self):
        self._stop_event.set()


class TimerThread(BaseThread):

    def __init__(self, callback, ticks, seconds_per_tick):
        super().__init__()
        self.ticks = ticks
        self.seconds_per_tick = seconds_per_tick
        self._callback = callback
        self.timer = None

    def _run(self):
        if self.ticks == 0:  # -1 to run forever
            self.stop()
        elif not self.timer or self.timer.finished.is_set():
            if self.timer:  # after each successive tick
                self.timer.join()
                self.ticks -=1
            self.timer = threading.Timer(self.seconds_per_tick, self._callback)
            self.timer.start()
        time.sleep(1)
