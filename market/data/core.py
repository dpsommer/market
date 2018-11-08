import os
from uuid import uuid4

from market.util.data import SIMULATION_STATE


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
    SIMULATION_STATE[cls] = {}
    return cls


class SimulatedObject:
    """
    Base simulation class. Defines core functionality and class-level methods.
    """

    is_loadable = False

    def __init__(self, name, uuid=None):
        self.name = name
        self.uuid = uuid or uuid4()
        SIMULATION_STATE[self.__class__][name] = self

    @classmethod
    def get(cls, name, **kwargs):
        if name in SIMULATION_STATE[cls]:
            return SIMULATION_STATE[cls][name]
        return cls(name, **kwargs)

    @classmethod
    def get_state(cls):
        return SIMULATION_STATE[cls]

    @classmethod
    def set_state(cls, state):
        SIMULATION_STATE[cls] = state

    @classmethod
    def state_file_path(cls):
        return os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, o):
        return self.uuid == o.uuid
