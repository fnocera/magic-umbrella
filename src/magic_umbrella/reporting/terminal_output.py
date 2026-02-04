"""Terminal output for time allocation reports using Rich."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from magic_umbrella.calendar.models import TimeAllocation
from magic_umbrella.reporting.time_calculator import TimeAllocationCalculator


class TerminalReporter:
    """Generate terminal output for time allocation reports."""

    def __init__(self):
        """Initialize reporter with Rich console."""
        self.console = Console()

    def print_summary(self, calculator: TimeAllocationCalculator):
        """Print summary statistics.

        Args:
            calculator: Time allocation calculator with events
        """
        stats = calculator.get_summary_stats()

        # Create summary text
        summary_text = Text()
        summary_text.append("📊 Total Meetings: ", style="bold")
        summary_text.append(f"{stats['total_meetings']}\n")
        summary_text.append("⏱️  Total Hours: ", style="bold")
        summary_text.append(f"{stats['total_hours']:.1f}h\n")
        summary_text.append("⌚ Avg Meeting Length: ", style="bold")
        summary_text.append(f"{stats['avg_meeting_length']:.1f}h\n")
        summary_text.append("👥 Customers: ", style="bold")
        summary_text.append(f"{stats['customer_count']}\n")
        summary_text.append("🏷️  Categories: ", style="bold")
        summary_text.append(f"{stats['category_count']}")

        panel = Panel(summary_text, title="[bold]Summary Statistics[/bold]", border_style="blue")
        self.console.print(panel)
        self.console.print()

    def print_by_customer(self, allocations: list[TimeAllocation]):
        """Print time allocation by customer.

        Args:
            allocations: List of time allocations by customer
        """
        if not allocations:
            self.console.print("[yellow]No customer allocations found[/yellow]")
            return

        # Calculate total for percentages
        total_hours = sum(a.total_hours for a in allocations)

        # Create table
        table = Table(
            title="Time Allocation by Customer", show_header=True, header_style="bold magenta"
        )
        table.add_column("Customer", style="cyan", no_wrap=True)
        table.add_column("Hours", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        table.add_column("Meetings", justify="right")

        for allocation in allocations:
            percentage = (allocation.total_hours / total_hours * 100) if total_hours > 0 else 0
            table.add_row(
                allocation.customer,
                f"{allocation.total_hours:.1f}h",
                f"{percentage:.1f}%",
                str(allocation.meeting_count),
            )

        self.console.print(table)
        self.console.print()

    def print_by_category(self, allocations: list[TimeAllocation]):
        """Print time allocation by category.

        Args:
            allocations: List of time allocations by category
        """
        if not allocations:
            self.console.print("[yellow]No category allocations found[/yellow]")
            return

        # Calculate total for percentages
        total_hours = sum(a.total_hours for a in allocations)

        # Create table
        table = Table(
            title="Time Allocation by Category", show_header=True, header_style="bold magenta"
        )
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Hours", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        table.add_column("Meetings", justify="right")

        for allocation in allocations:
            percentage = (allocation.total_hours / total_hours * 100) if total_hours > 0 else 0
            table.add_row(
                allocation.category,
                f"{allocation.total_hours:.1f}h",
                f"{percentage:.1f}%",
                str(allocation.meeting_count),
            )

        self.console.print(table)
        self.console.print()

    def print_by_customer_and_project(self, allocations: list[TimeAllocation]):
        """Print time allocation by customer and project.

        Args:
            allocations: List of time allocations by customer and project
        """
        if not allocations:
            self.console.print("[yellow]No allocations found[/yellow]")
            return

        # Group by customer
        current_customer = None
        table = None

        for allocation in allocations:
            if allocation.customer != current_customer:
                # Print previous table if exists
                if table:
                    self.console.print(table)
                    self.console.print()

                # Create new table for this customer
                current_customer = allocation.customer
                table = Table(
                    title=f"[bold]{current_customer}[/bold]",
                    show_header=True,
                    header_style="bold magenta",
                )
                table.add_column("Project", style="cyan")
                table.add_column("Hours", justify="right", style="green")
                table.add_column("Meetings", justify="right")

            project_name = allocation.project or "[dim]General[/dim]"
            table.add_row(
                project_name,
                f"{allocation.total_hours:.1f}h",
                str(allocation.meeting_count),
            )

        # Print last table
        if table:
            self.console.print(table)
            self.console.print()

    def print_full_report(self, calculator: TimeAllocationCalculator):
        """Print complete time allocation report.

        Args:
            calculator: Time allocation calculator with events
        """
        self.console.print("\n" + "=" * 60, style="bold blue")
        self.console.print("        TIME ALLOCATION REPORT", style="bold blue", justify="center")
        self.console.print("=" * 60 + "\n", style="bold blue")

        # Summary
        self.print_summary(calculator)

        # By customer
        customer_allocations = calculator.get_by_customer()
        self.print_by_customer(customer_allocations)

        # By category
        category_allocations = calculator.get_by_category()
        self.print_by_category(category_allocations)

        # By customer and project
        customer_project_allocations = calculator.get_by_customer_and_project()
        if any(a.project for a in customer_project_allocations):
            self.print_by_customer_and_project(customer_project_allocations)
