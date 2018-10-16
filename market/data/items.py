import os

from market.data.core import GameObject


class Item(GameObject):

    MARSHAL_FILE_NAME = os.path.join(os.path.dirname(__file__), 'items.json')
    REFERENCE_MAP = {}

    def __init__(self, name):
        super(Item, self).__init__(name)

    class NoSuchItem(Exception):
        pass


class Inventory(dict):

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)

    # TODO: make sure the object being inserted is an Item

    def __str__(self):
        return reduce(lambda x, y: "%s\t%s: %s\n" % (x, y.name, self[y]), self, "{\n") + "}"
