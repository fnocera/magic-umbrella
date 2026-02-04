# Task 2.1: Implement Rule-Based Classifier

**Phase:** 2 - Categorization Engine
**Estimated Time:** 1 day
**Dependencies:** Task 1.5 (Event parser), Task 2.5 (Config loader)

---

## Description

Implement a rule-based classifier that categorizes calendar meetings by matching patterns in titles and descriptions against known customers, projects, and meeting types. This provides fast, deterministic classification for clear-cut cases.

---

## Acceptance Criteria

### Classifier Module Created

- [x] `src/magic_umbrella/categorization/rule_classifier.py` created ✅
- [x] `RuleBasedClassifier` class implemented ✅
- [x] Pattern matching functions for each category type ✅

### Core Functionality

- [x] Customer name detection (exact and fuzzy matching) ✅
- [x] Project name detection ✅
- [x] Meeting type detection (1:1, Team Meeting, etc.) ✅
- [x] Attendee domain analysis for external meetings ✅
- [x] Outlook category parsing ✅
- [x] Confidence score calculation ✅
- [x] Reasoning explanation generation ✅

### Pattern Matching

- [x] Exact string matching (case-insensitive) ✅
- [x] Fuzzy string matching (>80% similarity using thefuzz) ✅
- [x] Regular expression patterns for common formats ✅
- [x] Prefix/suffix detection ([Customer], Customer:, etc.) ✅
- [x] Keyword matching for meeting types ✅

### Configuration Integration

- [x] Load customers from YAML config ✅
- [x] Load projects from YAML config ✅
- [x] Load meeting type keywords from config ✅
- [x] Support customer aliases ✅
- [x] Support project aliases ✅
- [x] Support domain-based customer detection ✅

### Output Format

- [x] Returns `MeetingClassification` dataclass ✅
- [x] Includes detected customer (if any) ✅
- [x] Includes detected project (if any) ✅
- [x] Includes meeting type ✅
- [x] Includes confidence score (0.0-1.0) ✅
- [x] Includes reasoning text ✅
- [x] Source marked as "rules" ✅

---

## Implementation Details

### Class Structure

```python
# src/magic_umbrella/categorization/rule_classifier.py

from dataclasses import dataclass
from typing import Optional
from fuzzywuzzy import fuzz
import re

@dataclass
class MeetingClassification:
    """Result of meeting classification."""
    customer: Optional[str]
    project: Optional[str]
    meeting_type: str
    confidence: float
    reasoning: str
    source: str = "rules"

class RuleBasedClassifier:
    """Rule-based meeting categorization using pattern matching."""

    def __init__(self, config_loader):
        """Initialize with configuration."""
        self.customers = config_loader.get_customers()
        self.projects = config_loader.get_projects()
        self.meeting_types = config_loader.get_meeting_types()

    def classify(
        self,
        subject: str,
        body: str,
        attendees: list[str],
        categories: list[str]
    ) -> MeetingClassification:
        """Classify a meeting using rules."""
        pass

    def _detect_customer(self, text: str, attendees: list[str]) -> tuple[Optional[str], float]:
        """Detect customer from text and attendee domains."""
        pass

    def _detect_project(self, text: str) -> tuple[Optional[str], float]:
        """Detect project from text."""
        pass

    def _detect_meeting_type(self, text: str, attendees: list[str]) -> tuple[str, float]:
        """Detect meeting type from patterns."""
        pass

    def _check_fuzzy_match(self, target: str, text: str, threshold: int = 80) -> bool:
        """Check if target fuzzy matches any part of text."""
        return fuzz.partial_ratio(target.lower(), text.lower()) > threshold

    def _extract_domain(self, email: str) -> str:
        """Extract domain from email address."""
        return email.split('@')[-1] if '@' in email else ""
```

### Detection Patterns

#### Customer Detection
```python
# Patterns to check (in order of confidence)
CUSTOMER_PATTERNS = [
    r"^\[([^\]]+)\]",  # [Customer Name]
    r"^([^:\-]+):",     # Customer Name:
    r"^([^:\-]+)\s*-",  # Customer Name -
]

# Also check:
# - Fuzzy match customer names/aliases in title
# - Check if attendee domains match customer domains
# - Check Outlook categories for customer names
```

#### Project Detection
```python
PROJECT_PATTERNS = [
    r"Project\s+(\w+)",
    r"\[Internal\].*?([A-Z][a-z]+)",
]
```

#### Meeting Type Detection
```python
MEETING_TYPE_PATTERNS = {
    "1:1": [r"1[:\-]1", r"one[- ]on[- ]one"],
    "Team Meeting": [r"team\s+sync", r"standup", r"all\s+hands"],
    "Administrative": [r"\[admin\]", r"\[hr\]", r"expense", r"timesheet"],
}
```

### Confidence Scoring Logic

```python
def _calculate_confidence(self, matches: dict) -> float:
    """
    Calculate confidence score based on match quality.

    High confidence (0.9-1.0):
    - Exact name match in brackets/prefix
    - Multiple signals (name + domain)

    Medium confidence (0.6-0.9):
    - Fuzzy match with high similarity
    - Domain match without name

    Low confidence (0.3-0.6):
    - Weak fuzzy match
    - Keyword match only

    No match (0.0):
    - No patterns detected
    """
    pass
```

---

## Example Classification Results

### High Confidence Example
```
Subject: "[Contoso] Q1 Planning Session"
Result:
  - customer: "Contoso"
  - meeting_type: "Customer Meeting"
  - confidence: 0.95
  - reasoning: "Customer name 'Contoso' found in bracket prefix"
```

### Medium Confidence Example
```
Subject: "Planning meeting"
Attendees: ["john@fabrikam.com"]
Result:
  - customer: "Fabrikam"
  - meeting_type: "Customer Meeting"
  - confidence: 0.75
  - reasoning: "Attendee domain 'fabrikam.com' matches known customer"
```

### Low Confidence Example
```
Subject: "Quick sync"
Attendees: ["colleague@microsoft.com"]
Result:
  - customer: None
  - meeting_type: "Internal Meeting"
  - confidence: 0.4
  - reasoning: "Generic title, internal attendees only"
```

---

## Testing Checklist

- [ ] Test exact customer name match
- [ ] Test fuzzy customer name match
- [ ] Test customer aliases
- [ ] Test domain-based detection
- [ ] Test project detection
- [ ] Test 1:1 meeting detection
- [ ] Test team meeting detection
- [ ] Test administrative meeting detection
- [ ] Test confidence scoring accuracy
- [ ] Test with ambiguous titles
- [ ] Test with empty body
- [ ] Test with no attendees

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 392-439)
- Configuration: [research/initial-research.md](../../research/initial-research.md) (Lines 755-804)
- Data Model: [research/initial-research.md](../../research/initial-research.md) (Lines 690-697)

---

## Validation Steps

1. Create test dataset with known classifications
2. Run classifier on test set
3. Verify accuracy >70% for clear-cut cases
4. Check confidence scores are reasonable
5. Verify reasoning text is helpful
