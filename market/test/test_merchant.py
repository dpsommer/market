import unittest

from market.data.items import Item, Inventory
from market.data.actors import Actor, Adventurer, Merchant
from market.util.data import MockData


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.test_item = Item.get('Test Item')
        self.adventurer = Adventurer.get('John Doe')
        self.merchant = Merchant.get('Item Shop', buy_list={self.test_item: 100}, starting_gold=100)

    def test_sell_item(self):
        """
        Tests basic sell functionality and that the merchant's prices are updated
        when their inventory changes.
        """
        self.adventurer.add_to_inventory(self.test_item)
        self.adventurer.sell(
            buyer=self.merchant,
            item=self.test_item,
            price=self.merchant.get_buy_list()[self.test_item]
        )
        assert self.merchant.get_prices()[self.test_item]

    def test_not_enough_gold(self):
        """
        Ensures that an exception is raised when the buyer doesn't have enough gold.
        """
        self.adventurer.add_to_inventory(self.test_item, 2)
        self.assertRaises(
            Actor.NotEnoughGold,
            self.adventurer.sell,
            buyer=self.merchant,
            item=self.test_item,
            price=self.merchant.get_buy_list()[self.test_item],
            amount=2
        )

    def test_insufficient_inventory(self):
        """
        Ensures that an exception is raised when the seller has insufficient inventory,
        and that the buyer's gold remains the same as before the transaction.
        """
        buyer_gold = self.merchant.get_gold_total()
        self.assertRaises(
            Inventory.InsufficientInventory,
            self.adventurer.sell,
            buyer=self.merchant,
            item=self.test_item,
            price=self.merchant.get_buy_list()[self.test_item],
        )
        assert buyer_gold == self.merchant.get_gold_total()

    def tearDown(self):
        MockData.clear()


if __name__ == "__main__":
    unittest.main()
