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
    if 'Potion' in Item.REFERENCE_MAP:
        potion = Item.REFERENCE_MAP.get('Potion')
    else:
        potion = Item(name='Potion')
    print(potion.uuid)
    drop = Resource.Drop(item=potion)
    monster = Monster(name='Slime', drop_table={drop: 60})
    adventurer = Adventurer(name='Isaac')
    adventurer.hunt(monster)
    print(adventurer.inventory)
    Data.save()


if __name__ == "__main__":
    main()
