import copy

from market.data.core import GameObject, loadable
from market.data.items import Item, Inventory


class Actor(GameObject):
    def __init__(self, name, starting_gold=0, starting_inventory=None):
        super(Actor, self).__init__(name)
        self._gold = starting_gold
        self._inventory = starting_inventory or Inventory()

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

    class NotEnoughGold(Exception):
        pass


@loadable
class Merchant(Actor):
    def __init__(self, name, buy_list=None, markup=1.5, **kwargs):
        super(Merchant, self).__init__(name, **kwargs)
        self._inventory.callback = self._update_price_list
        self._buy_list = buy_list or {}
        self._markup = markup
        self._price_list = {}
        self._update_price_list()

    def _determine_sale_price(self, item):
        # FIXME: naive initial implementation - if the item exists in the buylist simply apply a flat markup
        if item in self._buy_list:
            return self._buy_list.get(item) * self._markup
        return 0  # FIXME

    def _update_price_list(self):
        self._price_list = {item: self._determine_sale_price(item) for item in self._inventory.keys()}

    def add_to_buy_list(self, item, price):
        self._buy_list.add(item, price)

    def get_buy_list(self):
        return copy.deepcopy(self._buy_list)

    def get_prices(self):
        return copy.deepcopy(self._price_list)


@loadable
class Adventurer(Actor):
    def __init__(self, name, **kwargs):
        super(Adventurer, self).__init__(name, **kwargs)

    def hunt(self, monster):
        # TODO: rather than passing in a monster object,
        #   this function should accept a hunting 'zone'
        #   and determine monsters to hunt based on that
        drops = monster.generate_drops()
        for drop, amount in drops.items():
            self._inventory.add(drop, amount)
