import abc
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from market.data.actors import Actor
from market.data.items import Item
from market.data.resources import Resource
from market.core import Data

# TODO: thread safety in data classes
LOCK = threading.Lock()
# Each 'day' occurs on the main thread and then actor behaviours
# are parcelled out into a thread pool for computation
executor = ThreadPoolExecutor(max_workers=10)

# How long it takes for an hour to pass in simulation time
# 1 hour = 10 seconds; 1 day = 4 minutes; 1 week = 28 minutes; 1 year = 1460 minutes = ~61 hours = ~2.5 days
TIME_SCALE = 1 / 360
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY


class T(threading.Thread, abc.ABC):

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.setDaemon(True)

    def run(self):
        while not self._stop_event.is_set():
            self._run()

    @abc.abstractmethod
    def _run(self):
        pass

    def stop(self):
        self._stop_event.set()


class Simulation(T):

    def __init__(self, days_to_simulate=365):
        super().__init__()
        self.days_remaining = days_to_simulate
        self._zero = time.time()
        self.timer = None

    def _run(self):
        if self.days_remaining <= 0:
            self.stop()
            signal.alarm(1)
        elif not self.timer or self.timer.finished.is_set():
            self.timer = threading.Timer(SECONDS_PER_DAY * TIME_SCALE, self.decrement_day_count)
            self.timer.start()
        time.sleep(1)

    def decrement_day_count(self):
        self.days_remaining -= 1

    def time_of_day(self):
        seconds_since_zero = time.time() - self._zero
        days, t = divmod(seconds_since_zero, SECONDS_PER_DAY * TIME_SCALE)
        return divmod(t, (SECONDS_PER_DAY * TIME_SCALE) / HOURS_PER_DAY)

    def stop(self):
        executor.shutdown()
        super().stop()


def simulate_actor_behaviour(actor):
    # TODO
    actor.gather(Resource.get('Slime'))


MAIN_THREAD = Simulation(days_to_simulate=3)


def run():
    Data.load()
    potion = Item.get('Potion')
    slime = Resource.get('Slime')
    adventurer = Actor.get('Isaac')
    if not slime.get_drop_table():
        drop = Resource.Drop(item=potion)
        slime.add_drop(drop, rate=60)
    adventurer.gather(slime)
    print(adventurer.get_inventory())

    MAIN_THREAD.start()
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGALRM, shutdown)
    signal.pause()


def shutdown(sig, frame):
    print('Shutting down...')
    MAIN_THREAD.stop()
    MAIN_THREAD.join()
    print('Saving data...')
    Data.save()
    print('Stopped.')


if __name__ == "__main__":
    run()
