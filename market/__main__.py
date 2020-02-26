import signal

from market.data.actors import Actor
from market.data.items import Item
from market.data.resources import Resource
from market.core import Data
from market.util.time import SimulationTimer


MAIN_THREAD = SimulationTimer(
    completion_callback=signal.alarm,
    callback_arguments=[1],
    days_to_simulate=1
)


def run():
    Data.load()
    potion = Item('Potion')
    slime = Resource('Slime')
    adventurer = Actor('Isaac')
    if not slime.get_drop_table():
        drop = Resource.Drop(item=potion)
        slime.add_drop(drop, rate=60)
    adventurer.gather(slime)
    print(''.join([f'{k}: {v.value}, {v.tier}, {v.modifier}\n' for k, v in adventurer.priorities.items()]))

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
