from datetime import datetime
from typing import Callable, Any
import warnings


def time_it(loops: int = 1) -> Callable[..., Any]:
    """Decorator to time function execution time
    and print the results.

    :param loops: How many times to loop the function,
    starting and stopping the timer before and after
    each loop."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            timer = Timer(loops)
            for _ in range(loops):
                timer.start()
                result = func(*args, **kwargs)
                timer.stop()
            execution_time = timer.format_time(timer.average_elapsed_time, True)
            print(f"{func.__name__} average execution time: {execution_time}")
            return result

        return wrapper

    return decorator


class Timer:
    """Simple timer class that tracks total elapsed time
    and average time between calls to 'start' and 'stop'."""

    def __init__(
        self, averaging_window_length: int = 10, subsecond_resolution: bool = True
    ):
        """:param averaging_window_length: Number of start/stop cycles
        to calculate the average elapsed time with.

        :param subsecond_resolution: Whether to print formatted time
        strings with subsecond resolution or not."""
        self.start_time: datetime = datetime.now()
        self.stop_time: datetime = datetime.now()
        self.average_elapsed_time: float = 0
        self.history: list[float] = []
        self.elapsed_time: float = 0
        self.averaging_window_length: int = averaging_window_length
        self.started: bool = False
        self.subsecond_resolution = subsecond_resolution

    @property
    def elapsed(self) -> float:
        """Return the currently elapsed time."""
        if self.started:
            return (datetime.now() - self.start_time).total_seconds()
        else:
            return (self.stop_time - self.start_time).total_seconds()

    @property
    def elapsed_str(self) -> str:
        """Return the currently elapsed time
        as a formatted string."""
        return self.format_time(self.elapsed, self.subsecond_resolution)

    def start(self):
        """Start timer."""
        self.start_time = datetime.now()
        self.started = True

    def stop(self):
        """Stop timer.

        Calculates elapsed time and average elapsed time."""
        self.stop_time = datetime.now()
        self.started = False
        self.elapsed_time = (self.stop_time - self.start_time).total_seconds()
        self._save_elapsed_time()
        self.average_elapsed_time = sum(self.history) / (len(self.history))

    def _save_elapsed_time(self):
        """Saves current elapsed time to the history buffer
        in a FIFO manner."""
        if len(self.history) >= self.averaging_window_length:
            self.history.pop(0)
        self.history.append(self.elapsed_time)

    def current_elapsed_time(
        self, format: bool = True, subsecond_resolution: bool = False
    ) -> float | str:
        """Returns current elapsed without stopping the timer.

        :param format: If True, elapsed time is returned as a string.
        If False, elapsed time is returned as a float."""
        warnings.warn(
            "current_elapsed_time is depreciated. Use 'elapsed' and 'elapsed_str' properties instead.",
            FutureWarning,
            2,
        )
        self.elapsed_time = (datetime.now() - self.start_time).total_seconds()
        return (
            self.format_time(self.elapsed_time, subsecond_resolution)
            if format
            else self.elapsed_time
        )

    def _get_time_unit(
        self, num_seconds: float, seconds_per_unit: float, unit_suffix: str
    ) -> tuple[float, str]:
        """Determines the number of units in a given number of seconds
        by integer division.

        Returns a tuple containing the remaining number of seconds after division
        as well as the number of units as a string with 'unit_suffix' appended to the string.

        e.g. _get_time_unit(124, 60, 'm') will return (4, '2m')"""
        num_units = int(num_seconds / seconds_per_unit)
        if num_units > 0:
            remainder = num_seconds - (num_units * seconds_per_unit)
            return (remainder, f"{num_units}{unit_suffix}")
        else:
            return (num_seconds, "")

    def format_time(
        self, num_seconds: float, subsecond_resolution: bool = False
    ) -> str:
        """Returns num_seconds as a string with units.

        :param subsecond_resolution: Include milliseconds
        and microseconds with the output."""
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
            num_seconds, unit_string = self._get_time_unit(
                num_seconds, time_unit[0], time_unit[1]
            )
            if unit_string != "":
                time_string += f"{unit_string} "
        return time_string.strip()

    def get_stats(self, format: bool = True, subsecond_resolution: bool = False) -> str:
        """Returns string for elapsed time and average elapsed time.

        :param format: Times are returned as strings if True,
        otherwise they're raw floats.

        :param subsecond_resolution: Include milliseconds
        and microseconds with the output."""
        if format:
            return f"elapsed time: {self.format_time(self.elapsed_time, subsecond_resolution)}\naverage elapsed time: {self.format_time(self.average_elapsed_time, subsecond_resolution)}"
        else:
            return f"elapsed time: {self.elapsed_time}s\naverage elapsed time: {self.average_elapsed_time}s"
