import io
import pickle

from market.data.core import GAME_STATE


class Data:
    LOADABLE_CLASSES = GAME_STATE.keys()

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
    Mock data class for testing purposes.

    Uses in-memory data streams to hold pickled objects rather than flatfiles.
    """
    DATA_STREAMS = {cls: io.BytesIO() for cls in Data.LOADABLE_CLASSES}

    @staticmethod
    def save():
        for cls, stream in MockData.DATA_STREAMS.items():
            pickle.dump(GAME_STATE[cls], stream)

    @staticmethod
    def load():
        for cls, stream in MockData.DATA_STREAMS.items():
            try:
                GAME_STATE[cls] = pickle.load(stream)
            except EOFError:
                pass

    @staticmethod
    def clear():
        for cls, stream in MockData.DATA_STREAMS.items():
            stream.truncate()
        for k in GAME_STATE.keys():
            GAME_STATE[k] = {}
