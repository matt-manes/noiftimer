import time

import pytest

import noiftimer


def test_noiftimer_start():
    timer = noiftimer.Timer().start()
    assert timer.start_time
    assert timer.started is True


def test_noiftimer_stop():
    timer = noiftimer.Timer()
    timer.start()
    time.sleep(2)
    timer.stop()
    assert timer.stop_time
    assert not timer.started
    assert timer.elapsed > 1
    assert timer.elapsed == timer.average_elapsed


def test_noiftimer_reset():
    timer = noiftimer.Timer()
    timer.start()
    for i in range(5):
        timer.reset()
    assert len(timer.history) == 5


def test_noiftimer__save_elapsed_time():
    averaging_window_length = 10
    timer = noiftimer.Timer(averaging_window_length)
    timer.start()
    timer.stop()
    assert len(timer.history) == 1
    for _ in range(averaging_window_length * 2):
        timer.start()
        timer.stop()
    assert len(timer.history) == averaging_window_length


def test_noiftimer_current_elapsed_time():
    timer = noiftimer.Timer().start()
    time.sleep(1)
    elapsed_time = timer.elapsed
    time.sleep(1)
    assert 0 < elapsed_time and elapsed_time < timer.elapsed


def test__noiftimer__elapsed():
    timer = noiftimer.Timer()
    timer.start()
    time.sleep(1)
    elapsed = timer.elapsed
    time.sleep(1)
    assert 0 < elapsed and elapsed < timer.elapsed
    time.sleep(1)
    timer.stop()
    assert timer.elapsed


def test__noiftimer__elapsed_str():
    timer = noiftimer.Timer()
    timer.start()
    time.sleep(1)
    assert type(timer.elapsed_str) == str
    assert timer.elapsed_str != ""


@pytest.mark.parametrize(
    "num_seconds,subsecond_resolution,expected",
    [
        (3600, False, "1h"),
        (1800, False, "30m"),
        (5400, False, "1h 30m"),
        (
            (29030400) + (604800 * 2) + (3600 * 3) + (44.250043),
            True,
            "1y 2w 3h 44s 250ms 43us",
        ),
        (
            (29030400) + (604800 * 2) + (3600 * 3) + (44.250043),
            False,
            "1y 2w 3h 44s",
        ),
    ],
)
def test_noiftimer_format_time(
    num_seconds: float, subsecond_resolution: bool, expected: float
):
    assert noiftimer.Timer.format_time(num_seconds, subsecond_resolution) == expected


def test_noiftimer_get_stats():
    timer = noiftimer.Timer()
    timer.start()
    time.sleep(1)
    timer.stop()
    assert timer.stats


def test__noiftimer__time_it():
    @noiftimer.time_it(10)
    def zzz():
        time.sleep(0.1)
        return True

    assert zzz()


def test__pauser():
    pauser = noiftimer.noiftimer._Pauser()  # type: ignore
    assert not pauser.paused
    assert pauser.pause_total == 0
    pauser.pause()
    assert pauser.paused
    time.sleep(1.1)
    pauser.unpause()
    assert not pauser.paused
    assert pauser.pause_total > 1
    pauser.reset()
    assert pauser.pause_total == 0


def test__Timer_pause():
    timer = noiftimer.Timer().start()
    time.sleep(1)
    elapsed_time = timer.elapsed
    timer.pause()
    assert timer.is_paused
    time.sleep(1)
    # amount of time paused should be subtracted from elapsed
    assert elapsed_time == timer.elapsed
    timer.unpause()
    time.sleep(1)
    # pause tracker should be stopped
    assert timer.elapsed > elapsed_time
    timer.pause()
    time.sleep(1)
    timer.unpause()
