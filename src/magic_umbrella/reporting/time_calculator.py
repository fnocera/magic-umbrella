"""Time allocation calculator and aggregator."""

from collections import defaultdict

from magic_umbrella.calendar.models import CategorizedEvent, TimeAllocation


class TimeAllocationCalculator:
    """Calculate time allocation across customers, projects, and categories."""

    def __init__(self):
        """Initialize calculator."""
        self.events: list[CategorizedEvent] = []

    def add_events(self, events: list[CategorizedEvent]):
        """Add categorized events to the calculator.

        Args:
            events: List of categorized calendar events
        """
        self.events.extend(events)

    def get_total_meeting_hours(self) -> float:
        """Calculate total meeting hours.

        Returns:
            Total hours across all meetings (including prep and follow-up time)
        """
        return sum(event.total_hours for event in self.events)

    def get_by_customer(self) -> list[TimeAllocation]:
        """Aggregate time allocation by customer.

        Returns:
            List of TimeAllocation grouped by customer
        """
        customer_data = defaultdict(lambda: {"hours": 0.0, "count": 0, "events": []})

        for event in self.events:
            customer = event.customer or "Internal"
            customer_data[customer]["hours"] += event.total_hours
            customer_data[customer]["count"] += 1
            customer_data[customer]["events"].append(event)

        allocations = [
            TimeAllocation(
                customer=customer,
                project=None,
                category="All",
                total_hours=data["hours"],
                meeting_count=data["count"],
                events=data["events"],
            )
            for customer, data in customer_data.items()
        ]

        # Sort by hours descending
        return sorted(allocations, key=lambda x: x.total_hours, reverse=True)

    def get_by_category(self) -> list[TimeAllocation]:
        """Aggregate time allocation by category.

        Returns:
            List of TimeAllocation grouped by category
        """
        category_data = defaultdict(lambda: {"hours": 0.0, "count": 0, "events": []})

        for event in self.events:
            category = event.category
            category_data[category]["hours"] += event.total_hours
            category_data[category]["count"] += 1
            category_data[category]["events"].append(event)

        allocations = [
            TimeAllocation(
                customer="All",
                project=None,
                category=category,
                total_hours=data["hours"],
                meeting_count=data["count"],
                events=data["events"],
            )
            for category, data in category_data.items()
        ]

        # Sort by hours descending
        return sorted(allocations, key=lambda x: x.total_hours, reverse=True)

    def get_by_customer_and_project(self) -> list[TimeAllocation]:
        """Aggregate time allocation by customer and project.

        Returns:
            List of TimeAllocation grouped by customer and project
        """
        allocation_data = defaultdict(lambda: {"hours": 0.0, "count": 0, "events": []})

        for event in self.events:
            customer = event.customer or "Internal"
            project = event.project or "General"
            key = (customer, project)

            allocation_data[key]["hours"] += event.total_hours
            allocation_data[key]["count"] += 1
            allocation_data[key]["events"].append(event)

        allocations = [
            TimeAllocation(
                customer=customer,
                project=project if project != "General" else None,
                category="All",
                total_hours=data["hours"],
                meeting_count=data["count"],
                events=data["events"],
            )
            for (customer, project), data in allocation_data.items()
        ]

        # Sort by customer, then hours
        return sorted(allocations, key=lambda x: (x.customer, -x.total_hours))

    def get_summary_stats(self) -> dict:
        """Get summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        if not self.events:
            return {
                "total_meetings": 0,
                "total_hours": 0.0,
                "avg_meeting_length": 0.0,
                "customer_count": 0,
                "category_count": 0,
            }

        total_hours = self.get_total_meeting_hours()
        customer_allocations = self.get_by_customer()
        category_allocations = self.get_by_category()

        # Count customers (excluding "Internal")
        customer_count = sum(1 for a in customer_allocations if a.customer != "Internal")

        return {
            "total_meetings": len(self.events),
            "total_hours": total_hours,
            "avg_meeting_length": total_hours / len(self.events) if self.events else 0.0,
            "customer_count": customer_count,
            "category_count": len(category_allocations),
        }

    def get_unallocated_hours(
        self, work_hours_per_week: float = 40.0, period_days: int = 5
    ) -> float:
        """Calculate unallocated hours (time not in meetings).

        Args:
            work_hours_per_week: Expected work hours per week
            period_days: Number of days in the period

        Returns:
            Hours not allocated to meetings
        """
        # Calculate work hours for the period
        work_hours = (work_hours_per_week / 5) * period_days

        # Subtract meeting hours
        meeting_hours = self.get_total_meeting_hours()

        return max(0.0, work_hours - meeting_hours)

    def get_customer_percentage(self, customer: str) -> float:
        """Get percentage of time spent with a specific customer.

        Args:
            customer: Customer name

        Returns:
            Percentage (0-100) of total time
        """
        total_hours = self.get_total_meeting_hours()
        if total_hours == 0:
            return 0.0

        customer_hours = sum(
            event.total_hours for event in self.events if event.customer == customer
        )

        return (customer_hours / total_hours) * 100
