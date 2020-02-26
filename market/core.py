import io
import os
import pickle


# TODO: pickle random
# TODO: switch to JSON?

# TODO: it might be better to simply pickle the simulation state itself?
class Data(object):

    simulation_state = {}

    def __init__(self):
        raise TypeError('Non-instantiable type')

    @staticmethod
    def save():
        for loadable_class in Data.simulation_state.keys():
            with open(loadable_class.state_file_path(), 'wb') as data_file:
                pickle.dump(Data.simulation_state[loadable_class], data_file, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load():
        for loadable_class in Data.simulation_state.keys():
            try:
                with open(loadable_class.state_file_path(), 'rb') as data_file:
                    Data.simulation_state[loadable_class] = pickle.load(data_file)
            except EOFError:
                pass  # if file is empty
            except IOError:
                print("No datafile found for class: %s" % loadable_class.__name__)


class MockData(object):
    """
    Mock data class for testing purposes.

    Uses in-memory data streams to hold pickled objects rather than flatfiles.
    """
    def __init__(self):
        self._data_streams = {cls: io.BytesIO() for cls in Data.simulation_state.keys()}

    def save(self):
        for cls, stream in self._data_streams.items():
            pickle.dump(Data.simulation_state[cls], stream, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        for k in Data.simulation_state.keys():
            Data.simulation_state[k] = {}
        for cls, stream in self._data_streams.items():
            try:
                stream.seek(0)
                Data.simulation_state[cls] = pickle.load(stream)
            except EOFError:
                pass

    def clear(self):
        for stream in self._data_streams.values():
            stream.truncate()
        # retain keys but clear state contents
        for k in Data.simulation_state.keys():
            Data.simulation_state[k] = {}

    def close(self):
        for stream in self._data_streams.values():
            stream.close()


class SimulatedObject(object):
    """
    Base simulation class. Defines core functionality and class-level methods.
    """

    __default__ = '__default__'

    is_loadable = False

    # XXX: is it possible that at some point we'll want multiple objects
    #      to be able to have the same name? should we be using uuid after all?
    def __init__(self, name, **kwargs):
        self._name = name

    # XXX: this is way too complicated. It might be better to go back to the
    #      get() implementation than deal with all the extra boilerplate and
    #      exception cases this causes.
    def __new__(cls, name=None, *args, **kwargs):
        name = name or cls.__default__
        if cls.is_loadable and name in Data.simulation_state[cls]:
            instance = Data.simulation_state[cls][name]
            instance.initialized = True
            return instance
        instance = super().__new__(cls)
        instance._name = name  # necessary as pickle.load() doesn't call __init__
        instance.initialized = False
        Data.simulation_state[cls][name] = instance
        return instance

    @classmethod
    def state_file_path(cls):
        return os.path.join(os.path.dirname(__file__), '%s.p' % cls.__name__)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __getnewargs__(self):
        return self.name,

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o):
        return self.name == o.name


class SimulatedSingleton(SimulatedObject):

    __instance__ = None

    def __init__(self, *args, **kwargs):
        if not self.__instance__:
            raise TypeError("No instance of singleton class {}".format(self.__class__))
        super().__init__(name=self.__instance__.name)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super().__new__(cls, name=cls.__default__)
        return cls.__instance__


def loadable(cls: SimulatedObject) -> SimulatedObject:
    """
    Class decorator for loadable SimulatedObject subclasses.
    Defines the class as a pickle target for marshal save/load.

    As a side-effect, adds the calling class the global simulation state dict for simplicity.

    :param cls: the class being decorated
    :return: the decorated class
    """
    cls.is_loadable = True
    Data.simulation_state[cls] = {}
    return cls
