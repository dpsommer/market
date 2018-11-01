import copy

from market.data.core import GameObject, loadable
from market.data.items import Inventory


class Actor(GameObject):

    def __init__(self, name, starting_gold=0, starting_inventory=None):
        super(Actor, self).__init__(name)
        self._gold = starting_gold
        self._inventory = starting_inventory or Inventory()

    def buy(self, item, price, amount=1):
        if self._gold < price * amount:
            raise Actor.NotEnoughGold(
                "Can't buy %d %s at %dg, %s only has %dg." % (amount, str(item), price, self.name, self._gold))
        self._inventory.add(item, amount)
        self._gold -= price * amount

    def sell(self, item, price, amount=1):
        if item not in self._inventory or self._inventory[item] < amount:
            raise Actor.InsufficientInventory("Not enough inventory to sell %d %s." % (amount, str(item)))
        self._inventory[item] -= amount
        self._gold += price * amount

    def add_to_inventory(self, item, amount):
        self._inventory.add(item, amount)

    def update_inventory(self, items):
        self._inventory.update(items)

    def clear_inventory(self):
        self._inventory.clear()

    def get_inventory(self):
        return copy.deepcopy(self._inventory)

    class NotEnoughGold(Exception):
        pass

    class InsufficientInventory(Exception):
        pass


class Merchant(Actor):

    def __init__(self, name, price_list=None):
        super(Merchant, self).__init__(name)
        self.price_list = price_list or {}

    def get_prices(self):
        return self.price_list


@loadable
class Adventurer(Actor):

    def __init__(self, name):
        super(Adventurer, self).__init__(name)

    def hunt(self, monster):
        # TODO: rather than passing in a monster object,
        #   this function should accept a hunting 'zone'
        #   and determine monsters to hunt based on that
        drops = monster.generate_drops()
        for drop, amount in drops.items():
            self._inventory.add(drop, amount)
