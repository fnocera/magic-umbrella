# Task 4.1: Create Interactive Review Interface (CLI)

**Phase:** 4 - Interactive Validation Loop
**Estimated Time:** 6-8 hours
**Dependencies:** Task 3.1 (Time calculator), Task 3.2 (CLI report)

---

## Description

Implement an interactive CLI interface that allows users to review automatically categorized meetings and make adjustments for prep time, follow-up work, or reclassification. This addresses the requirement: "Include a validation loop where users can interactively edit time allocations to account for prep time or follow-up activities associated with meetings."

---

## Acceptance Criteria

### Interactive Review Module Created

- [x] `src/magic_umbrella/reporting/interactive_review.py` created ✅
- [x] `InteractiveReviewer` class implemented ✅
- [x] CLI interaction using `rich` library for formatting ✅

### Core Functionality

- [x] Display all meetings for the week with classifications ✅
- [x] Show meeting details (title, time, duration, category) ✅
- [x] Highlight low-confidence classifications (color-coded) ✅
- [x] Allow user to navigate through meetings ✅
- [x] Provide options to edit each meeting ✅

### Meeting Actions

- [x] Accept current classification ✅
- [x] Change customer assignment ✅
- [x] Change project assignment ✅
- [x] Change meeting type ✅
- [x] Add prep time (before meeting) ✅
- [x] Add follow-up time (after meeting) ✅
- [ ] Mark as uncategorized (can change to "Uncategorized" category)
- [x] Skip (keep as-is) ✅

### Time Allocation Filling (KEY FEATURE) ✅

- [x] Calculate unallocated hours in work week ✅
- [x] Prompt user for primary projects/customers they work on ✅
- [x] Allow specifying 1-3 background projects ✅
- [x] Distribute unallocated time across specified projects ✅
- [x] Support percentage-based allocation (e.g., 60% Project A, 40% Project B) ✅
- [x] Display total hours including filled time ✅

### User Experience

- [x] Clear visual presentation using `rich.table` ✅
- [x] Color coding for confidence levels ✅
- [ ] Keyboard shortcuts for common actions (uses text prompts instead)
- [x] Progress indicator showing # reviewed / total ✅
- [x] Option to filter by confidence level ✅
- [x] Option to only review low-confidence meetings ✅

### Time Adjustments

- [x] Prompt for prep time in minutes ✅
- [x] Prompt for follow-up time in minutes ✅
- [x] Validate time input (positive numbers) ✅
- [x] Associate adjusted time with same category ✅
- [x] Display total adjusted time clearly ✅

### Persistence

- [x] Save user corrections (in memory via adjustments dict) ✅
- [x] Save background project allocations ✅
- [x] Generate modified report with adjustments ✅
- [ ] Export corrections for future learning (not yet implemented)
- [x] Include filled time in final report ✅

---

## Implementation Details

### Class Structure

```python
# src/magic_umbrella/reporting/interactive_review.py

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from typing import List, Dict, Optional
import json

class InteractiveReviewer:
    """Interactive CLI for reviewing and adjusting meeting classifications."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize interactive reviewer."""
        self.console = console or Console()
        self.adjustments = {}

    def review_meetings(
        self,
        meetings: List[tuple],  # (CalendarEvent, MeetingClassification)
        customers: List[str],
        projects: List[str],
        filter_low_confidence: bool = False,
        confidence_threshold: float = 0.7
    ) -> Dict[str, any]:
        """
        Interactively review meetings and collect adjustments.

        Returns:
            Dictionary of adjustments keyed by meeting ID
        """
        pass

    def _display_meeting(
        self,
        event,
        classification,
        index: int,
        total: int
    ):
        """Display meeting details in formatted panel."""
        pass

    def _prompt_actions(self) -> str:
        """Prompt user for action to take."""
        pass

    def _change_customer(
        self,
        meeting_id: str,
        current_customer: Optional[str],
        customers: List[str]
    ) -> str:
        """Allow user to select new customer."""
        pass

    def _add_prep_time(self, meeting_id: str) -> int:
        """Prompt for prep time in minutes."""
        pass

    def _add_followup_time(self, meeting_id: str) -> int:
        """Prompt for follow-up time in minutes."""
        pass

    def _save_adjustment(
        self,
        meeting_id: str,
        adjustment: Dict
    ):
        """Save user adjustment for this meeting."""
        self.adjustments[meeting_id] = adjustment

    def get_adjustments(self) -> Dict:
        """Return all collected adjustments."""
        return self.adjustments

    def fill_unallocated_time(
        self,
        total_meeting_hours: float,
        work_hours_per_week: float,
        customers: List[str],
        projects: List[str]
    ) -> Dict[str, float]:
        """
        Fill unallocated time with background projects.

        Args:
            total_meeting_hours: Hours spent in meetings
            work_hours_per_week: Expected work hours (e.g., 40)
            customers: Available customers
            projects: Available projects

        Returns:
            Dictionary of project/customer -> allocated hours
        """
        pass

    def _prompt_background_projects(
        self,
        customers: List[str],
        projects: List[str]
    ) -> List[tuple[str, float]]:
        """
        Prompt user to specify background projects and percentages.

        Returns:
            List of (project/customer name, percentage) tuples
        """
        pass
```

