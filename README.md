# magic-umbrella

A Python project.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies

```bash
uv sync
```

Or with development dependencies:

```bash
uv sync --extra dev
```

## Development

### Run tests

```bash
uv run pytest
```

### Linting and formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

Check code:
```bash
uv run ruff check .
```

Format code:
```bash
uv run ruff format .
```

Fix issues automatically:
```bash
uv run ruff check --fix .
```

## Usage

```python
from magic_umbrella import example

example.hello()
```
