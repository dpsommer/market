import copy

from market.data.core import SimulatedObject, loadable
from market.data.items import Item, Inventory
from market.data.resources import Resource, Zone


@loadable
class Actor(SimulatedObject):
    def __init__(self, name, starting_gold=0, starting_inventory=None, buy_list=None):
        super(Actor, self).__init__(name)
        self._gold = starting_gold
        self._inventory = starting_inventory or Inventory()
        self._buy_list = buy_list or {}

    def gather(self, resource):
        """

        :param resource:
        :type resource: Resource
        """
        drops = resource.generate_drops()
        for drop, amount in drops.items():
            self._inventory.add(drop, amount)

    def gather_from_zone(self, zone):
        """

        :param zone:
        :type zone: Zone
        """
        for resource, amount in zone.get_resources().items():
            for _ in range(amount):
                self.gather(resource)
                zone.remove_resource(resource)

    def buy(self, seller, item, price, amount=1):
        """
        Buy some number of goods from another actor for a set price.

        :param seller: the actor to buy from
        :type seller: Actor
        :param item: the item to purchase
        :type item: Item
        :param price: the price at which to buy items. XXX: should this be dynamic?
        :type price: int
        :param amount: the number of items to buy
        :type amount: int
        """
        try:
            self.remove_gold(price * amount)
            seller.remove_from_inventory(item, amount)
            seller.add_gold(price * amount)
            self.add_to_inventory(item, amount)
        except Inventory.InsufficientInventory as e:
            # FIXME: this works as a stop-gap, but it would be better to have a proper transaction here
            #   e.g. pickle state for buyer and seller to memory, recover on failure
            self.add_gold(price * amount)
            raise e

    def sell(self, buyer, item, price, amount=1):
        buyer.buy(self, item, price, amount)

    def prioritize_buy_list(self):
        pass  # TODO: update buy list based on inventory contents

    def add_gold(self, amount):
        self._gold += amount

    def remove_gold(self, amount):
        if self._gold < amount:
            raise Actor.NotEnoughGold("Not enough gold for transaction.")
        self._gold -= amount

    def get_gold_total(self):
        return self._gold

    def add_to_inventory(self, item, amount=1):
        self._inventory.add(item, amount)

    def remove_from_inventory(self, item, amount=1):
        self._inventory.remove(item, amount)

    def update_inventory(self, items):
        self._inventory.update(items)

    def clear_inventory(self):
        self._inventory.clear()

    def get_inventory(self):
        return copy.deepcopy(self._inventory)

    def add_to_buy_list(self, item, price):
        self._buy_list.add(item, price)

    def remove_from_buy_list(self, item):
        self._buy_list.pop(item)

    def get_buy_list(self):
        return copy.deepcopy(self._buy_list)

    class NotEnoughGold(Exception):
        pass
