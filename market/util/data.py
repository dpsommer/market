import io
import pickle
import random

SIMULATION_STATE = {}


class Data:
    LOADABLE_CLASSES = SIMULATION_STATE.keys()

    @staticmethod
    def save():
        # TODO: pickle random state
        for loadable_class in Data.LOADABLE_CLASSES:
            with open(loadable_class.state_file_path(), 'wb') as data_file:
                pickle.dump(loadable_class.get_state(), data_file)

    @staticmethod
    def load():
        for loadable_class in Data.LOADABLE_CLASSES:
            try:
                with open(loadable_class.state_file_path(), 'rb') as data_file:
                    loadable_class.set_state(pickle.load(data_file))
            except EOFError:
                pass  # if file is empty
            except IOError:
                print("No datafile found for class: %s" % loadable_class.__name__)

    @staticmethod
    def generate():
        pass  # TODO: also need to pickle random state


class MockData:
    """
    Mock data class for testing purposes.

    Uses in-memory data streams to hold pickled objects rather than flatfiles.
    """
    DATA_STREAMS = {cls: io.BytesIO() for cls in Data.LOADABLE_CLASSES}
    SEED = 'mock data'

    @staticmethod
    def save():
        for cls, stream in MockData.DATA_STREAMS.items():
            pickle.dump(SIMULATION_STATE[cls], stream)

    @staticmethod
    def load():
        for cls, stream in MockData.DATA_STREAMS.items():
            try:
                SIMULATION_STATE[cls] = pickle.load(stream)
            except EOFError:
                pass

    @staticmethod
    def clear():
        for cls, stream in MockData.DATA_STREAMS.items():
            stream.truncate()
        for k in SIMULATION_STATE.keys():
            SIMULATION_STATE[k] = {}

    @staticmethod
    def generate():
        random.seed = MockData.SEED
        Data.generate()
