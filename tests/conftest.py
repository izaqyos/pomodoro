import pytest
from src.core.timer import PomodoroTimer
from src.utils.notifications import NotificationManager

@pytest.fixture
def timer():
    return PomodoroTimer()

@pytest.fixture
def notifier():
    return NotificationManager() 