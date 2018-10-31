from market.data.items import Item
from market.data.actors import Adventurer
from market.data.resources import Monster


class Data:

    LOADABLE_CLASSES = [
        Item,
        Adventurer,
        Monster
    ]

    @staticmethod
    def save():
        for loadable_class in Data.LOADABLE_CLASSES:
            loadable_class.marshal_save()

    @staticmethod
    def load():
        for loadable_class in Data.LOADABLE_CLASSES:
            try:
                loadable_class.marshal_load()
            except IOError:
                print("No datafile found for class %s" % loadable_class)
