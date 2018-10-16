import os

from market.data.core import GameObject
from market.data.items import Inventory


class Actor(GameObject):

    def __init__(self, name, starting_gold=0, starting_inventory=None):
        super(Actor, self).__init__(name)
        self.name = name
        self.gold = starting_gold
        self.inventory = starting_inventory or Inventory()

    def buy(self, item, price, amount=1):
        if self.gold < price * amount:
            raise Actor.NotEnoughGold(
                "Can't buy %d %s at %dg, %s only has %dg." % (amount, str(item), price, self.name, self.gold))
        self.add_to_inventory(item, amount)
        self.gold -= price * amount

    def sell(self, item, price, amount=1):
        if item not in self.inventory or self.inventory[item] < amount:
            raise Actor.InsufficientInventory("Not enough inventory to sell %d %s." % (amount, str(item)))
        self.inventory[item] -= amount
        self.gold += price * amount

    def add_to_inventory(self, item, amount):
        # TODO: update Inventory insert to simplify this
        if item in self.inventory:
            self.inventory[item] += amount
        else:
            self.inventory[item] = amount

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


class Adventurer(Actor):

    MARSHAL_FILE_NAME = os.path.join(os.path.dirname(__file__), 'adventurers.json')

    def __init__(self, name):
        super(Adventurer, self).__init__(name)

    def hunt(self, monster):
        # TODO: rather than passing in a monster object,
        #   this function should accept a hunting 'zone'
        #   and determine monsters to hunt based on that
        drops = monster.generate_drops()
        for drop, amount in drops.items():
            if drop in self.inventory:
                self.inventory[drop] += amount
            else:
                self.inventory[drop] = amount
