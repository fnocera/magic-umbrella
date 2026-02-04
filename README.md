# Magic Umbrella ☔

**Calendar-Based Time Allocation System**

An intelligent Python tool that analyzes your Microsoft Outlook/Teams calendar meetings to automatically determine time allocation across customers, projects, and activities.

## Problem

- Manual time tracking is tedious and error-prone
- Hard to remember how time was spent across the week
- Meetings don't capture prep time or follow-up work
- Different naming conventions make categorization difficult

## Solution

Magic Umbrella automatically:
- 🔐 Authenticates with Microsoft Graph API (OAuth 2.0)
- 📅 Fetches your calendar events for any date range
- 🤖 Categorizes meetings using hybrid AI (rules + LLM)
- ⏱️ Calculates time allocation by customer/project/type
- ✏️ Lets you interactively adjust and fill unallocated time
- 📊 Generates reports for timesheets

## Key Features

- **Hybrid Categorization**: Rule-based patterns + Azure OpenAI for ambiguous cases
- **Interactive Validation**: Review classifications, add prep/follow-up time
- **Time Filling**: Allocate non-meeting hours to background projects
- **CSV Export**: Easy integration with timesheet systems
- **Secure**: OAuth 2.0, encrypted token storage

## Quick Start

### Prerequisites

- Python 3.9+
- Microsoft 365 account
- Azure subscription (for app registration and Azure OpenAI)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/fnocera/magic-umbrella.git
   cd magic-umbrella
   ```

2. **Install dependencies**
   ```bash
   uv sync --extra dev
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

4. **Register Azure app** (see `plan/details/phase-0-azure-registration.md`)

5. **Configure customers and projects**
   ```bash
   cp config/customers.example.yaml config/customers.yaml
   cp config/projects.example.yaml config/projects.yaml
   # Edit with your customers and projects
   ```

## Usage

```bash
# Analyze current week
uv run python -m magic_umbrella analyze --week current

# Analyze specific date range
uv run python -m magic_umbrella analyze --start 2026-02-03 --end 2026-02-09

# Export to CSV
uv run python -m magic_umbrella export --week current --output timesheet.csv
```

## Development

### Dev Container (Recommended)

```bash
# Open in VS Code
code .
# Reopen in Container (Cmd/Ctrl + Shift + P)
```

### Run Tests

```bash
uv run pytest
uv run pytest --cov=magic_umbrella
```

### Code Quality

```bash
uv run ruff check .
uv run ruff format .
```

## Project Structure

```
magic-umbrella/
├── src/magic_umbrella/     # Main package
│   ├── auth/               # OAuth 2.0 authentication
│   ├── calendar/           # Microsoft Graph integration
│   ├── categorization/     # Meeting classification
│   ├── reporting/          # Time allocation & reports
│   └── config/             # Configuration management
├── tests/                   # Test suite
├── config/                  # YAML configuration files
├── docs/                    # Documentation
└── plan/                    # Implementation plan
```

## Technology Stack

- **Python 3.9+**: Core language
- **Microsoft Graph API**: Calendar access
- **Azure OpenAI**: LLM-based classification
- **MSAL**: Microsoft authentication
- **Rich**: Beautiful terminal output
- **Typer**: CLI framework
- **Ruff**: Linting and formatting

## Documentation

- [Implementation Plan](plan/plan.md)
- [Research Document](research/initial-research.md)
- [Azure Setup Guide](plan/details/phase-0-azure-registration.md)
- [Dev Environment Setup](plan/details/phase-0-dev-environment.md)

## Contributing

This project was built with AI assistance from Claude. Pull requests welcome!

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with ❤️ by Federica Nocera with assistance from Claude (Anthropic)
