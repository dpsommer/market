from functools import reduce

from market.core import SimulatedObject, loadable


@loadable
class Item(SimulatedObject):

    def __init__(self, name):
        super().__init__(name)

    class NoSuchItem(Exception):
        pass


class Inventory(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, item, amount=1):
        """
        Add some number of an item to the inventory.

        :param item: the item to add
        :type item: Item
        :param amount: amount to add
        :type amount: int
        """
        self[item] = self.get(item, 0) + amount

    def remove(self, item, amount=1):
        """
        Remove some number of an item from the inventory

        :param item: the item to remove
        :type item: Item
        :param amount: amount to remove
        :type amount: int
        """
        if item not in self or amount > self[item]:
            raise InsufficientInventory
        self[item] -= amount

    def update(self, E=None, **F):
        """
        Override the inbuilt dict update function to add to existing item totals.

        :param E: dict/iterable used to update the inventory
        :param F: optional k/v pairs
        """
        keys = getattr(E, 'keys', None)
        if keys and callable(keys):
            for k in E.keys():
                self.add(k, E[k])
        else:
            for k, v in E:
                self.add(k, v)
        for k in F.keys():
            self.add(k, F[k])

    def __setitem__(self, key, value):
        """
        Override __setitem__ to remove entries when their total reaches 0.

        :type key: Item
        :type value: int
        """
        super(Inventory, self).__setitem__(key, value)
        if value == 0:
            self.pop(key)

    def __str__(self):
        return reduce(lambda x, y: "%s\t%s: %s\n" % (x, y.name, self[y]), self, "{\n") + "}"


class Wallet(object):

    def __init__(self, gold):
        self.gold = gold

    def add(self, gold):
        self.gold += gold

    def remove(self, gold):
        if self.gold < gold:
            raise NotEnoughGold
        self.gold -= gold


class InsufficientInventory(Exception):
    pass


class NotEnoughGold(Exception):
    pass
