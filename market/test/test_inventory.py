import unittest

from market.data.items import Item
from market.data.actors import Adventurer
from market.util.data import MockData


class TestInventory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MockData.load()

    def setUp(self):
        self.test_item = Item.get('Test Item')
        self.adventurer = Adventurer.get('John Doe')

    def test_inventory_persistence(self):
        self.adventurer.add_to_inventory(self.test_item, 1)
        MockData.save()
        MockData.load()
        self.adventurer = Adventurer.get('John Doe')
        self.adventurer.add_to_inventory(self.test_item, 1)
        assert self.adventurer.inventory.get(self.test_item) is 2

if __name__ == "__main__":
    unittest.main()
