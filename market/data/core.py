import os
import pickle
from uuid import uuid4


GAME_DATA = {}


def loadable(cls):
    cls.is_loadable = True
    return cls


class GameObject:
    """
    Base game class. Handles core functionality and object marshalling using pickle.

    XXX: all the calls to .__name__ here are ugly
    """

    is_loadable = False

    def __init__(self, name, uuid=None):
        self.name = name
        self.uuid = uuid or uuid4()
        class_name = self.__class__.__name__
        if class_name not in GAME_DATA:
            GAME_DATA[class_name] = {}
        GAME_DATA[self.__class__.__name__][name] = self

    @classmethod
    def get(cls, name):
        if cls.__name__ not in GAME_DATA:
            GAME_DATA[cls.__name__] = {}
        if name in GAME_DATA[cls.__name__]:
            return GAME_DATA[cls.__name__][name]
        return cls(name)

    @classmethod
    def marshal_save(cls):
        with open(os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__), 'wb') as data_file:
            pickle.dump(GAME_DATA[cls.__name__], data_file)

    @classmethod
    def marshal_load(cls):
        with open(os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__), 'rb') as data_file:
            try:
                GAME_DATA[cls.__name__] = pickle.load(data_file)
            except EOFError:
                pass  # if file is empty

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, o):
        return self.uuid == o.uuid
