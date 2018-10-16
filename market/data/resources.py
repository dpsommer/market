from random import randint, uniform
import os

from market.data.core import GameObject


class Resource(GameObject):

    def __init__(self, name, drop_table):
        super(Resource, self).__init__(name)
        self.drop_table = drop_table

    def generate_drops(self):
        drops = {}
        for drop, rate in self.drop_table.items():
            if round(uniform(0, 100), Resource.Drop.DECIMAL_PLACES) <= rate:
                drops[drop.item] = randint(drop.lower_bound, drop.upper_bound)
        return drops

    class Drop:
        DECIMAL_PLACES = 3

        def __init__(self, item, lower_bound=1, upper_bound=1):
            self.item = item
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound

    class InvalidResourceType(Exception):
        pass


class Zone(GameObject):

    def __init__(self, name):
        super(Zone, self).__init__(name)
        self.resources = {}

    def add_resource(self, resource):
        self.resources[resource.name] = resource


class Monster(Resource):

    MARSHAL_FILE_NAME = os.path.join(os.path.dirname(__file__), 'monsters.json')

    def __init__(self, name, drop_table):
        super(Monster, self).__init__(name, drop_table)
