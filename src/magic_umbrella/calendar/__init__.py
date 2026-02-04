"""Calendar module for fetching and parsing events."""

from magic_umbrella.calendar.mock_client import MockGraphClient
from magic_umbrella.calendar.models import (
    Attendee,
    CalendarEvent,
    CategorizedEvent,
    TimeAllocation,
)

__all__ = [
    "MockGraphClient",
    "Attendee",
    "CalendarEvent",
    "CategorizedEvent",
    "TimeAllocation",
]
