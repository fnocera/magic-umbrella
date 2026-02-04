# Task 0.4: Create Configuration File Templates

**Phase:** 0 - Project Setup & Azure Registration
**Estimated Time:** 1 hour
**Dependencies:** Task 0.1 (Project structure)

---

## Description

Create template YAML configuration files for customers, projects, and meeting categories. These files will be used by the classifier to identify and categorize meetings.

---

## Acceptance Criteria

### Configuration Files Created

- [ ] `config/customers.example.yaml` created
- [ ] `config/projects.example.yaml` created
- [ ] `config/categories.example.yaml` created
- [ ] All files documented with comments
- [ ] Example entries provided for guidance

### customers.yaml Structure

- [ ] Customer name field
- [ ] Aliases list for variations
- [ ] Domain list for email matching
- [ ] Optional color for reports
- [ ] Schema validated

### projects.yaml Structure

- [ ] Project name field
- [ ] Aliases list
- [ ] Customer association (optional)
- [ ] Type (internal/customer)
- [ ] Active status
- [ ] Schema validated

### categories.yaml Structure

- [ ] Meeting type names
- [ ] Keywords for detection
- [ ] Color codes for visualization
- [ ] Priority/weight (optional)
- [ ] Schema validated

### Documentation

- [ ] README in config/ directory explaining usage
- [ ] Comments in YAML files explaining each field
- [ ] Instructions for adding new entries
- [ ] Validation instructions

---

## File Templates

### config/customers.example.yaml

```yaml
# Customer Configuration
# Copy this file to customers.yaml and customize for your organization
# This file is used by the classifier to identify customer meetings

customers:
  # Example customer 1
  - name: "Contoso Corporation"
    # Alternative names found in meeting titles
    aliases:
      - "Contoso"
      - "Contoso Corp"
      - "Contoso Ltd"
    # Email domains for attendee matching
    domains:
      - "contoso.com"
      - "contoso.net"
    # Optional: Color for reports (hex code)
    color: "#FF6B6B"

  # Example customer 2
  - name: "Fabrikam Inc"
    aliases:
      - "Fabrikam"
      - "Fabrikam Industries"
    domains:
      - "fabrikam.com"
    color: "#4ECDC4"

  # Example customer 3
  - name: "Northwind Traders"
    aliases:
      - "Northwind"
      - "Northwind Co"
    domains:
      - "northwind.com"
    color: "#45B7D1"

  # Add your customers here
  # - name: "Customer Name"
  #   aliases: ["Alias1", "Alias2"]
  #   domains: ["example.com"]
  #   color: "#HEXCODE"
```

### config/projects.example.yaml

```yaml
# Project Configuration
# Copy this file to projects.yaml and customize for your organization
# This file is used to identify project-related meetings

projects:
  # Customer project example
  - name: "Project Alpha"
    aliases:
      - "Alpha"
      - "Proj-Alpha"
      - "Alpha Initiative"
    customer: "Contoso Corporation"  # Links to customer
    type: "customer"
    active: true

  # Internal project example
  - name: "Platform Migration"
    aliases:
      - "Platform Mig"
      - "Migration Project"
    customer: null  # No associated customer
    type: "internal"
    active: true

  # Completed project example
  - name: "Legacy System Upgrade"
    aliases:
      - "Legacy Upgrade"
    type: "internal"
    active: false  # Completed projects

  # Add your projects here
  # - name: "Project Name"
  #   aliases: ["Alias1"]
  #   customer: "Customer Name" or null
  #   type: "customer" or "internal"
  #   active: true or false
```

### config/categories.example.yaml

