from enum import IntEnum

from market.core import SimulatedObject, loadable
from market.data.items import Item, Inventory, Wallet, InsufficientInventory, NotEnoughGold
from market.data.resources import Resource
from market.data.zones import Zone, world_map
from market.data.events import Event


class HierarchyOfNeeds(IntEnum):

    def __new__(cls, value, default=100., modifier=0.):
        obj = int.__new__(cls)
        obj._value_ = value
        obj.default = default
        obj.modifier = modifier
        return obj

    @property
    def tier(self):
        return self._value_ // 100

    FOOD = 100, 100., -.2
    WATER = 101, 100., -1.4
    SHELTER = 102, 100., -.05
    SLEEP = 103, 100., -2.5

    SAFETY = 200
    FINANCE = 201, 50.
    HEALTH = 202

    FRIENDS = 300, 50.
    FAMILY = 301, 50.
    LOVE = 302, 50.

    GOALS = 400, 0.
    CAREER = 401, 0.
    FULFILLMENT = 402, 0.


class State(IntEnum):
    IDLE = 0
    EAT = 1
    SLEEP = 2
    TRAVEL = 3
    WORK = 4
    FIGHT = 5
    DEATH = 6


ON_FOOT = 1
CARRIAGE = 2
HORSE = 3

# TODO: determine this based on the global time scale
TICK_INTERVAL = 5


@loadable
class Actor(SimulatedObject):

    def __init__(self, name: str,
                 starting_gold: int = 0,
                 starting_inventory: Inventory = None,
                 priorities: dict = None,
                 location: Zone = None):
        super().__init__(name)
        # gross hack to prevent from overwriting existing values post-pickle
        # or when an object is re-instantiated (identical name)
        if not self.initialized:
            self.state = State.IDLE
            self.travel_speed = ON_FOOT
            self.priorities = priorities or self.default_priorities()
            self.wallet = Wallet(starting_gold)
            self.inventory = starting_inventory or Inventory()
            self.location = location
            Event(self.update_priorities, TICK_INTERVAL)

    @staticmethod
    def default_priorities() -> dict:
        return {n.name.capitalize(): Priority(value=n.default, tier=n.tier, modifier=n.modifier)
                for n in HierarchyOfNeeds}

    def update_priorities(self):
        print(f"Updating priorities for actor {self.name}")
        # TODO: change modifiers based on state
        for p in self.priorities.values():
            p.value += p.modifier
        Event(self.update_priorities, TICK_INTERVAL)

    def move_to(self, zone: Zone) -> Event:
        self.state = State.TRAVEL
        # TODO: align this with actual values based on the global time scale
        travel_time = world_map.distance(self.location, zone) / self.travel_speed
        # TODO: how do we update priorities during travel?
        # TODO: should events be able to be paused?
        return Event(self.update_location, travel_time, zone)

    def gather(self, resource: Resource):
        drops = resource.generate_drops()
        for drop, amount in drops.items():
            self.inventory.add(drop, amount)

    def determine_price(self, item):
        # TODO: based on perceived supply/demand and individual valuation,
        #       determine the price of an item for purchase or sale
        #       Should operate the same whether buying or selling;
        #       then compare values for buyer/seller and judge price
        #       point from there.
        #       For example: if a wounded adventurer is in desperate
        #       need of a healing potion, they may place a premium
        #       on it - a merchant may take advantage of this.
        #       Use the seller's price when determining the
        #       final sale price.
        pass

    def buy(self, seller, item: Item, price: int, amount: int = 1):
        """
        Buy some number of goods from another actor for a set price.

        :param seller: the actor to buy from
        :param item: the item to purchase
        :param price: the price at which to buy items. XXX: should this be dynamic?
        :param amount: the number of items to buy
        """
        try:
            # TODO: determine the price using the above function rather than passing it
            self.wallet.remove(price * amount)
            seller.inventory.remove(item, amount)
            seller.wallet.add(price * amount)
            self.inventory.add(item, amount)
        except InsufficientInventory as e:
            # FIXME: this works as a stop-gap, but it would be better to have a proper transaction here
            #        e.g. pickle state for buyer and seller to memory, recover on failure
            self.wallet.add(price * amount)
            raise e
        except NotEnoughGold as e:
            raise e

    def sell(self, buyer, item: Item, price: int, amount: int = 1):
        buyer.buy(self, item, price, amount)

    def update_location(self, zone: Zone):
        self.state = State.IDLE
        self.location = zone


class Priority:
    """
    Defines actor priorities based on Maslow's hierarchy: food, water, shelter, etc.

    Each priority is defined as a float value between 0.0 and 100.0 and an integer tier.

    The value of the priority indicates how well the priority is currently fulfilled,
    while the tier represents the order in which an actor will attempt to fulfill
    each priority.
    """

    def __init__(self, value=50., tier=1, modifier=0.):
        self.value = value
        self.tier = tier
        self.modifier = modifier

    def __str__(self):
        return 'Tier: {}\tValue: {}'.format(self.tier, self.value)
