"""Data models for calendar events and meetings."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Attendee(BaseModel):
    """Represents a meeting attendee."""

    email: str
    name: Optional[str] = None
    is_organizer: bool = False
    response_status: str = "none"  # accepted, declined, tentative, none


class CalendarEvent(BaseModel):
    """Represents a calendar event/meeting from Microsoft Graph."""

    id: str
    subject: str
    start: datetime
    end: datetime
    duration_hours: float = Field(default=0.0)
    organizer: Optional[Attendee] = None
    attendees: list[Attendee] = Field(default_factory=list)
    body: Optional[str] = None
    location: Optional[str] = None
    is_online_meeting: bool = False
    is_all_day: bool = False
    is_cancelled: bool = False
    categories: list[str] = Field(default_factory=list)
    importance: str = "normal"  # low, normal, high

    def __init__(self, **data):
        """Initialize event and calculate duration."""
        super().__init__(**data)
        if self.duration_hours == 0.0:
            delta = self.end - self.start
            self.duration_hours = delta.total_seconds() / 3600


class CategorizedEvent(BaseModel):
    """Calendar event with classification results."""

    event: CalendarEvent
    customer: Optional[str] = None
    project: Optional[str] = None
    category: str = "unclassified"
    confidence: float = 0.0
    classification_method: str = "unknown"  # rule_based, llm, manual
    notes: Optional[str] = None
    prep_time_hours: float = 0.0
    followup_time_hours: float = 0.0

    @property
    def total_hours(self) -> float:
        """Total time including meeting, prep, and follow-up."""
        return self.event.duration_hours + self.prep_time_hours + self.followup_time_hours


class TimeAllocation(BaseModel):
    """Summary of time allocation across customers, projects, and categories."""

    customer: str
    project: Optional[str] = None
    category: str
    total_hours: float = 0.0
    meeting_count: int = 0
    events: list[CategorizedEvent] = Field(default_factory=list)
