# Task 0.1: Create Project Structure and Scaffold

**Phase:** 0 - Project Setup & Azure Registration
**Estimated Time:** 2-3 hours
**Dependencies:** None

---

## Description

Set up the foundational project structure following Python best practices and the architecture outlined in the research document. This includes creating the directory hierarchy, initializing the Python package, and setting up build configuration.

---

## Acceptance Criteria

### Directory Structure Created

- [ ] `src/magic_umbrella/` package directory exists
- [ ] `src/magic_umbrella/__init__.py` created
- [ ] Subpackages created:
  - [ ] `src/magic_umbrella/auth/`
  - [ ] `src/magic_umbrella/calendar/`
  - [ ] `src/magic_umbrella/categorization/`
  - [ ] `src/magic_umbrella/reporting/`
  - [ ] `src/magic_umbrella/config/`
- [ ] `tests/` directory with test structure matching `src/`
- [ ] `config/` directory for YAML configuration files
- [ ] `docs/` directory for documentation

### Configuration Files

- [ ] `pyproject.toml` properly configured with:
  - [ ] Project metadata (name, version, description)
  - [ ] Python version requirement (>=3.9)
  - [ ] Core dependencies listed
  - [ ] Optional dependency groups (dev, nlp, web)
  - [ ] Build system configuration
- [ ] `.env.example` created with required environment variable templates
- [ ] `.gitignore` updated for Python, Azure, and IDE files
- [ ] `README.md` with project overview

### Package Initialization

- [ ] All `__init__.py` files created in package directories
- [ ] Version number exported from main `__init__.py`
- [ ] Package imports functional (`from magic_umbrella import ...`)

---

## Technical Notes

### Directory Structure

```
magic-umbrella/
├── src/
│   └── magic_umbrella/
│       ├── __init__.py
│       ├── auth/
│       │   └── __init__.py
│       ├── calendar/
│       │   └── __init__.py
│       ├── categorization/
│       │   └── __init__.py
│       ├── reporting/
│       │   └── __init__.py
│       └── config/
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_calendar.py
│   ├── test_categorization.py
│   └── test_reporting.py
├── config/
│   ├── customers.example.yaml
│   ├── projects.example.yaml
│   └── categories.example.yaml
├── docs/
│   ├── research/
│   └── guides/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

### Dependencies to Include in pyproject.toml

```toml
dependencies = [
    "msgraph-sdk>=1.0.0",
    "azure-identity>=1.15.0",
    "msal>=1.26.0",
    "openai>=1.10.0",
    "pandas>=2.0.0",
    "python-dateutil>=2.8.0",
    "pytz>=2024.1",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0.0",
]
```

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 529-562)
- Python Project Structure: [research/initial-research.md](../../research/initial-research.md) (Lines 483-527)

---

## Validation Steps

1. Run `uv sync` successfully
2. Import package: `python -c "import magic_umbrella"`
3. Verify all directories exist: `ls -R src/magic_umbrella/`
4. Check pyproject.toml is valid: `uv run python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"`
