import os
from functools import reduce

from market.data.core import GameObject


class Item(GameObject):

    MARSHAL_FILE_NAME = os.path.join(os.path.dirname(__file__), 'items.p')
    REFERENCE_MAP = {}

    def __init__(self, name):
        super(Item, self).__init__(name)

    class NoSuchItem(Exception):
        pass


class Inventory(dict):

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)

    def add(self, item, amount):
        """
        Add some number of an item to the inventory

        :param item: the item to add
        :type item: Item
        :param amount: amount to add
        :type amount: int
        """
        amount = self.get(item) + amount if item in self else amount
        self[item] = amount

    def __str__(self):
        return reduce(lambda x, y: "%s\t%s: %s\n" % (x, y.name, self[y]), self, "{\n") + "}"
