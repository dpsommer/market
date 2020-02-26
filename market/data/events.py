import asyncio
from time import monotonic
from threading import RLock
from uuid import uuid4

from market.core import SimulatedSingleton, loadable
from market.util.threading import TimerThread


# need to track time remaining before the event pops
# rather than timestamps so unpickling later doesn't
# fire all events at the same time.
@loadable
class EventStream(SimulatedSingleton, TimerThread):

    def __init__(self):
        SimulatedSingleton.__init__(self)

    def __new__(cls, *args, **kwargs):
        if cls.__instance__:
            return cls.__instance__
        o = SimulatedSingleton.__new__(cls)
        o.events = set()
        o._lock = RLock()
        TimerThread.__init__(
            o,
            ticks=-1,  # Repeat until stopped
            seconds_per_tick=1,
            callback=o._event_tick
        )
        o.start()
        return o

    def _event_tick(self):
        with self._lock:
            completed_events = set()
            for e in self.events:
                if e.time <= monotonic():
                    completed_events.add(e)
            # this step needs to be separate in case
            # the callback creates a new Event, as 
            # this would cause a thread collision
            for e in completed_events:
                e.callback(*e.args, **e.kwargs)
                self.events.remove(e)

    def schedule(self, event):
        with self._lock:
            self.events.add(event)

    def empty(self):
        with self._lock:
            return len(self.events) == 0

    def cancel(self, e):
        with self._lock:
            self.events.remove(e)

    def clear(self):
        with self._lock:
            self.events.clear()

    def _stop(self):
        self._lock.release()
        super()._stop()

    def __contains__(self, i):
        with self._lock:
            return i in self.events

    def __getstate__(self):
        with self._lock:
            return self.events

    def __setstate__(self, events):
        self.events = events


class Event(object):

    def __init__(self, callback: callable, duration: int, *args, **kwargs):
        self._id = uuid4()
        self.callback = callback
        self.args, self.kwargs = args, kwargs
        self.time = monotonic() + duration
        self._event_stream = EventStream()
        self._event_stream.schedule(self)

    def cancel(self):
        self._event_stream.cancel(self)

    def wait_for_completion(self):
        while self in self._event_stream.events:
            pass

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, o):
        return self._id == o._id

    def __getstate__(self):
        now = monotonic()  # calculate the remaining time before the event fires
        return (self._id, self.args, self.kwargs, self.callback, self.time - now)

    def __setstate__(self, state):
        self._event_stream = EventStream()
        self._id, self.args, self.kwargs, self.callback, self.time = state
        self.time += monotonic()