### Display Format

```python
def _display_meeting(self, event, classification, index, total):
    """Display formatted meeting details."""

    # Color based on confidence
    color = self._confidence_color(classification.confidence)

    table = Table(title=f"Meeting {index}/{total}", show_header=False)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Subject", event.subject)
    table.add_row(
        "Time",
        f"{event.start_time.strftime('%a %b %d, %I:%M %p')} - "
        f"{event.end_time.strftime('%I:%M %p')}"
    )
    table.add_row("Duration", f"{event.duration_minutes} minutes")
    table.add_row("Customer", classification.customer or "None", style=color)
    table.add_row("Project", classification.project or "None", style=color)
    table.add_row("Type", classification.meeting_type, style=color)
    table.add_row(
        "Confidence",
        f"{classification.confidence:.0%}",
        style=color
    )
    table.add_row("Reasoning", classification.reasoning)

    self.console.print(table)

def _confidence_color(self, confidence: float) -> str:
    """Return color based on confidence level."""
    if confidence >= 0.8:
        return "green"
    elif confidence >= 0.5:
        return "yellow"
    else:
        return "red"
```

### Action Menu

```
┌─────────────────────────────────────────────────┐
│ What would you like to do?                      │
│                                                  │
│ [A] Accept classification                       │
│ [C] Change customer                              │
│ [P] Change project                               │
│ [T] Change meeting type                          │
│ [+] Add prep time                                │
│ [-] Add follow-up time                           │
│ [U] Mark as uncategorized                        │
│ [S] Skip (keep as-is)                            │
│ [Q] Quit review                                  │
└─────────────────────────────────────────────────┘
```

### Time Adjustment Prompt

```python
def _add_prep_time(self, meeting_id: str) -> int:
    """Prompt for prep time."""
    self.console.print("\n[bold]Prep Time[/bold]")
    self.console.print("How many minutes did you spend preparing for this meeting?")

    prep_minutes = IntPrompt.ask(
        "Prep time (minutes)",
        default=0,
        show_default=True
    )

    if prep_minutes > 0:
        self.console.print(
            f"[green]✓ Added {prep_minutes} minutes of prep time[/green]"
        )

    return prep_minutes
```

### Time Filling Flow (NEW)

After reviewing all meetings, prompt user to allocate remaining time:

```python
def fill_unallocated_time(
    self,
    total_meeting_hours: float,
    work_hours_per_week: float = 40.0
) -> Dict[str, float]:
    """Fill unallocated time with background work."""

    unallocated_hours = work_hours_per_week - total_meeting_hours

    if unallocated_hours <= 0:
        self.console.print("[yellow]No unallocated time to fill[/yellow]")
        return {}

    self.console.print("\n[bold cyan]Time Allocation Filling[/bold cyan]")
    self.console.print(
        f"You have [bold]{unallocated_hours:.1f} hours[/bold] unallocated this week."
    )
    self.console.print("\nWhat projects/customers did you work on during this time?")

    allocations = {}
    remaining = 100.0

    # Allow 1-3 background projects
    for i in range(3):
        if remaining <= 0:
            break

        # Prompt for project/customer
        project = Prompt.ask(
            f"\nProject/Customer {i+1} (or press Enter to finish)",
            default="" if i > 0 else None
        )

        if not project:
            break

        # Prompt for percentage
        percentage = IntPrompt.ask(
            f"What percentage of remaining time ({remaining:.0f}%)?",
            default=int(remaining) if i == 0 else 50
        )

        if percentage > remaining:
            self.console.print(f"[red]Cannot exceed {remaining:.0f}%[/red]")
            continue

        hours = unallocated_hours * (percentage / 100)
        allocations[project] = hours
        remaining -= percentage

        self.console.print(
            f"[green]✓ Allocated {hours:.1f} hours ({percentage}%) to {project}[/green]"
        )

    return allocations
```

