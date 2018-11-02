from random import randint, uniform

from market.data.core import GameObject, loadable


class Resource(GameObject):
    DEFAULT_DROP_RATE = 50

    def __init__(self, name, drop_table=None):
        super(Resource, self).__init__(name)
        self._drop_table = drop_table or {}

    def generate_drops(self):
        drops = {}
        for drop, rate in self._drop_table.items():
            if round(uniform(0, 100), Resource.Drop.DECIMAL_PLACES) <= rate:
                drops[drop.item] = randint(drop.lower_bound, drop.upper_bound)
        return drops

    def update_drop_table(self, drops):
        self._drop_table.update(drops)

    def add_drop(self, drop, rate=DEFAULT_DROP_RATE):
        self._drop_table[drop] = rate

    class Drop:
        DECIMAL_PLACES = 3

        def __init__(self, item, lower_bound=1, upper_bound=1):
            self.item = item
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound

        def __hash__(self):
            return self.item.__hash__()  # XXX: should drops with different bounds be equal?

        def __eq__(self, o):
            return self.item == o.item

    class InvalidResourceType(Exception):
        pass


class Zone(GameObject):
    def __init__(self, name, resources=None):
        super(Zone, self).__init__(name)
        self.resources = resources or {}

    def add_resource(self, resource):
        self.resources[resource.name] = resource


@loadable
class Monster(Resource):
    def __init__(self, name, **kwargs):
        super(Monster, self).__init__(name, **kwargs)
