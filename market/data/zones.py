import copy
import random

from market.core import SimulatedObject, SimulatedSingleton, loadable


DEFAULT = '__default__'
WIDTH = 100
HEIGHT = 100
MARGIN = 10


class Point(object):

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash('{}{}'.format(self.x, self.y))


@loadable
class Map(SimulatedSingleton):

    def __init__(self):
        super().__init__()
        if not self.initialized:
            self._zones = {}
            self._width = WIDTH
            self._height = HEIGHT
            self._existing_locations = {}  # set of used Points

    def add_zone(self, zone, location=None):
        location = location or Point(
            random.randint(-(self._width // 2), self._width // 2),
            random.randint(-(self._height // 2), self._height // 2)
        )

        # width and height of the world map are dynamic;
        # when a new location is added, grow the size if
        # the zone falls within the map's margin
        if location.x > abs((self._width - MARGIN) // 2):
            self._width += MARGIN
        if location.y > abs((self._height - MARGIN) // 2):
            self._height += MARGIN

        # check to ensure zone isn't colliding with existing zones
        if location not in self._existing_locations:
            self._zones[zone] = location

    def distance(self, from_zone, to_zone):
        p1 = self._zones[from_zone]
        p2 = self._zones[to_zone]
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)


world_map = Map()


@loadable
class Zone(SimulatedObject):

    # TODO: later on, multiple routes or roads could be an
    #       interesting addition - actors could choose
    #       which route to take based on their needs
    def __init__(self, name, resources=None, location: Point = None):
        super(Zone, self).__init__(name)
        if not self.initialized:
            self._resources = resources or {}
            world_map.add_zone(self, location)

    def add_resource(self, resource, amount=1):
        self._resources[resource] = amount

    def remove_resource(self, resource):
        self._resources.pop(resource)

    def get_resources(self):
        return copy.deepcopy(self._resources)


class CircularRoute(Exception):
    pass
