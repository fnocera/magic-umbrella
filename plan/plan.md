# Implementation Plan: Calendar-Based Time Allocation System

**Project:** Magic Umbrella
**Version:** 1.0 (MVP)
**Last Updated:** February 2026
**Target Timeline:** 3-5 days with AI assistance

---

## Table of Contents

1. [Overview](#overview)
2. [MVP Scope](#mvp-scope)
3. [Implementation Phases](#implementation-phases)
4. [Success Criteria](#success-criteria)

---

## Overview

This plan outlines the implementation strategy for building an agentic system that analyzes Microsoft Outlook/Teams calendar meetings to determine time allocation across customers, projects, and activities.

**Target:** Individual use first, team deployment later
**Timeline:** 4-5 weeks for MVP
**Technology:** Python 3.9+, Microsoft Graph API, Azure OpenAI

---

## MVP Scope

### In Scope ✅

- OAuth 2.0 authentication with Microsoft Graph
- Fetch calendar events for specified date range
- Hybrid categorization (rule-based + LLM fallback)
- Interactive validation loop for time adjustments
- CLI interface for weekly reports
- CSV export for timesheet integration
- Local configuration (customers, projects, categories)

### Out of Scope ❌

- Web interface (Phase 2)
- Multi-user support (Phase 2)
- Real-time sync (Future)
- Azure hosting (Local development only for MVP)
- Integration with internal timesheet APIs (Future)

---

## Implementation Phases

### [ ] Phase 0: Project Setup & Azure Registration
**Duration:** 1-2 days
**Goal:** Prepare development environment and Azure infrastructure

* [ ] Task 0.1: Create project structure and scaffold
  * Details: [plan/details/phase-0-project-setup.md](details/phase-0-project-setup.md) (Lines 1-40)

* [ ] Task 0.2: Register application in Microsoft Entra ID
  * Details: [plan/details/phase-0-azure-registration.md](details/phase-0-azure-registration.md) (Lines 1-50)

* [ ] Task 0.3: Set up development environment and dependencies
  * Details: [plan/details/phase-0-dev-environment.md](details/phase-0-dev-environment.md) (Lines 1-45)

* [ ] Task 0.4: Create configuration file templates
  * Details: [plan/details/phase-0-configuration.md](details/phase-0-configuration.md) (Lines 1-35)

---

### [ ] Phase 1: Authentication & Calendar Access
**Duration:** 1 week
**Goal:** Authenticate users and fetch calendar events from Microsoft Graph

* [ ] Task 1.1: Implement OAuth 2.0 authentication flow
  * Details: [plan/details/phase-1-oauth-flow.md](details/phase-1-oauth-flow.md) (Lines 1-80)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 123-229)

* [ ] Task 1.2: Implement secure token storage
  * Details: [plan/details/phase-1-token-storage.md](details/phase-1-token-storage.md) (Lines 1-55)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 202-218)

* [ ] Task 1.3: Create Microsoft Graph client wrapper
  * Details: [plan/details/phase-1-graph-client.md](details/phase-1-graph-client.md) (Lines 1-70)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 59-120)

* [ ] Task 1.4: Implement calendar event fetcher
  * Details: [plan/details/phase-1-event-fetcher.md](details/phase-1-event-fetcher.md) (Lines 1-65)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 65-69, 106-119)

* [ ] Task 1.5: Create event parser and data models
  * Details: [plan/details/phase-1-event-parser.md](details/phase-1-event-parser.md) (Lines 1-75)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 668-705)

---

### [ ] Phase 2: Categorization Engine
**Duration:** 1 week
**Goal:** Classify meetings by customer, project, and meeting type

* [ ] Task 2.1: Implement rule-based classifier
  * Details: [plan/details/phase-2-rule-classifier.md](details/phase-2-rule-classifier.md) (Lines 1-85)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 392-439)

* [ ] Task 2.2: Implement LLM-based classifier with Azure OpenAI
  * Details: [plan/details/phase-2-llm-classifier.md](details/phase-2-llm-classifier.md) (Lines 1-90)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 325-391)

* [ ] Task 2.3: Create hybrid classification orchestrator
  * Details: [plan/details/phase-2-hybrid-classifier.md](details/phase-2-hybrid-classifier.md) (Lines 1-60)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 440-456)

* [ ] Task 2.4: Implement confidence scoring system
  * Details: [plan/details/phase-2-confidence-scoring.md](details/phase-2-confidence-scoring.md) (Lines 1-50)

* [ ] Task 2.5: Load and parse configuration files (customers, projects)
  * Details: [plan/details/phase-2-config-loader.md](details/phase-2-config-loader.md) (Lines 1-55)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 755-804)

---

