import pytest
from src.core.timer import PomodoroTimer

def test_timer_initialization():
    timer = PomodoroTimer()
    assert timer.work_duration == 25 * 60  # 25 minutes in seconds
    assert timer.break_duration == 5 * 60  # 5 minutes in seconds
    assert timer.long_break_duration == 15 * 60  # 15 minutes in seconds
    assert timer.current_time == 0
    assert not timer.is_running

def test_timer_start():
    timer = PomodoroTimer()
    timer.start()
    assert timer.is_running

def test_timer_pause():
    timer = PomodoroTimer()
    timer.start()
    timer.pause()
    assert not timer.is_running

def test_timer_reset():
    timer = PomodoroTimer()
    timer.start()
    timer.current_time = 300  # Set some time
    timer.reset()
    assert timer.current_time == 0
    assert not timer.is_running 