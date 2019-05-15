import unittest

from market.data.items import Item
from market.data.actors import Actor
from market.test import MockDataTestCase


class TestInventory(MockDataTestCase):

    def setUp(self):
        self.test_item = Item('Test Item')
        self.adventurer = Actor('John Doe')

    def test_inventory_persistence(self):
        """
        This test does several things:
            1) ensures the inventory is persisted after a marshal save/load
            2) ensures the .get() method for GameObject instances successfully
                returns the same object after marshalling by reassigning adventurer
            3) ensures that an object held in memory matches marshaled objects
                post-load by retaining the same value for test_item
        """
        self.adventurer.inventory.add(self.test_item)
        self.mock_data.save()
        self.mock_data.load()
        self.adventurer = Actor('John Doe')
        self.adventurer.inventory.add(self.test_item)
        assert self.adventurer.inventory.get(self.test_item) is 2

    def test_bulk_update(self):
        """
        This test ensures the overridden bulk update function in Inventory correctly
        adds to totals rather than overriding them, and checks that new keys will be
        correctly created.
        """
        self.adventurer.inventory.add(self.test_item)
        potion = Item('Potion')
        items = {self.test_item: 3, potion: 2}
        self.adventurer.inventory.update(items)
        inventory = self.adventurer.inventory
        assert inventory.get(self.test_item) is 4 and inventory.get(potion) is 2

    def test_item_removed(self):
        """
        Ensures that when an item's total reaches 0 in the inventory, it's removed.
        """
        self.adventurer.inventory.add(self.test_item, 2)
        self.adventurer.inventory.remove(self.test_item)
        assert self.adventurer.inventory
        self.adventurer.inventory.remove(self.test_item)
        assert not self.adventurer.inventory


if __name__ == "__main__":
    unittest.main()
