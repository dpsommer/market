import time

from market.util.threading import TimerThread


# How long it takes for an hour to pass in simulation time
# @1/360  - 1 hour = 10 seconds; 1 day = 4 minutes; 1 week = 28 minutes; 1 year = 1460 minutes = ~61 hours = ~2.5 days
# @1/3600 - 1 hour = 1 second; 1 day = 24 seconds; 1 week = 168 seconds; 1 year = ~145 minutes = ~2.5 hours
TIME_SCALE = 1 / 3600
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY


# XXX: not sure if this is the right place for this class
# XXX: it might be better to use events for this?
class SimulationTimer(TimerThread):

    def __init__(self, completion_callback, callback_arguments=[], days_to_simulate=365):
        super().__init__(
            ticks=days_to_simulate,
            seconds_per_tick=SECONDS_PER_DAY * TIME_SCALE,
            callback=self.decrement_day_count
        )
        self.days_remaining = days_to_simulate
        self.on_complete = completion_callback
        self.args = callback_arguments
        self._zero = time.time()

    def decrement_day_count(self):
        pass

    def time_of_day(self):
        seconds_since_zero = time.time() - self._zero
        _, t = divmod(seconds_since_zero, SECONDS_PER_DAY * TIME_SCALE)
        return divmod(t, (SECONDS_PER_DAY * TIME_SCALE) / HOURS_PER_DAY)

    def stop(self):
        super().stop()
        self.on_complete(*self.args)
