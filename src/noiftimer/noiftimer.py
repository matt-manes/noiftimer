import time
from typing import Any, Callable

from typing_extensions import Self


def time_it(loops: int = 1) -> Callable[..., Any]:
    """Decorator to time function execution time and print the results.

    #### :params:

    `loops`: How many times to execute the decorated function,
    starting and stopping the timer before and after each loop."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            timer = Timer(loops)
            result = None
            for _ in range(loops):
                timer.start()
                result = func(*args, **kwargs)
                timer.stop()
            print(
                f"{func.__name__} average execution time: {timer.average_elapsed_str}"
            )
            return result

        return wrapper

    return decorator


class _Pauser:
    def __init__(self):
        self._pause_start = 0
        self._pause_total = 0
        self._paused = False

    def pause(self):
        self._pause_start = time.time()
        self._paused = True

    def unpause(self):
        self._pause_total += time.time() - self._pause_start
        self._paused = False

    def reset(self):
        self._pause_start = 0
        self._pause_total = 0
        self._paused = False

    @property
    def pause_total(self) -> float:
        if self._paused:
            return self._pause_total + (time.time() - self._pause_start)
        else:
            return self._pause_total


class Timer:
    """Simple timer class that tracks total elapsed time
    and average time between calls to `start()` and `stop()`."""

    def __init__(
        self, averaging_window_length: int = 10, subsecond_resolution: bool = True
    ):
        """
        #### :params:
        * `averaging_window_length`: Number of start/stop cycles to calculate the average elapsed time with.

        * `subsecond_resolution`: Whether to print formatted time strings with subsecond resolution or not."""
        self._start_time = time.time()
        self._stop_time = self.start_time
        self._elapsed = 0
        self._average_elapsed = 0
        self._history: list[float] = []
        self._started: bool = False
        self.averaging_window_length: int = averaging_window_length
        self.subsecond_resolution = subsecond_resolution
        self._pauser = _Pauser()

    @property
    def started(self) -> bool:
        """Returns whether the timer has been started and is currently running."""
        return self._started

    @property
    def elapsed(self) -> float:
        """Returns the currently elapsed time."""
        if self._started:
            return time.time() - self._start_time - self._pauser.pause_total
        else:
            return self._elapsed

    @property
    def elapsed_str(self) -> str:
        """Returns the currently elapsed time as a formatted string."""
        return self.format_time(self.elapsed, self.subsecond_resolution)

    @property
    def average_elapsed(self) -> float:
        """Returns the average elapsed time."""
        return self._average_elapsed

    @property
    def average_elapsed_str(self) -> str:
        """Returns the average elapsed time as a formatted string."""
        return self.format_time(self._average_elapsed, self.subsecond_resolution)

    @property
    def start_time(self) -> float:
        """Returns the timestamp of the last call to `start()`."""
        return self._start_time

    @property
    def stop_time(self) -> float:
        """Returns the timestamp of the last call to `stop()`."""
        return self._stop_time

    @property
    def history(self) -> list[float]:
        """Returns the history buffer for this timer.

        At most, it will be `averaging_window_length` elements long."""
        return self._history

    def start(self: Self) -> Self:
        """Start the timer.

        Returns this Timer instance so timer start can be chained to Timer creation if desired.

        >>> timer = Timer().start()"""
        if not self.started:
            self._start_time = time.time()
            self._started = True
        return self

    def stop(self):
        """Stop the timer.

        Calculates elapsed time and average elapsed time."""
        if self.started:
            self._stop_time = time.time()
            self._started = False
            self._elapsed = (
                self._stop_time - self._start_time - self._pauser.pause_total
            )
            self._pauser.reset()
            self._save_elapsed_time()
            self._average_elapsed = sum(self._history) / (len(self._history))

    def pause(self):
        """Pause the timer."""
        self._pauser.pause()

    def unpause(self):
        """Unpause the timer."""
        self._pauser.unpause()

    def _save_elapsed_time(self):
        """Saves current elapsed time to the history buffer in a FIFO manner."""
        if len(self._history) >= self.averaging_window_length:
            self._history.pop(0)
        self._history.append(self._elapsed)

    @staticmethod
    def format_time(num_seconds: float, subsecond_resolution: bool = False) -> str:
        """Returns `num_seconds` as a string with units.

        #### :params:

        `subsecond_resolution`: Include milliseconds and microseconds with the output."""
        microsecond = 0.000001
        millisecond = 0.001
        second = 1
        seconds_per_minute = 60
        seconds_per_hour = 3600
        seconds_per_day = 86400
        seconds_per_week = 604800
        seconds_per_month = 2419200
        seconds_per_year = 29030400
        time_units = [
            (seconds_per_year, "y"),
            (seconds_per_month, "mn"),
            (seconds_per_week, "w"),
            (seconds_per_day, "d"),
            (seconds_per_hour, "h"),
            (seconds_per_minute, "m"),
            (second, "s"),
            (millisecond, "ms"),
            (microsecond, "us"),
        ]
        if not subsecond_resolution:
            time_units = time_units[:-2]
        time_string = ""
        for time_unit in time_units:
            unit_amount, num_seconds = divmod(num_seconds, time_unit[0])
            if unit_amount > 0:
                time_string += f"{int(unit_amount)}{time_unit[1]} "
        if time_string == "":
            return f"<1{time_units[-1][1]}"
        return time_string.strip()

    @property
    def stats(self) -> str:
        """Returns a string stating the currently elapsed time and the average elapsed time."""
        return f"elapsed time: {self.elapsed_str}\naverage elapsed time: {self.average_elapsed_str}"
