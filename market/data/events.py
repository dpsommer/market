import asyncio
import sched

from market.core import SimulatedSingleton, loadable


@loadable
class EventStream(SimulatedSingleton, sched.scheduler):

    def __init__(self):
        SimulatedSingleton.__init__(self)

    def __new__(cls, *args, **kwargs):
        if cls.__instance__:
            return cls.__instance__
        o = SimulatedSingleton.__new__(cls)
        sched.scheduler.__init__(o)
        return o


class Event(object):

    def __init__(self, callback: callable, duration: int, *args, **kwargs):
        self._callback = callback
        self._args, self._kwargs = args, kwargs
        self._event_stream = EventStream()
        self._id = self._event_stream.enter(
            delay=duration,
            priority=1,
            action=callback,
            argument=tuple(args),
            kwargs=kwargs
        )
        loop = asyncio.get_event_loop() or asyncio.new_event_loop()
        loop.run_in_executor(None, self._event_stream.run)  # passing None uses default executor

    def cancel(self):
        self._event_stream.cancel(self._id)

    def wait_for_completion(self):
        while self._id in self._event_stream.queue:
            pass
