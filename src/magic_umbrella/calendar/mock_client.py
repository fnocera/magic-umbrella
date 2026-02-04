"""Mock Microsoft Graph client for testing without real authentication."""

from datetime import datetime, timedelta
from typing import Optional

from magic_umbrella.calendar.models import Attendee, CalendarEvent


class MockGraphClient:
    """Mock Microsoft Graph API client with sample calendar data."""

    def __init__(self):
        """Initialize mock client with sample events."""
        self.sample_events = self._generate_sample_events()

    def _generate_sample_events(self) -> list[CalendarEvent]:
        """Generate realistic sample calendar events for a week."""
        events = []
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

        # Monday
        events.append(
            CalendarEvent(
                id="evt_001",
                subject="Weekly Standup - Product Team",
                start=base_date,
                end=base_date + timedelta(minutes=30),
                organizer=Attendee(
                    email="manager@company.com", name="Sarah Manager", is_organizer=True
                ),
                attendees=[
                    Attendee(email="dev1@company.com", name="Dev One"),
                    Attendee(email="dev2@company.com", name="Dev Two"),
                ],
                is_online_meeting=True,
                categories=["Team Meeting"],
            )
        )

        events.append(
            CalendarEvent(
                id="evt_002",
                subject="Contoso Client - Requirements Review",
                start=base_date + timedelta(hours=2),
                end=base_date + timedelta(hours=3),
                organizer=Attendee(email="you@company.com", name="You", is_organizer=True),
                attendees=[
                    Attendee(email="client@contoso.com", name="Jane Client"),
                    Attendee(email="pm@company.com", name="Project Manager"),
                ],
                body="Discuss requirements for Phase 2 implementation. Prepare demo.",
                is_online_meeting=True,
                importance="high",
            )
        )

        events.append(
            CalendarEvent(
                id="evt_003",
                subject="Azure Architecture Review - Fabrikam",
                start=base_date + timedelta(hours=5),
                end=base_date + timedelta(hours=6, minutes=30),
                organizer=Attendee(email="architect@fabrikam.com", name="Chief Architect"),
                attendees=[
                    Attendee(email="you@company.com", name="You"),
                    Attendee(email="engineer@fabrikam.com", name="Lead Engineer"),
                ],
                body="Review cloud migration architecture for Fabrikam's infrastructure.",
                location="Teams",
                is_online_meeting=True,
            )
        )

        # Tuesday
        tuesday = base_date + timedelta(days=1)
        events.append(
            CalendarEvent(
                id="evt_004",
                subject="1:1 with Manager",
                start=tuesday + timedelta(hours=1),
                end=tuesday + timedelta(hours=1, minutes=30),
                organizer=Attendee(
                    email="manager@company.com", name="Sarah Manager", is_organizer=True
                ),
                attendees=[Attendee(email="you@company.com", name="You")],
                is_online_meeting=True,
                categories=["1:1"],
            )
        )

        events.append(
            CalendarEvent(
                id="evt_005",
                subject="AdventureWorks - Sprint Planning",
                start=tuesday + timedelta(hours=3),
                end=tuesday + timedelta(hours=5),
                organizer=Attendee(email="scrum@adventureworks.com", name="Scrum Master"),
                attendees=[
                    Attendee(email="you@company.com", name="You"),
                    Attendee(email="dev@adventureworks.com", name="Dev Team"),
                    Attendee(email="po@adventureworks.com", name="Product Owner"),
                ],
                body="Plan Sprint 12 for AdventureWorks CRM implementation",
                is_online_meeting=True,
                importance="high",
            )
        )

        events.append(
            CalendarEvent(
                id="evt_006",
                subject="Internal: All Hands Meeting",
                start=tuesday + timedelta(hours=6),
                end=tuesday + timedelta(hours=7),
                organizer=Attendee(email="ceo@company.com", name="CEO"),
                attendees=[],  # Large meeting
                body="Quarterly company update and roadmap",
                is_online_meeting=True,
            )
        )

        # Wednesday
        wednesday = base_date + timedelta(days=2)
        events.append(
            CalendarEvent(
                id="evt_007",
                subject="Contoso Technical Deep Dive",
                start=wednesday + timedelta(hours=2),
                end=wednesday + timedelta(hours=4),
                organizer=Attendee(email="you@company.com", name="You", is_organizer=True),
                attendees=[
                    Attendee(email="tech@contoso.com", name="Tech Lead"),
                    Attendee(email="dev@contoso.com", name="Senior Developer"),
                ],
                body="Deep dive into API integration requirements for Contoso project",
                is_online_meeting=True,
            )
        )

        events.append(
            CalendarEvent(
                id="evt_008",
                subject="Training: Azure AI Services",
                start=wednesday + timedelta(hours=5),
                end=wednesday + timedelta(hours=6, minutes=30),
                organizer=Attendee(
                    email="training@company.com", name="Training Team", is_organizer=True
                ),
                attendees=[],
                body="Learn about new Azure OpenAI features",
                is_online_meeting=True,
                categories=["Training"],
            )
        )

        # Thursday
        thursday = base_date + timedelta(days=3)
        events.append(
            CalendarEvent(
                id="evt_009",
                subject="Fabrikam Project Status",
                start=thursday + timedelta(hours=1),
                end=thursday + timedelta(hours=2),
                organizer=Attendee(email="pm@fabrikam.com", name="Fabrikam PM"),
                attendees=[
                    Attendee(email="you@company.com", name="You"),
                    Attendee(email="stakeholder@fabrikam.com", name="Stakeholder"),
                ],
                body="Weekly status update for Fabrikam cloud migration",
                is_online_meeting=True,
            )
        )

        events.append(
            CalendarEvent(
                id="evt_010",
                subject="Sales Demo - Northwind Traders",
                start=thursday + timedelta(hours=3),
                end=thursday + timedelta(hours=4),
                organizer=Attendee(email="sales@company.com", name="Sales Rep", is_organizer=True),
                attendees=[
                    Attendee(email="you@company.com", name="You"),
                    Attendee(email="decision@northwind.com", name="Decision Maker"),
                ],
                body="Product demonstration for potential new client Northwind Traders",
                is_online_meeting=True,
                importance="high",
            )
        )

        events.append(
            CalendarEvent(
                id="evt_011",
                subject="Code Review Session",
                start=thursday + timedelta(hours=5),
                end=thursday + timedelta(hours=6),
                organizer=Attendee(email="you@company.com", name="You", is_organizer=True),
                attendees=[
                    Attendee(email="junior@company.com", name="Junior Dev"),
                ],
                body="Review pull requests and provide mentoring",
                is_online_meeting=True,
                categories=["Development"],
            )
        )

        # Friday
        friday = base_date + timedelta(days=4)
        events.append(
            CalendarEvent(
                id="evt_012",
                subject="AdventureWorks Sprint Review",
                start=friday + timedelta(hours=1),
                end=friday + timedelta(hours=2, minutes=30),
                organizer=Attendee(email="po@adventureworks.com", name="Product Owner"),
                attendees=[
                    Attendee(email="you@company.com", name="You"),
                    Attendee(email="team@adventureworks.com", name="Scrum Team"),
                ],
                body="Demo completed work from Sprint 11",
                is_online_meeting=True,
            )
        )

        events.append(
            CalendarEvent(
                id="evt_013",
                subject="Team Social Hour",
                start=friday + timedelta(hours=4),
                end=friday + timedelta(hours=5),
                organizer=Attendee(email="team@company.com", name="Team Lead", is_organizer=True),
                attendees=[],
                body="Virtual team social and games",
                is_online_meeting=True,
                categories=["Social"],
            )
        )

        events.append(
            CalendarEvent(
                id="evt_014",
                subject="Focus Time - Documentation",
                start=friday + timedelta(hours=5, minutes=30),
                end=friday + timedelta(hours=7),
                organizer=Attendee(email="you@company.com", name="You", is_organizer=True),
                attendees=[],
                body="Catch up on project documentation",
                categories=["Focus Time"],
            )
        )

        return events

    def get_calendar_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[CalendarEvent]:
        """Get calendar events for a date range.

        Args:
            start_date: Start of date range (defaults to today)
            end_date: End of date range (defaults to 7 days from start)

        Returns:
            List of calendar events
        """
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if end_date is None:
            end_date = start_date + timedelta(days=7)

        # Filter events within the date range
        filtered = [event for event in self.sample_events if start_date <= event.start <= end_date]

        return filtered

    def get_user_info(self) -> dict:
        """Get mock user information.

        Returns:
            Dictionary with user details
        """
        return {
            "displayName": "Test User",
            "mail": "you@company.com",
            "userPrincipalName": "you@company.com",
        }
