"""Interactive demo with meeting review and time-filling."""

from magic_umbrella.calendar import CategorizedEvent, MockGraphClient
from magic_umbrella.categorization import RuleBasedClassifier
from magic_umbrella.config import ConfigLoader
from magic_umbrella.reporting import (
    InteractiveReviewer,
    TerminalReporter,
    TimeAllocationCalculator,
)


def main():
    """Run interactive demo."""
    # Step 1: Load configuration
    print("Loading configuration...")
    config = ConfigLoader(config_dir="./config")

    # Step 2: Get calendar events
    print("Fetching calendar events...\n")
    client = MockGraphClient()
    events = client.get_calendar_events()

    # Step 3: Classify events
    print(f"Classifying {len(events)} events...")
    classifier = RuleBasedClassifier(config)

    categorized_events = []
    for event in events:
        classification = classifier.classify(event)

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

    print("✓ Classification complete!\n")

    # Step 4: Interactive review
    reviewer = InteractiveReviewer(config)

    # Option to review low-confidence meetings
    print("=" * 60)
    print("Would you like to review meetings?")
    print("  1. Review all meetings")
    print("  2. Review only low-confidence meetings (< 70%)")
    print("  3. Skip review")
    choice = input("Choice [3]: ").strip() or "3"

    if choice == "1":
        reviewer.review_meetings(categorized_events, filter_low_confidence=False)
    elif choice == "2":
        reviewer.review_meetings(
            categorized_events, filter_low_confidence=True, confidence_threshold=0.7
        )

    # Step 5: Calculate time allocation
    calculator = TimeAllocationCalculator()
    calculator.add_events(categorized_events)

    total_meeting_hours = calculator.get_total_meeting_hours()

    # Step 6: Time allocation filling (KEY FEATURE!)
    background_allocations = reviewer.fill_unallocated_time(
        total_meeting_hours=total_meeting_hours,
        work_hours_per_week=40.0,
        period_days=5,
    )

    # Step 7: Generate final report
    reporter = TerminalReporter()
    reporter.print_full_report(calculator)

    # Step 8: Show background allocations
    if background_allocations:
        print("\n" + "=" * 60)
        print("         BACKGROUND PROJECT ALLOCATIONS")
        print("=" * 60 + "\n")

        for item, hours in background_allocations.items():
            print(f"  {item}: {hours:.1f}h")

        # Calculate new total
        background_hours = sum(background_allocations.values())
        total_hours = total_meeting_hours + background_hours
        print(f"\n[bold]Total allocated hours: {total_hours:.1f}h[/bold]")

    print("\n" + "=" * 60)
    print("Demo complete! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    main()
