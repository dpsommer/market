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
        assert self.adventurer.get_inventory().get(self.test_item) is 2

    def test_bulk_update(self):
        self.adventurer.add_to_inventory(self.test_item, 1)
        potion = Item.get('Potion')
        items = {self.test_item: 3, potion: 2}
        self.adventurer.update_inventory(items)
        inventory = self.adventurer.get_inventory()
        assert inventory.get(self.test_item) is 4 and inventory.get(potion) is 2

    def tearDown(self):
        self.adventurer.clear_inventory()

if __name__ == "__main__":
    unittest.main()
