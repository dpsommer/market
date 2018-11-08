import pprint

from market.util.data import SIMULATION_STATE
from market.data.items import Item
from market.util.data import Data
from market.data.resources import Resource
from market.data.actors import Actor


def main():
    Data.load()
    pprint.pprint(SIMULATION_STATE)
    potion = Item.get('Potion')
    print(potion.uuid)
    drop = Resource.Drop(item=potion)
    slime = Resource.get('Slime')
    slime.add_drop(drop, rate=60)
    adventurer = Actor.get('Isaac')
    adventurer.gather(slime)
    print(adventurer.get_inventory())
    Data.save()


if __name__ == "__main__":
    main()