```yaml
# Meeting Category Configuration
# This file defines meeting types and keywords for detection

meeting_types:
  # Customer-facing meetings
  - name: "Customer Meeting"
    description: "External meetings with customers"
    keywords:
      - "customer"
      - "client"
      - "external"
      - "demo"
      - "presentation"
    color: "#FF6B6B"
    priority: 10  # Higher priority = checked first

  # Internal project work
  - name: "Internal Project"
    description: "Work on internal projects and initiatives"
    keywords:
      - "internal"
      - "project"
      - "development"
      - "feature"
      - "sprint"
    color: "#4ECDC4"
    priority: 9

  # One-on-one meetings
  - name: "1:1 Meeting"
    description: "One-on-one meetings with colleagues"
    keywords:
      - "1:1"
      - "1-1"
      - "one on one"
      - "one-on-one"
      - "check in"
      - "skip level"
    color: "#45B7D1"
    priority: 8

  # Team meetings
  - name: "Team Meeting"
    description: "Team syncs, standups, and all-hands"
    keywords:
      - "team sync"
      - "team meeting"
      - "standup"
      - "daily scrum"
      - "all hands"
      - "weekly sync"
    color: "#96CEB4"
    priority: 7

  # Administrative tasks
  - name: "Administrative"
    description: "Admin work, HR, expenses, etc."
    keywords:
      - "admin"
      - "hr"
      - "human resources"
      - "expense"
      - "timesheet"
      - "benefits"
      - "onboarding"
    color: "#FFEAA7"
    priority: 6

  # Training and development
  - name: "Training"
    description: "Learning, workshops, courses"
    keywords:
      - "training"
      - "workshop"
      - "course"
      - "learning"
      - "certification"
      - "lunch and learn"
    color: "#DFE6E9"
    priority: 5

  # Social/informal
  - name: "Social"
    description: "Coffee chats, social events"
    keywords:
      - "coffee chat"
      - "social"
      - "happy hour"
      - "team lunch"
      - "celebration"
    color: "#FDCB6E"
    priority: 4

  # Uncategorized fallback
  - name: "Uncategorized"
    description: "Could not be categorized"
    keywords: []
    color: "#B2BEC3"
    priority: 0
```

---

## Configuration README

### config/README.md

```markdown
# Configuration Files

This directory contains YAML configuration files used by the Magic Umbrella time allocation system.

## Files

- **customers.yaml** - List of customers and their aliases/domains
- **projects.yaml** - List of projects and their associations
- **categories.yaml** - Meeting type definitions and keywords

## Setup

1. Copy the example files:
   ```bash
   cp customers.example.yaml customers.yaml
   cp projects.example.yaml projects.yaml
   cp categories.example.yaml categories.yaml
   ```

2. Edit each file to add your organization's customers and projects

3. The `.yaml` files are gitignored to protect sensitive information

## Adding a New Customer

```yaml
- name: "Full Customer Name"
  aliases: ["Short Name", "Alternative Name"]
  domains: ["customerdomain.com"]
  color: "#HEXCOLOR"
```

## Adding a New Project

```yaml
- name: "Project Name"
  aliases: ["Alias"]
  customer: "Customer Name" # or null for internal
  type: "customer" # or "internal"
  active: true # or false if completed
```

## Validation

Run validation to check YAML syntax:
```bash
uv run python -m magic_umbrella.config.validator
```
```

---

## Schema Definition (Optional)

### Pydantic Models for Validation

```python
# src/magic_umbrella/config/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class Customer(BaseModel):
    """Customer configuration schema."""
    name: str
    aliases: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    color: Optional[str] = None

class Project(BaseModel):
    """Project configuration schema."""
    name: str
    aliases: List[str] = Field(default_factory=list)
    customer: Optional[str] = None
    type: str = Field(pattern="^(customer|internal)$")
    active: bool = True

class MeetingType(BaseModel):
    """Meeting type schema."""
    name: str
    description: str
    keywords: List[str] = Field(default_factory=list)
    color: str
    priority: int = 0
```

---

## Testing Checklist

- [ ] YAML files parse without errors
- [ ] Example entries are realistic
- [ ] All required fields present
- [ ] Comments are clear and helpful
- [ ] README explains usage
- [ ] .gitignore excludes non-example files

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 755-804)
- YAML Specification: https://yaml.org/spec/

---

## Validation Steps

1. Copy example files to active config files
2. Edit with real data
3. Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('config/customers.yaml'))"`
4. Load in application and verify parsing
