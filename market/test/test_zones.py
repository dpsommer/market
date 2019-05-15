import unittest

from market.data.zones import Zone, world_map
from market.test import MockDataTestCase


class TestZones(MockDataTestCase):

    def test_seeded_map_generation(self):
        pass

    def test_add_zone_to_map(self):
        town = Zone('Town')
        world_map.add_zone(town)
        self.assertIn(town, world_map._zones)

    def test_dynamic_map_expansion(self):
        pass

    def test_zone_persistence(self):
        pass


if __name__ == "__main__":
    unittest.main()
