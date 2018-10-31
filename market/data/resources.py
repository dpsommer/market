from random import randint, uniform
import os

from market.data.core import GameObject


class Resource(GameObject):

    DEFAULT_DROP_RATE = 50

    def __init__(self, drop_table=None, **kwargs):
        super(Resource, self).__init__(**kwargs)
        self.drop_table = drop_table or {}

    def generate_drops(self):
        drops = {}
        for drop, rate in self.drop_table.items():
            if round(uniform(0, 100), Resource.Drop.DECIMAL_PLACES) <= rate:
                drops[drop.item] = randint(drop.lower_bound, drop.upper_bound)
        return drops

    def update_drop_table(self, drops):
        self.drop_table.update(drops)

    def add_drop(self, drop, rate=DEFAULT_DROP_RATE):
        self.drop_table[drop] = rate

    class Drop:
        DECIMAL_PLACES = 3

        def __init__(self, item, lower_bound=1, upper_bound=1):
            self.item = item
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound

    class InvalidResourceType(Exception):
        pass


class Zone(GameObject):

    def __init__(self, resources=None, **kwargs):
        super(Zone, self).__init__(**kwargs)
        self.resources = resources or {}

    def add_resource(self, resource):
        self.resources[resource.name] = resource


class Monster(Resource):

    MARSHAL_FILE_NAME = os.path.join(os.path.dirname(__file__), 'monsters.json')
    REFERENCE_MAP = {}

    def __init__(self, **kwargs):
        super(Monster, self).__init__(**kwargs)
