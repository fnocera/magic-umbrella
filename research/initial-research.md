# Initial Research: Calendar-Based Time Allocation System

**Date:** February 3, 2026
**Purpose:** Research document for building an agentic system to analyze calendar meetings and determine time allocation across customers, projects, and activities.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Microsoft Graph Calendar API](#microsoft-graph-calendar-api)
4. [Authentication & Security](#authentication--security)
5. [Azure Hosting Options](#azure-hosting-options)
6. [AI/ML Approaches for Meeting Categorization](#aiml-approaches-for-meeting-categorization)
7. [Python Libraries & Tools](#python-libraries--tools)
8. [Architecture Considerations](#architecture-considerations)
9. [Data Model & Convention Standards](#data-model--convention-standards)
10. [Potential Challenges](#potential-challenges)
11. [Recommended Next Steps](#recommended-next-steps)

---

## Problem Statement

**Current Challenge:**
- Team members struggle with time tracking and entering activities into internal systems
- Manual entry is time-consuming and often inaccurate
- Need to understand time allocation across customers, projects, internal work, and 1:1 meetings
- Different people label meetings differently, making categorization difficult

**Desired Outcome:**
- Automated analysis of weekly calendar to show time allocation breakdown
- Identify customer-specific work vs. internal projects vs. administrative time
- Reduce manual time entry burden
- Establish conventions to make future categorization easier
- Include a validation loop where users can interactively edit time allocations to account for prep time or follow-up activities associated with meetings

---

## Solution Overview

### High-Level Approach

Build a Python-based agentic system that:
1. **Connects** to Microsoft Graph API to retrieve Outlook/Teams calendar data
2. **Analyzes** meeting metadata (title, description, participants, organizer)
3. **Categorizes** meetings using AI/ML to identify customers, projects, or activity types
4. **Generates** weekly time allocation reports
5. **Learns** from user feedback to improve categorization over time
6. **Suggests** naming conventions to users based on patterns

### Target Users
- Initial: Individual use (you)
- Future: Team-wide deployment

---

## Microsoft Graph Calendar API

### Key Capabilities

The Calendar API provides comprehensive access to calendar data:

#### **Available Operations**
- **List Events**: Retrieve all events within a time range using `calendarView`
- **Event Details**: Access single instances, recurring series, and exceptions
- **Meeting Information**: Get attendees, organizer, location, online meeting details
- **Availability**: Query free/busy schedules (for future features)

#### **Event Data Structure**

Key properties available from calendar events:
```json
{
  "id": "string",
  "subject": "Customer X - Project Planning",
  "body": {
    "content": "Discuss Q1 deliverables",
    "contentType": "HTML"
  },
  "start": {"dateTime": "2026-02-03T14:00:00", "timeZone": "UTC"},
  "end": {"dateTime": "2026-02-03T15:00:00", "timeZone": "UTC"},
  "organizer": {"emailAddress": {"name": "string", "address": "string"}},
  "attendees": [
    {"emailAddress": {"name": "string", "address": "string"}, "type": "required"}
  ],
  "onlineMeeting": {
    "joinUrl": "https://teams.microsoft.com/...",
    "conferenceId": "string"
  },
  "categories": ["Customer A", "Project X"],
  "isOrganizer": true,
  "responseStatus": "accepted",
  "showAs": "busy"
}
```

#### **Required Permissions**

Graph API requires delegated permissions:
- `Calendars.Read` - Read-only access to user calendars
- `Calendars.ReadWrite` - Read/write access (for future features like categorization)
- `Calendars.ReadWrite.Shared` - Access to shared calendars

#### **API Endpoints**

```bash
# Get user's calendar events for a date range
GET https://graph.microsoft.com/v1.0/me/calendar/calendarView
  ?startDateTime=2026-02-03T00:00:00Z
  &endDateTime=2026-02-09T23:59:59Z

# Get specific event details
GET https://graph.microsoft.com/v1.0/me/events/{event-id}

# List all calendars (for users with multiple)
GET https://graph.microsoft.com/v1.0/me/calendars
```

---

## Authentication & Security

### Microsoft Identity Platform (OAuth 2.0)

#### **Authentication Flow Types**

1. **Delegated Access (Recommended for this use case)**
   - User signs in and grants permission to the app
   - App accesses Graph API on behalf of the signed-in user
   - Uses OAuth 2.0 Authorization Code Flow
   - User can revoke access at any time

2. **Application Permissions**
   - App accesses data with its own identity (no user sign-in)
   - Requires admin consent
   - Not recommended for individual user tools

#### **OAuth 2.0 Authorization Code Flow**

**Step 1: Request Authorization**
```
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
  ?client_id={app-id}
  &response_type=code
  &redirect_uri=http://localhost:8000/callback
  &scope=offline_access Calendars.Read User.Read
  &state={random-state}
```

**Step 2: Exchange Code for Token**
```python
# User is redirected back with authorization code
# App exchanges code for access token + refresh token
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
  client_id={app-id}
  &code={authorization-code}
  &grant_type=authorization_code
  &redirect_uri=http://localhost:8000/callback
  &client_secret={client-secret}  # For web apps
```

**Step 3: Call Microsoft Graph**
```python
GET https://graph.microsoft.com/v1.0/me/calendar/calendarView
Authorization: Bearer {access-token}
```

**Step 4: Refresh Token**
```python
# When access token expires (typically 1 hour)
# Use refresh token to get new access token
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
  grant_type=refresh_token
  &refresh_token={refresh-token}
  &client_id={app-id}
```

#### **Python Authentication Libraries**

**Primary Library: `azure-identity`**
```bash
pip install azure-identity msal
```

**`DefaultAzureCredential` Approach (Recommended)**
```python
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from msgraph import GraphServiceClient

# For local development - prompts user to sign in via browser
credential = InteractiveBrowserCredential(
    client_id="your-app-id",
    tenant_id="your-tenant-id"
)

# Initialize Graph client
graph_client = GraphServiceClient(credentials=credential)
```

**Token Management Best Practices:**
- Store refresh tokens securely (encrypted local storage or key vault)
- Never store tokens in code or version control
- Use `DefaultAzureCredential` for automatic credential chain
- Implement proper error handling for token expiration

#### **Security Considerations**

1. **Principle of Least Privilege**
   - Request only necessary permissions (`Calendars.Read` initially)
   - Avoid `Calendars.ReadWrite` unless categorization features require it

2. **Token Storage**
   - Use Azure Key Vault for production deployments
   - For local development: encrypted local cache with OS keyring integration
   - Never log tokens

3. **User Consent**
   - Clearly explain what data the app accesses
   - Show privacy policy and data usage
   - Allow users to revoke access easily

4. **App Registration Requirements**
   - Register app in Microsoft Entra ID (Azure AD)
   - Configure redirect URIs
   - Generate client secret (store in Azure Key Vault)
   - Set up API permissions

---

## Azure Hosting Options

### Python Deployment Options on Azure

#### **Option 1: Azure App Service (Recommended for MVP)**

**Pros:**
- Fully managed platform (PaaS)
- Built-in support for Python (Linux app service plan)
- Easy CI/CD integration with GitHub Actions
- Auto-scaling capabilities
- Built-in authentication/authorization
- HTTPS by default

**Cons:**
- Higher cost than serverless for infrequent use
- May be overkill for single-user tool initially

**Use Case:**
- Team-wide deployment with web interface
- Continuous availability required
- Need for background processing

**Estimated Cost:**
- Basic tier (B1): ~$13/month
- Standard tier (S1): ~$70/month (auto-scaling, custom domains)

#### **Option 2: Azure Functions (Good for Scheduled Analysis)**

**Pros:**
- Serverless - pay only for execution time
- Excellent for scheduled jobs (e.g., weekly analysis)
- Scales automatically
- Low cost for infrequent use
- Python support (Linux-based)

**Cons:**
- Cold start latency
- Execution time limits (10 minutes default, 60 max)
- More complex for interactive applications

**Use Case:**
- Scheduled weekly reports
- Event-driven processing
- Cost-sensitive deployments

**Estimated Cost:**
- Consumption plan: First 1M executions free, then $0.20/million

#### **Option 3: Azure Container Apps**

**Pros:**
- Microservices-friendly
- Kubernetes-based but simplified
- Good for complex applications
- Supports background jobs and APIs

**Cons:**
- More complex setup
- Overkill for simple use case

**Use Case:**
- Future multi-service architecture
- Need for Kubernetes features without complexity

#### **Option 4: Azure Virtual Machines / Local Development**

**Pros:**
- Full control
- No platform constraints
- Can run locally initially

**Cons:**
- Manual OS/security management
- Less cost-effective
- No built-in scaling

**Use Case:**
- Initial development and testing
- Proof of concept

### Recommended Approach

**Phase 1 (MVP):** Run locally or deploy to Azure App Service (Basic tier)
**Phase 2 (Team Rollout):** Azure Functions for scheduled analysis + App Service for web UI
**Phase 3 (Scale):** Container Apps or enhanced App Service with auto-scaling

---

## AI/ML Approaches for Meeting Categorization

### Categorization Strategies

#### **Approach 1: LLM-Based Classification (Recommended)**

**Model Options:**
1. **Azure OpenAI Service**
   - GPT-4o or GPT-4o-mini for classification
   - Excellent at understanding context and nuance
   - Can handle unstructured meeting titles/descriptions
   - Supports few-shot learning with examples

2. **Azure AI Foundry (formerly Azure Machine Learning)**
   - Host open-source models (Llama, Mistral)
   - More cost-effective at scale
   - Requires more setup

**Implementation Approach:**
```python
# Pseudo-code for LLM-based categorization
def categorize_meeting(meeting_title, meeting_body, attendees):
    prompt = f"""
    Analyze this calendar meeting and categorize it:

    Title: {meeting_title}
    Description: {meeting_body}
    Attendees: {attendees}

    Categories:
    - Customer name (if customer meeting)
    - Project name (if project-related)
    - Meeting type: [Customer Meeting, Internal Project, 1:1, Team Meeting,
                    Administrative, Training, Social]

    Known customers: [Customer X, Customer Y, Customer Z]
    Known projects: [Project Alpha, Project Beta]

    Return JSON:
    {{
      "customer": "Customer X or null",
      "project": "Project Alpha or null",
      "meeting_type": "Customer Meeting",
      "confidence": 0.95,
      "reasoning": "Title contains customer name"
    }}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

**Pros:**
- Handles ambiguity and natural language well
- Can learn from few-shot examples
- No training required
- Adapts to new customers/projects easily

**Cons:**
- API costs (though minimal for weekly analysis)
- Requires internet connectivity
- Privacy considerations (meeting data sent to LLM)

**Cost Estimate:**
- GPT-4o-mini: ~$0.15 per 1M input tokens
- Analyzing 50 meetings/week: ~500 tokens each = 25K tokens = $0.004/week = $0.20/year

#### **Approach 2: Rule-Based Classification with NLP**

**Libraries:**
- `spaCy` for named entity recognition
- `fuzzywuzzy` for fuzzy string matching
- Regular expressions for pattern matching

**Implementation:**
```python
import spacy
from fuzzywuzzy import fuzz

# Define known entities
CUSTOMERS = ["Customer X", "Customer Y", "Contoso", "Fabrikam"]
PROJECTS = ["Project Alpha", "Project Beta", "Initiative Gamma"]

def classify_meeting_rule_based(title, description):
    text = f"{title} {description}".lower()

    # Check for customer matches
    for customer in CUSTOMERS:
        if customer.lower() in text or fuzz.partial_ratio(customer, text) > 85:
            return {"customer": customer, "type": "Customer Meeting"}

    # Check for project keywords
    for project in PROJECTS:
        if project.lower() in text:
            return {"project": project, "type": "Internal Project"}

    # 1:1 detection
    if "1:1" in text or "one on one" in text or "1-1" in text:
        return {"type": "1:1 Meeting"}

    return {"type": "Uncategorized"}
```

**Pros:**
- No API costs
- Fast execution
- Complete data privacy
- Deterministic results

**Cons:**
- Requires manual rule maintenance
- Struggles with ambiguity
- Needs user to establish conventions
- Less flexible

#### **Approach 3: Hybrid Approach (Best of Both Worlds)**

1. **First Pass:** Rule-based classification with high-confidence patterns
2. **Second Pass:** LLM for low-confidence or ambiguous meetings
3. **Learning:** Track user corrections to improve rules over time

```python
def categorize_with_hybrid(meeting):
    # Try rule-based first
    result = classify_rule_based(meeting)

    if result["confidence"] > 0.8:
        return result

    # Fall back to LLM for ambiguous cases
    return categorize_with_llm(meeting)
```

#### **Approach 4: Azure AI Language Service**

**Custom Text Classification:**
- Train custom model on your labeled meetings
- Hosted on Azure
- Good privacy controls

**Pros:**
- Purpose-built for classification
- Good enterprise integration
- Compliance-friendly

**Cons:**
- Requires labeled training data (50-100+ examples per category)
- Setup complexity
- Less flexible than LLM approaches

### Recommended Approach

**Start with:** Hybrid approach (rule-based + GPT-4o-mini fallback)
**Evolve to:** Full LLM-based with user feedback loop
**Long-term:** Custom fine-tuned model if handling sensitive data

---

## Python Libraries & Tools

### Core Libraries

#### **Microsoft Graph API**
```bash
pip install msgraph-sdk        # Official Microsoft Graph SDK
pip install azure-identity     # Authentication
```

#### **Azure Services**
```bash
pip install azure-keyvault-secrets    # Secure credential storage
pip install openai                     # Azure OpenAI integration
```

#### **Data Processing**
```bash
pip install pandas                # Data analysis and reporting
pip install python-dateutil       # Date/time manipulation
pip install pytz                  # Timezone handling
```

#### **NLP/ML (if using rule-based)**
```bash
pip install spacy                 # NLP processing
pip install fuzzywuzzy            # Fuzzy string matching
pip install python-Levenshtein    # Fast string comparison
```

#### **Web Framework (for UI)**
```bash
pip install fastapi               # Modern Python API framework
pip install uvicorn               # ASGI server
pip install jinja2                # Template engine
# OR
pip install flask                 # Traditional web framework
```

#### **Testing & Development**
```bash
pip install pytest                # Testing framework
pip install python-dotenv         # Environment variable management
pip install ruff                  # Linting/formatting
```

### Example Project Structure

```
time-allocation-system/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── microsoft_auth.py      # OAuth flow handling
│   ├── calendar/
│   │   ├── __init__.py
│   │   ├── graph_client.py        # Microsoft Graph API wrapper
│   │   └── event_parser.py        # Parse calendar events
│   ├── categorization/
│   │   ├── __init__.py
│   │   ├── llm_classifier.py      # LLM-based classification
│   │   ├── rule_classifier.py     # Rule-based classification
│   │   └── hybrid_classifier.py   # Combined approach
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── time_allocation.py     # Calculate time breakdown
│   │   └── report_generator.py    # Generate reports
│   └── main.py                     # CLI entry point
├── tests/
│   ├── test_auth.py
│   ├── test_classification.py
│   └── test_reporting.py
├── config/
│   ├── customers.yaml              # Known customers list
│   ├── projects.yaml               # Known projects list
│   └── categories.yaml             # Category definitions
├── .env.example                    # Environment variables template
├── pyproject.toml
└── README.md
```

---

## Architecture Considerations

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│              CLI / Web Interface                             │
│  - Authenticate user                                         │
│  - Select date range                                         │
│  - Display results                                           │
│  - Collect feedback                                          │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│           Calendar Service                                   │
│  - Microsoft Graph API client                                │
│  - Token management                                          │
│  - Event retrieval and caching                               │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│        Categorization Engine                                 │
│  ┌──────────────────┐      ┌────────────────────┐          │
│  │  Rule-Based      │──────│  LLM Classifier    │          │
│  │  Classifier      │      │  (Azure OpenAI)    │          │
│  └──────────────────┘      └────────────────────┘          │
│                │                    │                        │
│                └────────┬───────────┘                        │
│                         ▼                                    │
│                  ┌──────────────┐                           │
│                  │   Hybrid     │                           │
│                  │  Classifier  │                           │
│                  └──────────────┘                           │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│          Time Allocation Calculator                          │
│  - Aggregate meeting durations by category                   │
│  - Calculate percentages                                     │
│  - Generate insights                                         │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│          Report Generator                                    │
│  - Formatted text reports                                    │
│  - CSV export for timesheet systems                          │
│  - Visual charts (optional)                                  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Authentication:** User authenticates via OAuth 2.0, receives access token
2. **Fetch Calendar:** Retrieve calendar events for specified date range
3. **Parse Events:** Extract relevant metadata (title, description, duration, attendees)
4. **Categorize:** Run through classification engine
5. **Calculate:** Aggregate time by category
6. **Report:** Generate human-readable and machine-readable outputs
7. **Feedback Loop (Optional):** User confirms/corrects categories, system learns

### Deployment Architecture Options

#### **Option A: Desktop Application (Initial)**
```
User's Machine
├── Python CLI Application
├── Local Token Cache (encrypted)
├── Local Configuration (customers.yaml, projects.yaml)
└── Output Reports (CSV, TXT)
```

#### **Option B: Web Application (Team Deployment)**
```
Azure App Service
├── FastAPI Web Application
├── Azure Key Vault (credentials)
├── Azure Blob Storage (reports)
└── Azure Application Insights (monitoring)
```

#### **Option C: Serverless (Scheduled Reports)**
```
Azure Functions (Timer Trigger - Weekly)
├── Fetch calendar events
├── Categorize meetings
├── Generate report
└── Email to user (via Azure Communication Services)
```

---

## Data Model & Convention Standards

### Meeting Data Structure

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class CalendarMeeting:
    id: str
    subject: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    organizer: str
    attendees: List[str]
    body: Optional[str]
    online_meeting_url: Optional[str]
    categories: List[str]  # User-defined categories in Outlook
    is_all_day: bool
    response_status: str  # accepted, tentative, declined

@dataclass
class MeetingCategory:
    customer: Optional[str]
    project: Optional[str]
    meeting_type: str  # Customer, Internal, 1:1, Team, Admin, Training
    confidence: float
    reasoning: str
    tags: List[str]

@dataclass
class TimeAllocation:
    date_range: tuple[datetime, datetime]
    total_hours: float
    breakdown: dict[str, float]  # category -> hours
    meetings: List[tuple[CalendarMeeting, MeetingCategory]]
```

### Naming Convention Recommendations

To improve automatic categorization, suggest these conventions to users:

#### **Customer Meetings**
```
✅ Good:
- "Customer X - Quarterly Business Review"
- "[Contoso] Project planning"
- "Fabrikam: Technical discussion"

❌ Ambiguous:
- "Business review" (which customer?)
- "Project planning" (which project?)
```

#### **Internal Projects**
```
✅ Good:
- "Project Alpha - Sprint Planning"
- "[Internal] Initiative Beta Review"
- "Platform Team - Architecture Sync"

❌ Ambiguous:
- "Sprint planning"
- "Team sync"
```

#### **1:1 Meetings**
```
✅ Good:
- "1:1 with John"
- "One on one - Jane"
- "1-1 Career Discussion"

✅ Detected automatically by most systems
```

#### **Administrative/Meta**
```
✅ Good:
- "[Admin] Expense approvals"
- "[HR] Benefits enrollment"
- "Training: Azure Fundamentals"

✅ Use brackets or prefixes for non-project work
```

### Configuration Files

#### **customers.yaml**
```yaml
customers:
  - name: "Customer X"
    aliases: ["CustX", "Customer-X", "CustomerX"]
    domains: ["customerx.com"]

  - name: "Contoso"
    aliases: ["Contoso Ltd", "Contoso Corp"]
    domains: ["contoso.com", "contoso.net"]
```

#### **projects.yaml**
```yaml
projects:
  - name: "Project Alpha"
    aliases: ["Alpha", "Proj-Alpha"]
    customer: "Customer X"
    active: true

  - name: "Internal Platform"
    type: "internal"
    team: "Engineering"
```

#### **categories.yaml**
```yaml
meeting_types:
  - name: "Customer Meeting"
    keywords: ["customer", "client", "external"]
    color: "#FF6B6B"

  - name: "Internal Project"
    keywords: ["internal", "project", "development"]
    color: "#4ECDC4"

  - name: "1:1 Meeting"
    keywords: ["1:1", "one on one", "1-1", "one-on-one"]
    color: "#45B7D1"

  - name: "Team Meeting"
    keywords: ["team sync", "standup", "all hands"]
    color: "#96CEB4"

  - name: "Administrative"
    keywords: ["admin", "hr", "expense", "timesheet"]
    color: "#FFEAA7"
```

---

## Potential Challenges

### 1. **Ambiguous Meeting Titles**

**Problem:**
- "Quick sync" - with whom? About what?
- "Follow-up" - which customer/project?
- Generic titles with no context

**Solutions:**
- Analyze attendee email domains (e.g., @customer.com = customer meeting)
- Check meeting body for additional context
- Prompt user for clarification on low-confidence classifications
- Build learning system: remember user corrections

### 2. **Multi-Purpose Meetings**

**Problem:**
- Meeting covers multiple customers or projects
- 50% Customer X, 50% Customer Y
- How to allocate time?

**Solutions:**
- Allow multi-category assignments with percentages
- Let user manually split allocations
- Default to primary detected category if unclear

### 3. **Privacy & Data Sensitivity**

**Problem:**
- Meeting details may contain confidential information
- Sending to external LLM API raises concerns
- Regulatory compliance (GDPR, CCPA)

**Solutions:**
- Anonymize attendee names/emails before processing
- Only send meeting title and sanitized description to LLM
- Option to use local models (Ollama, Azure AI Foundry)
- Clear privacy policy and user consent

### 4. **Token Management & Expiration**

**Problem:**
- Access tokens expire after 1 hour
- Refresh tokens can be revoked
- Users need to re-authenticate periodically

**Solutions:**
- Implement robust token refresh logic
- Store refresh tokens securely
- Graceful degradation with re-auth prompt
- Test token health before API calls

### 5. **Varying Calendar Patterns**

**Problem:**
- Some users have 50+ meetings/week
- Others have 10-15 meetings/week
- Block-scheduled focus time vs. packed calendars

**Solutions:**
- Handle both sparse and dense calendars
- Exclude focus time, personal appointments, lunch blocks
- Use `showAs` field to filter "free" or "out of office" events

### 6. **Time Zone Handling**

**Problem:**
- Users in different time zones
- Daylight saving time transitions
- Meeting times in UTC vs. local time

**Solutions:**
- Use `python-dateutil` and `pytz` for robust datetime handling
- Store all times in UTC internally
- Display in user's local time zone
- Handle DST transitions correctly

### 7. **Recurring Meeting Handling**

**Problem:**
- Weekly team syncs appear as one series
- Need individual instances for proper time allocation
- Cancelled instances should be excluded

**Solutions:**
- Use `calendarView` endpoint (expands recurring series automatically)
- Filter out cancelled occurrences
- Track recurring patterns for better categorization

### 8. **Integration with Internal Systems**

**Problem:**
- Need to export data to internal timesheet systems
- Different format requirements
- API integration complexity

**Solutions:**
- Support multiple export formats (CSV, JSON, Excel)
- Build adapters for common systems
- Allow custom export templates
- API for system-to-system integration

---

## Recommended Next Steps

### Immediate Actions (Research Phase Complete)

1. **Register Application in Azure**
   - Create app registration in Microsoft Entra ID
   - Configure redirect URIs
   - Set API permissions (Calendars.Read)
   - Generate client secret

2. **Set Up Development Environment**
   - Create new Python project with `uv`
   - Install core dependencies: `msgraph-sdk`, `azure-identity`
   - Set up `.env` file for credentials

3. **Proof of Concept Goals**
   - Authenticate user via OAuth 2.0
   - Retrieve calendar events for current week
   - Display meeting titles and durations
   - Basic rule-based categorization (customer name in title)

4. **Create Configuration Files**
   - `customers.yaml` with your known customers
   - `projects.yaml` with active projects
   - `categories.yaml` with meeting types

### Planning Phase

5. **Define MVP Scope**
   - Authentication and calendar access ✅
   - Basic categorization (hybrid approach) ✅
   - CLI-based weekly report ✅
   - CSV export for timesheet ✅

6. **Out of Scope for MVP**
   - Web interface (future)
   - Multi-user support (future)
   - Real-time classification (future)
   - Integration with internal systems (future)

### Development Phases

**Phase 1: Authentication & Data Access (Week 1)**
- Implement OAuth flow
- Fetch calendar events
- Parse event metadata
- Store credentials securely

**Phase 2: Categorization Engine (Week 2)**
- Rule-based classifier with customer/project matching
- LLM fallback for ambiguous cases
- Confidence scoring
- User feedback mechanism

**Phase 3: Reporting & Analytics (Week 3)**
- Time allocation calculator
- CLI report generator
- CSV export format
- Weekly summary email (optional)

**Phase 4: Refinement & Testing (Week 4)**
- Test with real calendar data
- Tune classification rules
- Handle edge cases
- Documentation

**Phase 5: Team Rollout (Future)**
- Deploy to Azure App Service
- Multi-user authentication
- Web interface
- Admin dashboard

---

## Key Resources

### Documentation
- [Microsoft Graph Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [Microsoft Graph Python SDK](https://learn.microsoft.com/en-us/graph/sdks/sdks-overview)
- [Azure Identity for Python](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Code Examples
- [Microsoft Graph Python Samples](https://github.com/microsoftgraph/msgraph-sdk-python)
- [Azure Identity Examples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)

### Tools
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) - Test API calls interactively
- [Azure Portal](https://portal.azure.com) - App registration and resource management

---

## Conclusion

This solution is highly feasible and aligned with Microsoft's technology stack. The hybrid categorization approach balances accuracy, cost, and privacy concerns. Starting with a CLI-based MVP allows for rapid iteration and user feedback before investing in team-wide deployment infrastructure.

**Estimated Development Time:** 3-4 weeks for MVP
**Estimated Azure Cost:** $5-20/month (depending on hosting choice and LLM usage)
**Key Success Factors:**
- User adoption of naming conventions
- Iterative improvement based on feedback
- Secure handling of calendar data
- Clear value proposition (time savings vs. manual entry)

**Risks:**
- Low user adoption if categorization accuracy is poor
- Privacy concerns from team members
- Maintenance burden of customer/project lists

**Mitigation:**
- Start with personal use to validate approach
- Transparent privacy controls and local-first options
- Self-service configuration for users to manage their own lists
