import pytest
from src.utils.notifications import NotificationManager

def test_notification_initialization():
    notifier = NotificationManager()
    assert notifier.enabled

def test_notification_disable():
    notifier = NotificationManager()
    notifier.enabled = False
    assert not notifier.enabled

def test_send_notification():
    notifier = NotificationManager()
    # This is a basic test - you might want to mock the actual notification
    # system and test that it's called correctly
    notifier.send_notification("Test", "Test Message")
    assert True  # If no exception is raised, test passes 