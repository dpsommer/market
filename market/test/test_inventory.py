import unittest

from market.data.items import Item
from market.data.actors import Actor
from market.util.data import MockData


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.test_item = Item.get('Test Item')
        self.adventurer = Actor.get('John Doe')

    def test_inventory_persistence(self):
        """
        This test does several things:
            1) ensures the inventory is persisted after a marshal save/load
            2) ensures the .get() method for GameObject instances successfully
                returns the same object after marshalling by reassigning adventurer
            3) ensures that an object held in memory matches marshaled objects
                post-load by retaining the same value for test_item
        """
        self.adventurer.add_to_inventory(self.test_item)
        MockData.save()
        MockData.load()
        self.adventurer = Actor.get('John Doe')
        self.adventurer.add_to_inventory(self.test_item)
        assert self.adventurer.get_inventory().get(self.test_item) is 2

    def test_bulk_update(self):
        """
        This test ensures the overridden bulk update function in Inventory correctly
        adds to totals rather than overriding them, and checks that new keys will be
        correctly created.
        """
        self.adventurer.add_to_inventory(self.test_item)
        potion = Item.get('Potion')
        items = {self.test_item: 3, potion: 2}
        self.adventurer.update_inventory(items)
        inventory = self.adventurer.get_inventory()
        assert inventory.get(self.test_item) is 4 and inventory.get(potion) is 2

    def test_item_removed(self):
        """
        Ensures that when an item's total reaches 0 in the inventory, it's removed.
        """
        self.adventurer.add_to_inventory(self.test_item, 2)
        self.adventurer.remove_from_inventory(self.test_item)
        assert self.adventurer.get_inventory()
        self.adventurer.remove_from_inventory(self.test_item)
        assert not self.adventurer.get_inventory()

    def tearDown(self):
        MockData.clear()


if __name__ == "__main__":
    unittest.main()
