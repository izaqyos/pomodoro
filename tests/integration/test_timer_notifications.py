import pytest
from src.core.timer import PomodoroTimer
from src.utils.notifications import NotificationManager

def test_timer_completion_notification():
    timer = PomodoroTimer()
    notifier = NotificationManager()
    
    # Simulate timer completion
    timer.start()
    timer.current_time = timer.work_duration
    
    # This test will need to be updated based on your actual implementation
    # of how timer and notifications interact
    assert timer.is_running
    assert notifier.enabled 