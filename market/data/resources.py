import copy
from random import randint, uniform

from market.data.core import SimulatedObject, loadable


@loadable
class Resource(SimulatedObject):
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
        """
        Add a drop object to the resources drop table.

        :param drop: the object representing the number and type of item to drop
        :type drop: Resource.Drop
        :param rate: the rate at which the item will drop
        :type rate: int | float
        """
        self._drop_table[drop] = rate

    class Drop:
        DECIMAL_PLACES = 3

        def __init__(self, item, lower_bound=1, upper_bound=1):
            if upper_bound < lower_bound or upper_bound < 0 or lower_bound < 0:
                raise self.BoundingError("Invalid upper or lower bound defined for Drop object, "
                                         "given lower: %d, upper: %d" % (lower_bound, upper_bound))
            self.item = item
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound

        def __hash__(self):
            """
            Derived from https://stackoverflow.com/a/11742634
            """
            h = hash(self.item) * 31 + self.lower_bound
            return h * 31 + self.upper_bound

        def __eq__(self, o):
            """
            Equality comparisons for drops should check the represented item
            and both upper and lower bounds for drop amounts.

            Item objects, like all GameObjects, are compared by UUID.

            :param o: the drop to compare against
            :type o: Resource.Drop
            """
            return (self.item == o.item
                    and self.lower_bound == o.lower_bound
                    and self.upper_bound == o.upper_bound)

        class BoundingError(Exception):
            pass

    class InvalidResourceType(Exception):
        pass


@loadable
class Zone(SimulatedObject):
    def __init__(self, name, resources=None):
        super(Zone, self).__init__(name)
        self._resources = resources or {}

    def add_resource(self, resource, amount=1):
        self._resources[resource] = amount

    def remove_resource(self, resource):
        self._resources.pop(resource)

    def get_resources(self):
        return copy.deepcopy(self._resources)
