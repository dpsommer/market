import unittest

from market.core import MockData


class MockDataTestCase(unittest.TestCase):

    mock_data = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_data = MockData()

    def tearDown(self) -> None:
        self.mock_data.clear()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_data.close()
