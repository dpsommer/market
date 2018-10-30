import json
from uuid import uuid4


##
# Base game class. Handles core functionality and object marshalling
##
class GameObject(json.JSONEncoder):

    MARSHAL_FILE_NAME = ''
    REFERENCE_MAP = {}

    def __init__(self, name):
        super(GameObject, self).__init__()
        self.uuid = uuid4()
        self.name = name
        self.__class__.REFERENCE_MAP[name] = self

    def default(self, o):
        return {
            'uuid': o.uuid,
            'name': o.name
        }

    @classmethod
    def marshal_save(cls, values):
        with open(cls.MARSHAL_FILE_NAME, 'w') as data_file:
            json.dump(values.values(), data_file, cls=cls)

    @classmethod
    def marshal_load(cls):
        with open(cls.MARSHAL_FILE_NAME) as data_file:
            objects = json.load(data_file)
        for o in objects:
            cls.REFERENCE_MAP[o['name']] = cls(o['name'])

    def __str__(self):
        return self.name
