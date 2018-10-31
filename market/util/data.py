import io
import pickle

from market.data.items import Item
from market.data.actors import Adventurer
from market.data.resources import Monster


class Data:

    # TODO: come up with a way to generate this list dynamically
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
                print("No datafile found for class: %s" % loadable_class.__name__)


class MockData:
    """
    Mock data class for testing purposes
    """
    DATA_STREAMS = {cls: io.BytesIO() for cls in Data.LOADABLE_CLASSES}

    @staticmethod
    def save():
        for cls, stream in MockData.DATA_STREAMS.items():
            pickle.dump(cls.REFERENCE_MAP, stream)

    @staticmethod
    def load():
        for cls, stream in MockData.DATA_STREAMS.items():
            try:
                cls.REFERENCE_MAP = pickle.load(stream)
            except EOFError:
                pass
