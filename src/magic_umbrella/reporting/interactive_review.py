"""Interactive review interface for meeting classifications."""

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from magic_umbrella.calendar.models import CategorizedEvent
from magic_umbrella.config import ConfigLoader


class InteractiveReviewer:
    """Interactive CLI for reviewing and adjusting meeting classifications."""

    def __init__(self, config: ConfigLoader, console: Optional[Console] = None):
        """Initialize interactive reviewer.

        Args:
            config: Configuration loader with customers and projects
            console: Rich console (optional, creates new one if not provided)
        """
        self.config = config
        self.console = console or Console()
        self.adjustments = {}
        self.background_allocations = {}

    def review_meetings(
        self,
        events: list[CategorizedEvent],
        filter_low_confidence: bool = False,
        confidence_threshold: float = 0.7,
    ) -> dict:
        """Interactively review meetings and collect adjustments.

        Args:
            events: List of categorized events to review
            filter_low_confidence: Only show low-confidence meetings
            confidence_threshold: Confidence threshold for filtering

        Returns:
            Dictionary of adjustments keyed by event ID
        """
        # Filter events if requested
        events_to_review = events
        if filter_low_confidence:
            events_to_review = [e for e in events if e.confidence < confidence_threshold]

        if not events_to_review:
            self.console.print("[green]All meetings have high confidence classifications![/green]")
            return {}

        self.console.print("\n[bold blue]═══ Interactive Meeting Review ═══[/bold blue]")
        self.console.print(f"Reviewing {len(events_to_review)} of {len(events)} meetings\n")

        # Review each event
        for i, event in enumerate(events_to_review, 1):
            self._display_meeting(event, i, len(events_to_review))

            # Ask if user wants to make changes
            if Confirm.ask("Review this meeting?", default=True):
                self._review_single_meeting(event)

        return self.get_adjustments()

    def fill_unallocated_time(
        self,
        total_meeting_hours: float,
        work_hours_per_week: float = 40.0,
        period_days: int = 5,
    ) -> dict[str, float]:
        """Fill unallocated time with background projects/customers.

        Args:
            total_meeting_hours: Hours spent in meetings
            work_hours_per_week: Expected work hours per week
            period_days: Number of days in the period

        Returns:
            Dictionary of customer/project -> allocated hours
        """
        # Calculate unallocated hours
        work_hours = (work_hours_per_week / 5) * period_days
        unallocated_hours = max(0.0, work_hours - total_meeting_hours)

        if unallocated_hours == 0:
            self.console.print("[yellow]No unallocated time - all hours accounted for![/yellow]")
            return {}

        # Display info
        self.console.print("\n[bold blue]═══ Time Allocation Filling ═══[/bold blue]")
        self.console.print(f"Meeting hours: {total_meeting_hours:.1f}h")
        self.console.print(f"Work hours: {work_hours:.1f}h")
        self.console.print(
            f"[bold green]Unallocated hours: {unallocated_hours:.1f}h[/bold green]\n"
        )

        # Ask if user wants to fill time
        if not Confirm.ask(
            "Would you like to allocate this time to background projects/customers?",
            default=True,
        ):
            return {}

        # Collect background projects
        allocations = self._prompt_background_projects(unallocated_hours)

        # Save allocations
        self.background_allocations = allocations

        # Display summary
        self._display_background_summary(allocations, unallocated_hours)

        return allocations

    def _display_meeting(self, event: CategorizedEvent, index: int, total: int):
        """Display meeting details in formatted panel.

        Args:
            event: Categorized event to display
            index: Current meeting number
            total: Total number of meetings
        """
        # Determine confidence color
        if event.confidence >= 0.8:
            confidence_color = "green"
        elif event.confidence >= 0.6:
            confidence_color = "yellow"
        else:
            confidence_color = "red"

        # Build content
        content = Text()
        content.append(f"📅 {event.event.subject}\n", style="bold")
        start_time = event.event.start.strftime("%a %I:%M %p")
        end_time = event.event.end.strftime("%I:%M %p")
        content.append(f"⏰ {start_time} - {end_time} ")
        content.append(f"({event.event.duration_hours:.1f}h)\n\n")

        content.append("Classification:\n", style="bold")
        content.append(f"  Customer: {event.customer or 'None'}\n")
        content.append(f"  Project: {event.project or 'None'}\n")
        content.append(f"  Category: {event.category}\n")
        content.append("  Confidence: ", style="bold")
        content.append(f"{event.confidence:.0%}\n", style=confidence_color)
        content.append(f"  Reasoning: {event.notes}\n")

        if event.prep_time_hours > 0 or event.followup_time_hours > 0:
            content.append("\nTime Adjustments:\n", style="bold")
            if event.prep_time_hours > 0:
                content.append(f"  Prep time: {event.prep_time_hours:.1f}h\n")
            if event.followup_time_hours > 0:
                content.append(f"  Follow-up time: {event.followup_time_hours:.1f}h\n")

        panel = Panel(
            content,
            title=f"[bold]Meeting {index}/{total}[/bold]",
            border_style="blue",
        )
        self.console.print(panel)

    def _review_single_meeting(self, event: CategorizedEvent):
        """Review and potentially adjust a single meeting.

        Args:
            event: Event to review
        """
        while True:
            self.console.print("\n[bold]Actions:[/bold]")
            self.console.print("  [c] Change customer")
            self.console.print("  [p] Change project")
            self.console.print("  [t] Change category/type")
            self.console.print("  [prep] Add prep time")
            self.console.print("  [follow] Add follow-up time")
            self.console.print("  [ok] Accept and continue")
            self.console.print("  [skip] Skip without changes")

            action = Prompt.ask("Choose action", default="ok").lower()

            if action == "c":
                self._change_customer(event)
            elif action == "p":
                self._change_project(event)
            elif action == "t":
                self._change_category(event)
            elif action == "prep":
                self._add_prep_time(event)
            elif action == "follow":
                self._add_followup_time(event)
            elif action in ["ok", "skip"]:
                break
            else:
                self.console.print("[red]Invalid action[/red]")

    def _change_customer(self, event: CategorizedEvent):
        """Change customer assignment.

        Args:
            event: Event to modify
        """
        customers = [c.name for c in self.config.get_customers()]
        customers.append("None (Internal)")

        self.console.print("\n[bold]Available customers:[/bold]")
        for i, customer in enumerate(customers, 1):
            self.console.print(f"  {i}. {customer}")

        choice = IntPrompt.ask("Select customer number (0 to cancel)", default=0, show_default=True)

        if choice > 0 and choice <= len(customers):
            new_customer = customers[choice - 1]
            if new_customer == "None (Internal)":
                new_customer = None

            event.customer = new_customer
            event.classification_method = "manual"
            self.console.print(f"[green]✓ Customer updated to: {new_customer or 'None'}[/green]")

            # Save adjustment
            self._save_adjustment(event.event.id, {"customer": new_customer})

    def _change_project(self, event: CategorizedEvent):
        """Change project assignment.

        Args:
            event: Event to modify
        """
        projects = [p.name for p in self.config.get_projects()]
        projects.append("None")

        self.console.print("\n[bold]Available projects:[/bold]")
        for i, project in enumerate(projects, 1):
            self.console.print(f"  {i}. {project}")

        choice = IntPrompt.ask("Select project number (0 to cancel)", default=0, show_default=True)

        if choice > 0 and choice <= len(projects):
            new_project = projects[choice - 1]
            if new_project == "None":
                new_project = None

            event.project = new_project
            event.classification_method = "manual"
            self.console.print(f"[green]✓ Project updated to: {new_project or 'None'}[/green]")

            # Save adjustment
            self._save_adjustment(event.event.id, {"project": new_project})

    def _change_category(self, event: CategorizedEvent):
        """Change category/meeting type.

        Args:
            event: Event to modify
        """
        categories = [mt.name for mt in self.config.get_meeting_types()]

        self.console.print("\n[bold]Available categories:[/bold]")
        for i, category in enumerate(categories, 1):
            self.console.print(f"  {i}. {category}")

        choice = IntPrompt.ask("Select category number (0 to cancel)", default=0, show_default=True)

        if choice > 0 and choice <= len(categories):
            new_category = categories[choice - 1]
            event.category = new_category
            event.classification_method = "manual"
            self.console.print(f"[green]✓ Category updated to: {new_category}[/green]")

            # Save adjustment
            self._save_adjustment(event.event.id, {"category": new_category})

    def _add_prep_time(self, event: CategorizedEvent):
        """Add preparation time to meeting.

        Args:
            event: Event to modify
        """
        minutes = FloatPrompt.ask("Prep time in minutes", default=0.0, show_default=True)

        if minutes > 0:
            hours = minutes / 60.0
            event.prep_time_hours = hours
            self.console.print(f"[green]✓ Added {minutes} minutes ({hours:.1f}h) prep time[/green]")

            # Save adjustment
            self._save_adjustment(event.event.id, {"prep_time_hours": hours})

    def _add_followup_time(self, event: CategorizedEvent):
        """Add follow-up time to meeting.

        Args:
            event: Event to modify
        """
        minutes = FloatPrompt.ask("Follow-up time in minutes", default=0.0, show_default=True)

        if minutes > 0:
            hours = minutes / 60.0
            event.followup_time_hours = hours
            self.console.print(
                f"[green]✓ Added {minutes} minutes ({hours:.1f}h) follow-up time[/green]"
            )

            # Save adjustment
            self._save_adjustment(event.event.id, {"followup_time_hours": hours})

    def _save_adjustment(self, event_id: str, adjustment: dict):
        """Save user adjustment for this meeting.

        Args:
            event_id: ID of the event
            adjustment: Dictionary of adjustments
        """
        if event_id not in self.adjustments:
            self.adjustments[event_id] = {}

        self.adjustments[event_id].update(adjustment)

    def _prompt_background_projects(self, unallocated_hours: float) -> dict[str, float]:
        """Prompt user to specify background projects and allocation.

        Args:
            unallocated_hours: Total hours to allocate

        Returns:
            Dictionary of project/customer -> hours
        """
        allocations = {}

        # Get available customers and projects
        customers = [c.name for c in self.config.get_customers()]
        projects = [p.name for p in self.config.get_projects()]

        # Combine for selection
        options = ["[Customer] " + c for c in customers] + ["[Project] " + p for p in projects]

        self.console.print(
            "\n[bold]Specify 1-3 background projects/customers for unallocated time:[/bold]\n"
        )

        # Get number of items
        num_items = IntPrompt.ask(
            "How many projects/customers?", default=1, show_choices=["1", "2", "3"]
        )

        remaining_percentage = 100.0

        for i in range(num_items):
            self.console.print(f"\n[bold]Item {i + 1}:[/bold]")

            # Show options
            for j, option in enumerate(options, 1):
                self.console.print(f"  {j}. {option}")

            choice = IntPrompt.ask("Select number", show_default=False)

            if choice < 1 or choice > len(options):
                self.console.print("[red]Invalid choice, skipping[/red]")
                continue

            item_name = options[choice - 1]

            # Get percentage
            if i == num_items - 1:
                # Last item gets remainder
                percentage = remaining_percentage
                self.console.print(
                    f"[dim]Automatically allocating remaining {percentage:.0f}%[/dim]"
                )
            else:
                percentage = FloatPrompt.ask(
                    f"Percentage of time (remaining: {remaining_percentage:.0f}%)",
                    default=50.0,
                )

                # Validate
                if percentage > remaining_percentage:
                    self.console.print(f"[yellow]Adjusting to {remaining_percentage:.0f}%[/yellow]")
                    percentage = remaining_percentage

            # Calculate hours
            hours = (percentage / 100.0) * unallocated_hours
            allocations[item_name] = hours

            remaining_percentage -= percentage

            if remaining_percentage <= 0:
                break

        return allocations

    def _display_background_summary(self, allocations: dict[str, float], total_hours: float):
        """Display summary of background time allocations.

        Args:
            allocations: Dictionary of item -> hours
            total_hours: Total hours allocated
        """
        self.console.print("\n[bold green]✓ Background Time Allocated:[/bold green]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Project/Customer", style="cyan")
        table.add_column("Hours", justify="right", style="green")
        table.add_column("Percentage", justify="right")

        for item, hours in allocations.items():
            percentage = (hours / total_hours * 100) if total_hours > 0 else 0
            table.add_row(item, f"{hours:.1f}h", f"{percentage:.0f}%")

        self.console.print(table)
        self.console.print()

    def get_adjustments(self) -> dict:
        """Get all collected adjustments.

        Returns:
            Dictionary of adjustments
        """
        return self.adjustments

    def get_background_allocations(self) -> dict[str, float]:
        """Get background time allocations.

        Returns:
            Dictionary of project/customer -> hours
        """
        return self.background_allocations
