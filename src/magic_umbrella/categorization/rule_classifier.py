"""Rule-based meeting classifier using pattern matching."""

import re
from dataclasses import dataclass
from typing import Optional

from thefuzz import fuzz

from magic_umbrella.calendar.models import CalendarEvent
from magic_umbrella.config.loader import ConfigLoader


@dataclass
class MeetingClassification:
    """Result of meeting classification."""

    customer: Optional[str] = None
    project: Optional[str] = None
    category: str = "Uncategorized"
    confidence: float = 0.0
    reasoning: str = ""
    source: str = "rules"


class RuleBasedClassifier:
    """Rule-based meeting categorization using pattern matching."""

    def __init__(self, config_loader: ConfigLoader):
        """Initialize with configuration.

        Args:
            config_loader: Loaded configuration with customers, projects, and meeting types
        """
        self.config = config_loader
        self.customers = config_loader.get_customers()
        self.projects = config_loader.get_projects()
        self.meeting_types = config_loader.get_meeting_types()

    def classify(self, event: CalendarEvent) -> MeetingClassification:
        """Classify a calendar event using rules.

        Args:
            event: Calendar event to classify

        Returns:
            MeetingClassification with detected customer, project, category, and confidence
        """
        # Prepare text for analysis
        subject = event.subject or ""
        body = event.body or ""
        combined_text = f"{subject} {body}".lower()

        # Extract attendee emails
        attendee_emails = [a.email for a in event.attendees if a.email]

        # Detect customer
        customer, customer_confidence, customer_reason = self._detect_customer(
            combined_text, attendee_emails, event.categories
        )

        # Detect project
        project, project_confidence, project_reason = self._detect_project(combined_text)

        # Detect meeting type/category
        category, category_confidence, category_reason = self._detect_category(
            combined_text, attendee_emails, customer is not None
        )

        # Calculate overall confidence (weighted average)
        if customer:
            confidence = customer_confidence * 0.6 + category_confidence * 0.4
        else:
            confidence = category_confidence

        # Build reasoning text
        reasons = []
        if customer_reason:
            reasons.append(customer_reason)
        if project_reason:
            reasons.append(project_reason)
        if category_reason:
            reasons.append(category_reason)

        reasoning = "; ".join(reasons) if reasons else "No clear patterns detected"

        return MeetingClassification(
            customer=customer,
            project=project,
            category=category,
            confidence=confidence,
            reasoning=reasoning,
            source="rules",
        )

    def _detect_customer(
        self, text: str, attendee_emails: list[str], categories: list[str]
    ) -> tuple[Optional[str], float, str]:
        """Detect customer from text, attendee domains, and Outlook categories.

        Args:
            text: Combined subject and body text (lowercase)
            attendee_emails: List of attendee email addresses
            categories: Outlook categories

        Returns:
            Tuple of (customer_name, confidence, reasoning)
        """
        # Pattern 1: Bracketed customer name [Customer]
        bracket_pattern = r"\[([^\]]+)\]"
        match = re.search(bracket_pattern, text)
        if match:
            potential_name = match.group(1).strip()
            customer = self.config.get_customer_by_name(potential_name)
            if customer:
                return customer.name, 0.95, f"Customer '{customer.name}' in brackets"

        # Pattern 2: Customer name prefix "Customer -" or "Customer:"
        for customer in self.customers:
            # Check main name
            names_to_check = [customer.name] + customer.aliases

            for name in names_to_check:
                name_lower = name.lower()

                # Exact match at start with separator
                if text.startswith(f"{name_lower} -") or text.startswith(f"{name_lower}:"):
                    return (
                        customer.name,
                        0.90,
                        f"Customer '{customer.name}' as prefix",
                    )

        # Pattern 3: Fuzzy match customer names in text
        best_fuzzy_score = 0
        best_customer = None

        for customer in self.customers:
            names_to_check = [customer.name] + customer.aliases

            for name in names_to_check:
                score = fuzz.partial_ratio(name.lower(), text)
                if score > best_fuzzy_score and score >= 80:
                    best_fuzzy_score = score
                    best_customer = customer

        # Pattern 4: Domain matching from attendees
        domain_match = None
        for email in attendee_emails:
            domain = self._extract_domain(email)
            for customer in self.customers:
                if domain in customer.domains:
                    domain_match = customer
                    break
            if domain_match:
                break

        # Combine fuzzy and domain matching
        if best_customer and domain_match:
            if best_customer.name == domain_match.name:
                # Both agree - high confidence
                return (
                    best_customer.name,
                    0.90,
                    f"Customer '{best_customer.name}' matched by name and attendee domain",
                )

        if domain_match:
            return (
                domain_match.name,
                0.75,
                f"Customer '{domain_match.name}' matched by attendee domain",
            )

        if best_customer:
            confidence = 0.65 if best_fuzzy_score >= 90 else 0.50
            return (
                best_customer.name,
                confidence,
                f"Customer '{best_customer.name}' fuzzy matched in text",
            )

        # Pattern 5: Check Outlook categories
        for category_name in categories:
            customer = self.config.get_customer_by_name(category_name)
            if customer:
                return (
                    customer.name,
                    0.70,
                    f"Customer '{customer.name}' from Outlook category",
                )

        return None, 0.0, ""

    def _detect_project(self, text: str) -> tuple[Optional[str], float, str]:
        """Detect project from text.

        Args:
            text: Combined subject and body text (lowercase)

        Returns:
            Tuple of (project_name, confidence, reasoning)
        """
        # Check each project for matches
        for project in self.projects:
            names_to_check = [project.name] + project.aliases

            for name in names_to_check:
                name_lower = name.lower()

                # Exact match
                if name_lower in text:
                    return (
                        project.name,
                        0.85,
                        f"Project '{project.name}' mentioned",
                    )

                # Fuzzy match
                score = fuzz.partial_ratio(name_lower, text)
                if score >= 85:
                    return (
                        project.name,
                        0.70,
                        f"Project '{project.name}' fuzzy matched",
                    )

        return None, 0.0, ""

    def _detect_category(
        self, text: str, attendee_emails: list[str], has_customer: bool
    ) -> tuple[str, float, str]:
        """Detect meeting category/type.

        Args:
            text: Combined subject and body text (lowercase)
            attendee_emails: List of attendee email addresses
            has_customer: Whether a customer was detected

        Returns:
            Tuple of (category_name, confidence, reasoning)
        """
        # Special case: If customer detected and keywords match, it's a customer meeting
        if has_customer:
            return "Customer Meeting", 0.85, "Meeting with external customer"

        # Check meeting types by priority
        for meeting_type in self.meeting_types:
            if not meeting_type.keywords:
                continue  # Skip types without keywords (like Uncategorized)

            for keyword in meeting_type.keywords:
                keyword_lower = keyword.lower()

                # Check for keyword match
                if keyword_lower in text:
                    return (
                        meeting_type.name,
                        0.75,
                        f"Keyword '{keyword}' matched for {meeting_type.name}",
                    )

        # Heuristic: Check if all attendees are internal (same domain as you)
        if attendee_emails:
            # Assume emails ending with company domain are internal
            internal_domains = ["company.com", "microsoft.com"]
            all_internal = all(
                any(email.endswith(domain) for domain in internal_domains)
                for email in attendee_emails
            )

            if all_internal:
                return (
                    "Internal Meeting",
                    0.60,
                    "All attendees from internal domain",
                )

        # Default: Uncategorized
        return "Uncategorized", 0.30, "No category patterns detected"

    def _extract_domain(self, email: str) -> str:
        """Extract domain from email address.

        Args:
            email: Email address

        Returns:
            Domain portion (e.g., "example.com")
        """
        if "@" in email:
            return email.split("@")[-1].lower()
        return ""
