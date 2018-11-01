from market.data.items import Item
from market.util.data import Data
from market.data.resources import Resource, Monster
from market.data.actors import Adventurer


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
    print(adventurer.get_inventory())
    Data.save()


if __name__ == "__main__":
    main()
