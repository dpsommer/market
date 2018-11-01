from functools import reduce

from market.data.core import GameObject, loadable


@loadable
class Item(GameObject):

    def __init__(self, name):
        super(Item, self).__init__(name)

    class NoSuchItem(Exception):
        pass


class Inventory(dict):

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)

    def add(self, item, amount):
        """
        Add some number of an item to the inventory.

        :param item: the item to add
        :type item: Item
        :param amount: amount to add
        :type amount: int
        """
        amount = self.get(item) + amount if item in self else amount
        self[item] = amount

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

    def __str__(self):
        return reduce(lambda x, y: "%s\t%s: %s\n" % (x, y.name, self[y]), self, "{\n") + "}"
