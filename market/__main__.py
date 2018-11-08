import abc
import signal
import threading
from concurrent.futures import ThreadPoolExecutor

from market.data.actors import Actor
from market.data.items import Item
from market.data.resources import Resource
from market.util.data import Data, SIMULATION_STATE

LOCK = threading.Lock()
# Each 'day' occurs on the main thread and then actor behaviours
# are parcelled out into a thread pool for computation
executor = ThreadPoolExecutor(max_workers=10)


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

    def _run(self):
        for actor in SIMULATION_STATE[Actor].values():
            executor.submit(simulate_actor_behaviour, actor)
        self.days_remaining -= 1
        if self.days_remaining <= 0:
            self.stop()
            signal.alarm(1)

    def stop(self):
        executor.shutdown()
        super().stop()


def simulate_actor_behaviour(actor):
    # TODO
    actor.gather(Resource.get('Slime'))

MAIN_THREAD = Simulation()


def run():
    Data.load()

    print(SIMULATION_STATE)
    potion = Item.get('Potion')
    slime = Resource.get('Slime')
    adventurer = Actor.get('Isaac')
    if not slime.get_drop_table():
        drop = Resource.Drop(item=potion)
        slime.add_drop(drop, rate=60)
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