### Adjustment Data Structure

```python
{
    "meeting_id": {
        "original_classification": {...},
        "updated_classification": {...},
        "prep_time_minutes": 30,
        "followup_time_minutes": 15,
        "user_note": "Spent time reviewing docs before meeting",
        "timestamp": "2026-02-03T10:30:00Z"
    }
}
```

---

## User Flow Example

```
┌─────────────────────────────────────────────────┐
│ Meeting 1/50                                     │
├─────────────────────────────────────────────────┤
│ Subject:  Weekly Sync                            │
│ Time:     Mon Feb 03, 02:00 PM - 03:00 PM       │
│ Duration: 60 minutes                             │
│ Customer: None                                   │
│ Project:  None                                   │
│ Type:     Internal Meeting                       │
│ Confidence: 45% 🟡                               │
│ Reasoning: Generic title, internal attendees     │
└─────────────────────────────────────────────────┘

What would you like to do? [A/C/P/T/+/-/U/S/Q]: T

Select meeting type:
 1. Customer Meeting
 2. Internal Project
 3. 1:1 Meeting
 4. Team Meeting
 5. Administrative
 6. Training

Choice [1-6]: 4

✓ Changed to 'Team Meeting'

Add prep time? [y/N]: n

Add follow-up time? [y/N]: n

Classification updated!
```

---

## User Flow Example: Time Filling (NEW)

After reviewing all 50 meetings:

```
┌─────────────────────────────────────────────────┐
│ Time Allocation Filling                          │
└─────────────────────────────────────────────────┘

You have 15.5 hours unallocated this week.

What projects/customers did you work on during this time?

Project/Customer 1: Contoso Platform Development

What percentage of remaining time (100%)?  [60]: 60

✓ Allocated 9.3 hours (60%) to Contoso Platform Development

Project/Customer 2 (or press Enter to finish): Internal Tools

What percentage of remaining time (40%)? [40]: 40

✓ Allocated 6.2 hours (40%) to Internal Tools

Project/Customer 3 (or press Enter to finish): [Enter]

┌─────────────────────────────────────────────────┐
│ Final Time Allocation Summary                    │
├─────────────────────────────────────────────────┤
│ Total Hours:              40.0                   │
│                                                  │
│ Meeting Time:             24.5 hours (61%)       │
│ ├─ Customer Meetings:     18.0 hours            │
│ ├─ Internal Meetings:      4.5 hours            │
│ └─ Administrative:         2.0 hours            │
│                                                  │
│ Filled Time:              15.5 hours (39%)       │
│ ├─ Contoso Platform:       9.3 hours (60%)      │
│ └─ Internal Tools:         6.2 hours (40%)      │
└─────────────────────────────────────────────────┘
```

---

## Filter Options

### Low-Confidence Only Mode

```python
if filter_low_confidence:
    meetings_to_review = [
        (event, classification)
        for event, classification in meetings
        if classification.confidence < confidence_threshold
    ]
    self.console.print(
        f"Reviewing {len(meetings_to_review)} low-confidence meetings "
        f"(< {confidence_threshold:.0%})"
    )
```

### Quick Review Stats

```
┌─────────────────────────────────────────────────┐
│ Review Summary                                   │
├─────────────────────────────────────────────────┤
│ Total Meetings:        50                       │
│ Reviewed:              35                       │
│ Accepted:              28                       │
│ Modified:              7                        │
│ Prep Time Added:       2.5 hours                │
│ Follow-up Time Added:  1.75 hours               │
└─────────────────────────────────────────────────┘
```

---

## Testing Checklist

- [ ] Test with single meeting
- [ ] Test with 50+ meetings
- [ ] Test changing customer
- [ ] Test changing project
- [ ] Test adding prep time
- [ ] Test adding follow-up time
- [ ] Test accepting classification
- [ ] Test skipping meetings
- [ ] Test quitting mid-review
- [ ] Test with filter_low_confidence=True
- [ ] Test saving adjustments
- [ ] Verify adjustments persist

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 37, 577-582)
- CLI Tools: `rich` library for formatting

---

## Validation Steps

1. Run interactive review with test data
2. Navigate through meetings
3. Make various adjustments
4. Verify adjustments are saved
5. Regenerate report with adjustments
6. Confirm adjusted times are included
