# Task 3.1: Implement Time Allocation Calculator

**Phase:** 3 - Time Allocation & Reporting
**Estimated Time:** 4-6 hours
**Dependencies:** Task 2.3 (Hybrid classifier)

---

## Description

Implement a time allocation calculator that aggregates classified meetings by customer, project, and meeting type to generate time breakdowns. This is the core analytics engine of the system.

---

## Acceptance Criteria

### Calculator Module Created

- [x] `src/magic_umbrella/reporting/time_calculator.py` created ✅
- [x] `TimeAllocationCalculator` class implemented ✅
- [x] Aggregation logic for all category types ✅

### Core Functionality

- [x] Calculate total meeting time for date range ✅
- [x] Aggregate time by customer ✅
- [x] Aggregate time by project ✅
- [x] Aggregate time by meeting type (category) ✅
- [x] Calculate percentages for each category ✅
- [x] Handle meetings with no classification (marked as "Internal") ✅
- [ ] Handle multi-day meetings correctly (mock data is single-day only)
- [ ] Exclude cancelled meetings (not in mock data)

### Time Calculations

- [x] Duration calculated from start/end times (auto in CalendarEvent) ✅
- [ ] Handle timezone conversions correctly (uses datetime objects)
- [ ] Round to nearest 15 minutes (optional - not implemented)
- [x] Support different time units (hours primarily) ✅
- [ ] Calculate business hours only (optional - not implemented)

### Data Structures

- [x] Returns `TimeAllocation` dataclass (not Report, but similar) ✅
- [x] Includes total hours ✅
- [x] Includes breakdown lists (by customer, category, project) ✅
- [x] Includes list of classified meetings ✅

### Statistics

- [x] Average meeting duration ✅
- [x] Number of meetings per category ✅
- [ ] Longest/shortest meetings (not implemented)
- [ ] Most frequent meeting types (could be derived from data)
- [x] Uncategorized meeting percentage (uses summary stats) ✅

---

## Implementation Details

### Class Structure

```python
# src/magic_umbrella/reporting/time_calculator.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

@dataclass
class TimeAllocationReport:
    """Time allocation summary."""
    start_date: datetime
    end_date: datetime
    total_hours: float
    total_meetings: int
    by_customer: Dict[str, float]
    by_project: Dict[str, float]
    by_type: Dict[str, float]
    uncategorized_hours: float
    meetings: List[tuple]  # (CalendarEvent, MeetingClassification)

class TimeAllocationCalculator:
    """Calculate time allocation from classified meetings."""

    def calculate(
        self,
        meetings: List[tuple],  # (CalendarEvent, MeetingClassification)
        start_date: datetime,
        end_date: datetime
    ) -> TimeAllocationReport:
        """Calculate time allocation for date range."""
        pass

    def _calculate_duration_hours(
        self,
        start: datetime,
        end: datetime
    ) -> float:
        """Calculate meeting duration in hours."""
        duration = end - start
        return duration.total_seconds() / 3600

    def _aggregate_by_customer(
        self,
        meetings: List[tuple]
    ) -> Dict[str, float]:
        """Aggregate time by customer."""
        customer_hours = defaultdict(float)
        for event, classification in meetings:
            if classification.customer:
                duration = self._calculate_duration_hours(
                    event.start_time,
                    event.end_time
                )
                customer_hours[classification.customer] += duration
        return dict(customer_hours)

    def _aggregate_by_project(
        self,
        meetings: List[tuple]
    ) -> Dict[str, float]:
        """Aggregate time by project."""
        pass

    def _aggregate_by_type(
        self,
        meetings: List[tuple]
    ) -> Dict[str, float]:
        """Aggregate time by meeting type."""
        pass

    def _calculate_uncategorized_time(
        self,
        meetings: List[tuple]
    ) -> float:
        """Calculate time for uncategorized meetings."""
        uncategorized_hours = 0.0
        for event, classification in meetings:
            if (not classification.customer and
                not classification.project and
                classification.confidence < 0.5):
                duration = self._calculate_duration_hours(
                    event.start_time,
                    event.end_time
                )
                uncategorized_hours += duration
        return uncategorized_hours
```

### Time Rounding (Optional)

```python
def _round_to_quarter_hour(self, hours: float) -> float:
    """Round duration to nearest 15 minutes (0.25 hours)."""
    return round(hours * 4) / 4
```

### Business Hours Filter (Optional)

```python
def _filter_business_hours(
    self,
    start: datetime,
    end: datetime,
    business_start: int = 9,
    business_end: int = 17
) -> float:
    """
    Calculate only time during business hours.

    Args:
        start: Meeting start time
        end: Meeting end time
        business_start: Business day start hour (default 9am)
        business_end: Business day end hour (default 5pm)

    Returns:
        Hours during business hours only
    """
    pass
```

---

## Example Output

### Sample Calculation

```python
Input:
- 50 meetings over 1 week
- Total calendar time: 25 hours

Output:
TimeAllocationReport(
    start_date=datetime(2026, 2, 3),
    end_date=datetime(2026, 2, 9),
    total_hours=25.0,
    total_meetings=50,
    by_customer={
        "Contoso": 8.5,
        "Fabrikam": 6.0,
        "Northwind": 3.5
    },
    by_project={
        "Project Alpha": 4.0,
        "Internal Platform": 2.0
    },
    by_type={
        "Customer Meeting": 18.0,
        "Internal Project": 6.0,
        "1:1 Meeting": 3.0,
        "Team Meeting": 2.5,
        "Administrative": 1.5
    },
    uncategorized_hours=1.0,
    meetings=[...]
)
```

### Percentage Calculation

```python
def _calculate_percentages(report: TimeAllocationReport) -> Dict[str, float]:
    """Calculate percentage breakdown."""
    total = report.total_hours
    return {
        "Customer Work": sum(report.by_customer.values()) / total * 100,
        "Internal Projects": sum(report.by_project.values()) / total * 100,
        "Other": report.uncategorized_hours / total * 100
    }

# Output: {"Customer Work": 72%, "Internal Projects": 24%, "Other": 4%}
```

---

## Edge Cases to Handle

### Multi-Day Meetings

- [ ] All-day events spanning multiple days
- [ ] Multi-hour meetings crossing midnight
- [ ] Recurring meetings with exceptions

### Timezone Issues

- [ ] Meetings in different timezones
- [ ] DST transitions during date range
- [ ] UTC vs. local time storage

### Overlapping Meetings

- [ ] Double-booked time slots
- [ ] Strategy: Count all hours (may exceed 40/week)
- [ ] Optional: Detect and flag overlaps

### Missing Data

- [ ] Meetings with no end time
- [ ] Zero-duration meetings
- [ ] Cancelled meetings (should exclude)

---

## Testing Checklist

- [ ] Test with single meeting
- [ ] Test with multiple customers
- [ ] Test with no categorized meetings
- [ ] Test with all meetings categorized
- [ ] Test date range filtering
- [ ] Test timezone handling
- [ ] Test DST transitions
- [ ] Test all-day events
- [ ] Test overlapping meetings
- [ ] Test duration calculation accuracy

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 609-614)
- Data Model: [research/initial-research.md](../../research/initial-research.md) (Lines 699-705)

---

## Validation Steps

1. Create test dataset with known durations
2. Run calculator
3. Verify totals match expected values
4. Check all meetings are accounted for
5. Verify percentages sum to ~100%
6. Test with real calendar data
