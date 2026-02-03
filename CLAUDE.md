# Claude Code Instructions

This file contains instructions for Claude Code when working with this project.

## Project Structure

```
magic-umbrella/
├── src/
│   └── magic_umbrella/    # Main package code
├── tests/                  # Test files
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # User-facing documentation
└── CLAUDE.md              # This file - AI assistant instructions
```

## Technology Stack

- **Language**: Python 3.9+
- **Package Manager**: uv (modern, fast Python package manager)
- **Testing**: pytest
- **Linting/Formatting**: Ruff (replaces black, isort, flake8, etc.)
- **Build System**: hatchling

## Development Commands

### Setup
```bash
uv sync --extra dev
```

### Testing
```bash
uv run pytest                    # Run all tests
uv run pytest tests/test_*.py    # Run specific test file
uv run pytest -v                 # Verbose output
uv run pytest -k "test_name"     # Run specific test by name
```

### Code Quality
```bash
uv run ruff check .              # Check for issues
uv run ruff check --fix .        # Auto-fix issues
uv run ruff format .             # Format code
```

## Coding Guidelines

### Style
- Max line length: 100 characters
- Use type hints where beneficial
- Follow PEP 8 conventions
- Ruff handles import sorting and formatting

### Testing
- Write tests for all new functionality
- Test files should match pattern: `test_*.py`
- Test classes should start with `Test*`
- Test functions should start with `test_*`
- Always run tests before marking a task complete

### Code Organization
- Keep modules focused and single-purpose
- Use descriptive variable and function names
- Add docstrings for public functions and classes
- Keep functions small and testable

## Workflow for Changes

1. **Read existing code first** - Always read relevant files before modifying
2. **Run tests** - Verify current state with `uv run pytest`
3. **Make changes** - Implement the requested functionality
4. **Format code** - Run `uv run ruff format .`
5. **Check linting** - Run `uv run ruff check .` and fix any issues
6. **Run tests again** - Ensure `uv run pytest` passes
7. **Verify changes** - Review what was changed

## Common Tasks

### Adding a New Module
1. Create file in `src/magic_umbrella/`
2. Add corresponding test file in `tests/`
3. Update imports if needed
4. Run tests to verify

### Adding Dependencies
1. Add to `dependencies` array in `pyproject.toml`
2. Run `uv sync` to install
3. Document why the dependency is needed

### Adding Dev Dependencies
1. Add to `dev` array under `[project.optional-dependencies]`
2. Run `uv sync --extra dev` to install

## Important Notes

- **Always run tests** before completing a task - failing tests mean the task isn't done
- **Use uv commands** - Don't use pip or other package managers
- **Read before writing** - Never modify code you haven't read
- **Keep it simple** - Avoid over-engineering or adding unnecessary features
- **Format with Ruff** - Don't manually format, let Ruff handle it
- **No placeholders** - Don't use TODO comments or incomplete implementations unless explicitly requested

## Project-Specific Conventions

(Add your specific conventions here as the project grows)

- [ ] Update this section with project-specific patterns
- [ ] Add common code patterns used in this project
- [ ] Document any architectural decisions
- [ ] Note any important gotchas or quirks
