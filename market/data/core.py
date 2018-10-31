import json
from uuid import uuid4, UUID


##
# Base game class. Handles core functionality and object marshalling
##
class GameObject(json.JSONEncoder):
    MARSHAL_FILE_NAME = ''
    REFERENCE_MAP = {}

    def __init__(self, name='', uuid=None, **kwargs):
        super(GameObject, self).__init__(**kwargs)
        self.name = name
        self.uuid = uuid or uuid4()
        self.__class__.REFERENCE_MAP[self.name] = self

    def default(self, o):
        if isinstance(o, GameObject):
            return {
                'uuid': o.uuid,
                'name': o.name
            }
        elif isinstance(o, UUID):
            return str(o)
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            # TODO: handle various iterable types
            return list(iterable)
        return json.JSONEncoder.default(self, o)

    @classmethod
    def marshal_save(cls, values):
        with open(cls.MARSHAL_FILE_NAME, 'w') as data_file:
            json.dump(values.values(), data_file, cls=cls)

    @classmethod
    def marshal_load(cls):
        with open(cls.MARSHAL_FILE_NAME) as data_file:
            try:
                objects = json.load(data_file)
            except json.JSONDecodeError:
                return  # if file is empty
        for o in objects:
            # TODO: get uuids from loaded objects as well
            cls.REFERENCE_MAP[o['name']] = cls(name=o['name'])

    def __str__(self):
        return self.name
