import unittest

from market.data.items import Item, InsufficientInventory
from market.data.actors import Actor, State, NotEnoughGold
from market.data.zones import Zone, Point
from market.test import MockDataTestCase


class TestActors(MockDataTestCase):

    def setUp(self) -> None:
        self.test_item = Item('Test Item')
        self.adventurer = Actor('John Doe')
        self.merchant = Actor('Item Shop', starting_gold=100)
        self.adventurer.location = Zone('Town', location=Point(0, 0))

    def test_sell_item(self):
        """
        Tests basic sell functionality.
        """
        self.adventurer.inventory.add(self.test_item)
        self.adventurer.sell(
            buyer=self.merchant,
            item=self.test_item,
            price=100
        )
        assert self.merchant.inventory.get(self.test_item)

    def test_not_enough_gold(self):
        """
        Ensures that an exception is raised when the buyer doesn't have enough gold.
        """
        self.adventurer.inventory.add(self.test_item, 2)
        self.assertRaises(
            NotEnoughGold,
            self.adventurer.sell,
            buyer=self.merchant,
            item=self.test_item,
            price=100,
            amount=2
        )

    def test_insufficient_inventory(self):
        """
        Ensures that an exception is raised when the seller has insufficient inventory,
        and that the buyer's gold remains the same as before the transaction.
        """
        buyer_gold = self.merchant.wallet.gold
        self.assertRaises(
            InsufficientInventory,
            self.adventurer.sell,
            buyer=self.merchant,
            item=self.test_item,
            price=100
        )
        assert buyer_gold == self.merchant.wallet.gold

    def test_state_change(self):
        pass

    def test_move_to_zone(self):
        forest = Zone('Forest', location=Point(0, 1))
        e = self.adventurer.move_to(forest)
        e.wait_for_completion()
        self.assertEqual(State.IDLE, self.adventurer.state)
        self.assertEqual(forest, self.adventurer.location)

    def test_hunger(self):
        pass

    def test_die_when_killed(self):
        pass


if __name__ == "__main__":
    unittest.main()
