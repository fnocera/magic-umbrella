"""End-to-end demo of the Magic Umbrella time allocation system."""

from magic_umbrella.calendar import CategorizedEvent, MockGraphClient
from magic_umbrella.categorization import RuleBasedClassifier
from magic_umbrella.config import ConfigLoader
from magic_umbrella.reporting import TerminalReporter, TimeAllocationCalculator


def main():
    """Run end-to-end demo."""
    # Step 1: Load configuration
    print("Loading configuration...")
    config = ConfigLoader(config_dir="./config")

    # Step 2: Get calendar events (using mock data)
    print("Fetching calendar events...\n")
    client = MockGraphClient()
    events = client.get_calendar_events()

    # Step 3: Classify events
    print(f"Classifying {len(events)} events...")
    classifier = RuleBasedClassifier(config)

    categorized_events = []
    for event in events:
        classification = classifier.classify(event)

        # Convert to CategorizedEvent
        categorized = CategorizedEvent(
            event=event,
            customer=classification.customer,
            project=classification.project,
            category=classification.category,
            confidence=classification.confidence,
            classification_method=classification.source,
            notes=classification.reasoning,
        )
        categorized_events.append(categorized)

    # Step 4: Calculate time allocation
    print("Calculating time allocation...")
    calculator = TimeAllocationCalculator()
    calculator.add_events(categorized_events)

    # Step 5: Generate report
    reporter = TerminalReporter()
    reporter.print_full_report(calculator)

    # Additional insights
    print("\n" + "=" * 60)
    print("         ADDITIONAL INSIGHTS")
    print("=" * 60 + "\n")

    # Unallocated hours
    unallocated = calculator.get_unallocated_hours(work_hours_per_week=40.0, period_days=5)
    print(f"📝 Unallocated Hours (40h work week): {unallocated:.1f}h")
    print("   This time could be allocated to background projects/customers\n")

    # Top customers by percentage
    customer_allocations = calculator.get_by_customer()
    if customer_allocations:
        print("🏆 Top Customers by Time:")
        for i, allocation in enumerate(customer_allocations[:3], 1):
            percentage = calculator.get_customer_percentage(allocation.customer)
            print(f"   {i}. {allocation.customer}: {percentage:.1f}%")


if __name__ == "__main__":
    main()