### [ ] Phase 3: Time Allocation & Reporting
**Duration:** 2-3 days
**Goal:** Calculate time breakdowns and generate basic terminal output

* [ ] Task 3.1: Implement time allocation calculator
  * Details: [plan/details/phase-3-time-calculator.md](details/phase-3-time-calculator.md) (Lines 1-70)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 609-614)

* [ ] Task 3.2: Create simple terminal output for reports
  * Details: [plan/details/phase-3-terminal-output.md](details/phase-3-terminal-output.md) (Lines 1-50)
  * Note: Basic terminal display using rich.console

---

### [ ] Phase 4: Interactive Validation Loop
**Duration:** 2-3 days
**Goal:** Allow users to review and adjust time allocations

* [ ] Task 4.1: Create interactive review interface (CLI)
  * Details: [plan/details/phase-4-interactive-review.md](details/phase-4-interactive-review.md) (Lines 1-75)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 37)
  * **NEW:** Includes time-filling feature for unallocated hours

* [ ] Task 4.2: Implement time adjustment for prep/follow-up
  * Details: [plan/details/phase-4-time-adjustments.md](details/phase-4-time-adjustments.md) (Lines 1-65)

* [ ] Task 4.3: Save and persist user corrections
  * Details: [plan/details/phase-4-persistence.md](details/phase-4-persistence.md) (Lines 1-55)

* [ ] Task 4.4: Add learning from user feedback
  * Details: [plan/details/phase-4-learning.md](details/phase-4-learning.md) (Lines 1-60)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 50)

* [ ] Task 4.5: Implement CSV export functionality
  * Details: [plan/details/phase-4-csv-export.md](details/phase-4-csv-export.md) (Lines 1-55)
  * Moved from Phase 3

* [ ] Task 4.6: Add summary statistics and insights
  * Details: [plan/details/phase-4-statistics.md](details/phase-4-statistics.md) (Lines 1-50)
  * Moved from Phase 3

---

### [ ] Phase 5: Testing & Refinement
**Duration:** 1 week
**Goal:** Ensure reliability and handle edge cases

* [ ] Task 5.1: Write unit tests for all modules
  * Details: [plan/details/phase-5-unit-tests.md](details/phase-5-unit-tests.md) (Lines 1-70)

* [ ] Task 5.2: Write integration tests
  * Details: [plan/details/phase-5-integration-tests.md](details/phase-5-integration-tests.md) (Lines 1-65)

* [ ] Task 5.3: Test with real calendar data
  * Details: [plan/details/phase-5-real-data-testing.md](details/phase-5-real-data-testing.md) (Lines 1-50)

* [ ] Task 5.4: Handle edge cases and error scenarios
  * Details: [plan/details/phase-5-edge-cases.md](details/phase-5-edge-cases.md) (Lines 1-80)
  * References: [research/initial-research.md](../research/initial-research.md) (Lines 808-910)

* [ ] Task 5.5: Create user documentation
  * Details: [plan/details/phase-5-documentation.md](details/phase-5-documentation.md) (Lines 1-55)

* [ ] Task 5.6: Performance optimization and tuning
  * Details: [plan/details/phase-5-optimization.md](details/phase-5-optimization.md) (Lines 1-50)

---

## Success Criteria

### MVP Completion Checklist

- [ ] User can authenticate with Microsoft 365 account
- [ ] System fetches calendar events for specified week
- [ ] Meetings are categorized with >80% accuracy
- [ ] User can review and adjust categorizations
- [ ] Weekly report shows time breakdown by customer/project/type
- [ ] CSV export works for timesheet integration
- [ ] All tests pass (unit + integration)
- [ ] Documentation is complete
- [ ] System runs without errors on test data

### Performance Targets

- [ ] Authentication completes in <10 seconds
- [ ] Calendar fetch for 1 week completes in <5 seconds
- [ ] Categorization of 50 meetings completes in <30 seconds
- [ ] Report generation completes in <2 seconds

### Quality Targets

- [ ] Code coverage >80%
- [ ] All Ruff checks pass
- [ ] No security vulnerabilities in dependencies
- [ ] Secrets properly managed (not in code)

---

## Risk Management

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Azure app registration delays | Medium | Start early, use test tenant | ⏳ Pending |
| LLM accuracy below expectations | High | Tune prompts, collect feedback | ⏳ Pending |
| Token management complexity | Medium | Use MSAL library, test thoroughly | ⏳ Pending |
| Edge case handling | Medium | Comprehensive testing, user feedback | ⏳ Pending |

---

## Next Steps

1. ✅ Complete research phase
2. ⏩ Review and approve this plan
3. 🔜 Begin Phase 0: Project Setup
