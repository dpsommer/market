import io
import importlib
import pickle
import pkgutil
import pyclbr

from market import data as data_module
from market.data.core import GameObject, GAME_DATA


def find_loadable_classes(package):
    """
    Recursively walk through the given package and find all loadable GameObject subclasses.

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: list[GameObject]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    loadable_classes = []
    for loader, name, is_pkg in pkgutil.walk_packages(path=package.__path__):
        full_name = package.__name__ + '.' + name
        module = importlib.import_module(full_name)
        # get name here because returned values are pyclbr class objects
        cls = [_.name for _ in pyclbr.readmodule(full_name).values()]
        for class_name in cls:
            c = getattr(module, class_name)
            if issubclass(c, GameObject) and c.is_loadable:
                loadable_classes.append(c)
        if is_pkg:
            return loadable_classes + find_loadable_classes(full_name)
    return loadable_classes


class Data:

    LOADABLE_CLASSES = find_loadable_classes(data_module)

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
            pickle.dump(GAME_DATA[cls.__name__], stream)

    @staticmethod
    def load():
        for cls, stream in MockData.DATA_STREAMS.items():
            try:
                GAME_DATA[cls.__name__] = pickle.load(stream)
            except EOFError:
                pass
