from market.data.items import Item
from market.util.data import Data
from market.data.resources import Resource, Monster
from market.data.actors import Adventurer
import threading

THREADS = []


class T(threading.Thread):

    def __init__(self):
        super(T, self).__init__()

    def run(self):
        super(T, self).run()
        while True:
            pass
    
    def join(self, timeout=None):
        # TODO: marshal objects
        super(T, self).join(timeout)

for thread in THREADS:
    thread.run()

for thread in THREADS:
    thread.join()


def main():
    Data.load()
    print(Item.REFERENCE_MAP)
    potion = Item.get('Potion')
    print(potion.uuid)
    drop = Resource.Drop(item=potion)
    slime = Monster.get('Slime')
    slime.add_drop(drop, rate=60)
    adventurer = Adventurer.get('Isaac')
    adventurer.hunt(slime)
    print(adventurer.inventory)
    Data.save()


if __name__ == "__main__":
    main()
