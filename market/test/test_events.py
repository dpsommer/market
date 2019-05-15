import unittest

from market.data.events import Event, EventStream
from market.test import MockDataTestCase


def pickleable_function(x):
    print(x)


class TestEvents(MockDataTestCase):

    def test_event_stream(self):
        test_set = set()
        e = Event(lambda s: s.add('test'), 1, test_set)
        e.wait_for_completion()
        self.assertIn('test', test_set)

    def test_event_stream_pickling(self):
        e = Event(pickleable_function, 1, 'test')
        self.mock_data.save()
        e.cancel()
        self.mock_data.load()
        self.assertIn(e._id, EventStream().queue)

    def tearDown(self) -> None:
        # clearing the MockData object here removes the
        # instance from the global data map, but since
        # the event stream singleton retains its internal
        # state, it's never repopulated - instead just
        # clear the event stream queue
        EventStream()._queue.clear()


if __name__ == "__main__":
    unittest.main()
