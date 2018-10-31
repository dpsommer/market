import pickle
from uuid import uuid4


##
# Base game class. Handles core functionality and object marshalling
##
class GameObject(object):
    MARSHAL_FILE_NAME = ''
    REFERENCE_MAP = {}

    def __init__(self, name, uuid=None):
        super(GameObject, self).__init__()
        self.name = name
        self.uuid = uuid or uuid4()
        self.__class__.REFERENCE_MAP[name] = self

    @classmethod
    def marshal_save(cls):
        with open(cls.MARSHAL_FILE_NAME, 'wb') as data_file:
            pickle.dump(cls.REFERENCE_MAP, data_file)

    @classmethod
    def marshal_load(cls):
        with open(cls.MARSHAL_FILE_NAME, 'rb') as data_file:
            try:
                cls.REFERENCE_MAP = pickle.load(data_file)
            except EOFError:
                return  # if file is empty

    def __str__(self):
        return self.name  # TODO
