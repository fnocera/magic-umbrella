# Task 0.3: Set Up Development Environment and Dependencies

**Phase:** 0 - Project Setup & Azure Registration
**Estimated Time:** 1-2 hours
**Dependencies:** Task 0.1 (Project structure)

---

## Description

Configure the development environment with all required dependencies, tools, and IDE settings to enable smooth development workflow.

---

## Acceptance Criteria

### Dependencies Installed

- [ ] Python 3.9+ installed and verified
- [ ] `uv` package manager installed
- [ ] All core dependencies installed via `uv sync`
- [ ] Development dependencies installed via `uv sync --extra dev`
- [ ] Optional dependencies documented

### Environment Configuration

- [ ] `.env` file created from `.env.example`
- [ ] Required environment variables documented
- [ ] `.env` file added to `.gitignore`
- [ ] Sensitive values (API keys, secrets) never committed

### Development Tools

- [ ] Ruff configured for linting and formatting
- [ ] pytest configured for testing
- [ ] Dev container configured for cross-machine compatibility
- [ ] VS Code settings (optional) configured
- [ ] Git hooks (optional) configured

### Verification

- [ ] All imports work: `python -c "import magic_umbrella"`
- [ ] Tests run: `uv run pytest`
- [ ] Linting works: `uv run ruff check .`
- [ ] Formatting works: `uv run ruff format .`
- [ ] Dev container builds successfully (if using)

---

## Dev Container Setup (Recommended)

### Why Use Dev Containers?

- Consistent environment across all machines
- Works on macOS, Windows, Linux
- No local Python installation conflicts
- Includes all tools and dependencies
- Easy team onboarding

### Prerequisites

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Install VS Code: https://code.visualstudio.com/
3. Install Dev Containers extension: `ms-vscode-remote.remote-containers`

### Configuration Files

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "Magic Umbrella Python Dev",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/devcontainers-contrib/features/uv:latest": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "charliermarsh.ruff",
        "ms-python.vscode-pylance"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.testing.pytestEnabled": true,
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff"
        }
      }
    }
  },

  "postCreateCommand": "uv sync --extra dev",

  "forwardPorts": [8000],

  "remoteEnv": {
    "PATH": "${containerEnv:PATH}:${containerWorkspaceFolder}/.venv/bin"
  }
}
```

### Using Dev Container

1. Open project in VS Code
2. Press `Cmd/Ctrl + Shift + P`
3. Select "Dev Containers: Reopen in Container"
4. Wait for container to build (first time only)
5. All dependencies installed automatically

### Dev Container Features

- Python 3.11 pre-installed
- `uv` package manager installed
- VS Code extensions loaded
- Port 8000 forwarded (for OAuth callback)
- All project dependencies installed on startup

---

## Installation Steps

### 1. Install Python 3.9+

```bash
# macOS with Homebrew
brew install python@3.11

# Verify installation
python --version  # Should be 3.9+
```

### 2. Install uv Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 3. Install Dependencies

```bash
# Navigate to project root
cd magic-umbrella

# Install core dependencies
uv sync

# Install development dependencies
uv sync --extra dev

# Verify installation
uv pip list
```

---

## Environment Variables

### Required Variables (.env)

```bash
# Azure App Registration
AZURE_CLIENT_ID=your-client-id-from-task-0.2
AZURE_TENANT_ID=your-tenant-id-from-task-0.2
AZURE_CLIENT_SECRET=your-client-secret-from-task-0.2
AZURE_REDIRECT_URI=http://localhost:8000/callback

# Azure OpenAI (for LLM classification)
AZURE_OPENAI_API_KEY=your-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4o-mini

# Application Settings
LOG_LEVEL=INFO
CONFIG_DIR=./config
```

### Create .env File

```bash
# Copy example
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

---

## Ruff Configuration

### pyproject.toml Configuration

```toml
[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Run Ruff

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

---

## pytest Configuration

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--color=yes",
    "--strict-markers",
]
markers = [
    "integration: Integration tests requiring external services",
    "unit: Unit tests that don't require external services",
]
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=magic_umbrella

# Run unit tests only
uv run pytest -m unit

# Run specific test file
uv run pytest tests/test_auth.py
```

---

## Optional: VS Code Configuration

### .vscode/settings.json

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.linting.enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

---

## Dependency Reference

### Core Dependencies

```
msgraph-sdk>=1.0.0         # Microsoft Graph API client
azure-identity>=1.15.0     # Azure authentication
msal>=1.26.0               # Microsoft Authentication Library
openai>=1.10.0             # Azure OpenAI client
pandas>=2.0.0              # Data analysis
python-dateutil>=2.8.0     # Date/time handling
pytz>=2024.1               # Timezone support
pydantic>=2.0.0            # Data validation
pydantic-settings>=2.0.0   # Settings management
python-dotenv>=1.0.0       # Environment variables
typer>=0.9.0               # CLI framework
rich>=13.0.0               # Terminal formatting
pyyaml>=6.0.0              # YAML parsing
```

### Dev Dependencies

```
pytest>=8.0.0              # Testing framework
pytest-asyncio>=0.23.0     # Async test support
pytest-cov>=4.1.0          # Coverage reporting
ruff>=0.2.0                # Linting & formatting
```

### Optional: NLP Dependencies

```
fuzzywuzzy>=0.18.0         # Fuzzy string matching
python-Levenshtein>=0.25.0 # Fast string comparison
```

---

## Verification Checklist

- [ ] `python --version` shows 3.9+
- [ ] `uv --version` works
- [ ] `uv sync` completes without errors
- [ ] `uv run python -c "import magic_umbrella"` works
- [ ] `uv run pytest` runs (even if no tests yet)
- [ ] `uv run ruff check .` runs
- [ ] `.env` file exists with all required variables
- [ ] `.env` is in `.gitignore`
- [ ] No secrets in code or version control

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 483-527)
- CLAUDE.md: Project conventions and commands

---

## Troubleshooting

### uv sync fails

```bash
# Clear cache
uv cache clean

# Try again
uv sync
```

### Import errors

```bash
# Verify installation
uv pip list | grep magic-umbrella

# Reinstall in editable mode
uv pip install -e .
```

### .env not loaded

```bash
# Verify python-dotenv is installed
uv pip show python-dotenv

# Load in code
from dotenv import load_dotenv
load_dotenv()
```
