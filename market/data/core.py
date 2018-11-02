import os
import pickle
from uuid import uuid4

GAME_STATE = {}


def loadable(cls):
    """
    Class decorator for loadable GameObject subclasses.
    Defines the class as a pickle target for marshal save/load.

    As a side-effect, adds the calling class the global GAME_STATE dict for simplicity.

    :param cls: the class being decorated
    :type cls: class[GameObject]
    :return: the decorated class
    :rtype: class[GameObject]
    """
    cls.is_loadable = True
    GAME_STATE[cls] = {}
    return cls


class GameObject:
    """
    Base game class. Handles core functionality and object marshalling using pickle.
    """

    is_loadable = False

    def __init__(self, name, uuid=None):
        self.name = name
        self.uuid = uuid or uuid4()
        GAME_STATE[self.__class__][name] = self

    @classmethod
    def get(cls, name, **kwargs):
        if name in GAME_STATE[cls]:
            return GAME_STATE[cls][name]
        return cls(name, **kwargs)

    @classmethod
    def marshal_save(cls):
        with open(os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__), 'wb') as data_file:
            pickle.dump(GAME_STATE[cls], data_file)

    @classmethod
    def marshal_load(cls):
        with open(os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__), 'rb') as data_file:
            try:
                GAME_STATE[cls] = pickle.load(data_file)
            except EOFError:
                pass  # if file is empty

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, o):
        return self.uuid == o.uuid
