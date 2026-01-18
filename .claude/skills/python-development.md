---
name: python-development
description: Modern Python development with uv, pyproject.toml, type hints, pytest, and async patterns
user-invocable: true
---

# Python Development

Use this skill when building Python applications, libraries, or scripts with modern tooling (uv, pyproject.toml), type hints, and testing.

## Project Setup with uv

### 1. Initialize New Project

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init my-project
cd my-project

# Or with specific Python version
uv init my-project --python 3.12
```

### 2. Project Structure

```
my-project/
├── pyproject.toml        # Project configuration
├── uv.lock               # Lock file (commit this)
├── src/
│   └── my_project/       # Source package
│       ├── __init__.py
│       └── main.py
├── tests/                # Test directory
│   ├── __init__.py
│   ├── conftest.py       # pytest fixtures
│   └── test_main.py
├── .python-version       # Python version
└── README.md
```

### 3. pyproject.toml Configuration

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Your Name", email = "you@example.com" }]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[project.scripts]
my-project = "my_project.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=src/my_project --cov-report=term-missing"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Dependency Management

### Add Dependencies

```bash
# Add production dependency
uv add httpx pydantic

# Add dev dependency
uv add --dev pytest pytest-asyncio ruff mypy

# Add optional dependency group
uv add --optional docs sphinx

# Sync dependencies (install all)
uv sync

# Sync with dev dependencies
uv sync --dev
```

### Pin Dependencies

```bash
# Generate/update lock file
uv lock

# Install from lock file
uv sync --frozen
```

## Type Hints and Pydantic

### Modern Type Hints (Python 3.10+)

```python
from collections.abc import Sequence
from typing import TypeAlias

# Use | instead of Union
def process(value: str | int | None) -> str:
    if value is None:
        return "empty"
    return str(value)

# Use built-in generics
def get_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# TypeAlias for complex types
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# Callable types
from collections.abc import Callable

Handler: TypeAlias = Callable[[str, int], bool]
```

### Pydantic Models (v2)

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()

    model_config = {
        "str_strip_whitespace": True,
        "validate_assignment": True,
    }

# Usage
user = User(id=1, name="Alice", email="Alice@Example.com")
print(user.model_dump())  # {"id": 1, "name": "Alice", "email": "alice@example.com", ...}

# Validation
data = {"id": 1, "name": "Bob", "email": "invalid"}
try:
    User.model_validate(data)
except ValidationError as e:
    print(e.errors())
```

## Async Patterns

### Async/Await with httpx

```python
import asyncio
import httpx

async def fetch_user(client: httpx.AsyncClient, user_id: int) -> dict:
    response = await client.get(f"/users/{user_id}")
    response.raise_for_status()
    return response.json()

async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        tasks = [fetch_user(client, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)

# Run async code
async def main():
    users = await fetch_all_users([1, 2, 3])
    print(users)

if __name__ == "__main__":
    asyncio.run(main())
```

### Async Context Managers

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def database_connection() -> AsyncIterator[Connection]:
    conn = await connect_to_database()
    try:
        yield conn
    finally:
        await conn.close()

async def query_database():
    async with database_connection() as conn:
        result = await conn.execute("SELECT * FROM users")
        return result
```

### Async Generators

```python
from typing import AsyncIterator

async def stream_lines(file_path: str) -> AsyncIterator[str]:
    async with aiofiles.open(file_path) as f:
        async for line in f:
            yield line.strip()

async def process_file(path: str):
    async for line in stream_lines(path):
        print(f"Processing: {line}")
```

## Testing with pytest

### Basic Tests

```python
# tests/test_main.py
import pytest
from my_project.main import calculate, process_data

def test_calculate_addition():
    assert calculate(2, 3) == 5

def test_calculate_with_negative():
    assert calculate(-1, 1) == 0

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, -1, -2),
])
def test_calculate_parametrized(a: int, b: int, expected: int):
    assert calculate(a, b) == expected
```

### Async Tests

```python
import pytest
from my_project.api import fetch_user

@pytest.mark.asyncio
async def test_fetch_user():
    user = await fetch_user(1)
    assert user["id"] == 1
    assert "name" in user

@pytest.mark.asyncio
async def test_fetch_multiple():
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
    )
    assert len(users) == 2
```

### Fixtures

```python
# tests/conftest.py
import pytest
import httpx
from typing import AsyncIterator

@pytest.fixture
def sample_data() -> dict:
    return {"id": 1, "name": "Test User"}

@pytest.fixture
async def async_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client

# Usage in tests
async def test_with_client(async_client: httpx.AsyncClient):
    response = await async_client.get("https://httpbin.org/get")
    assert response.status_code == 200
```

### Mocking

```python
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.mark.asyncio
async def test_with_mock():
    mock_client = AsyncMock()
    mock_client.get.return_value.json.return_value = {"id": 1}

    with patch("my_project.api.httpx.AsyncClient", return_value=mock_client):
        result = await fetch_user(1)
        assert result["id"] == 1

def test_with_patch():
    with patch("my_project.utils.external_api") as mock_api:
        mock_api.return_value = "mocked result"
        result = process_data("input")
        mock_api.assert_called_once_with("input")
```

## Code Quality

### Ruff Linting & Formatting

```bash
# Lint
uv run ruff check .

# Fix lint issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting
uv run ruff format --check .
```

### Type Checking with mypy

```bash
# Run type checker
uv run mypy src/

# With strict mode
uv run mypy src/ --strict
```

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]
```

```bash
# Install pre-commit
uv add --dev pre-commit
uv run pre-commit install
```

## CLI Applications

### With Click

```python
# src/my_project/cli.py
import click

@click.group()
@click.version_option()
def cli():
    """My CLI application."""
    pass

@cli.command()
@click.argument("name")
@click.option("--count", "-c", default=1, help="Number of greetings")
def greet(name: str, count: int):
    """Greet NAME."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def process(verbose: bool):
    """Process data."""
    if verbose:
        click.echo("Processing in verbose mode...")
    click.echo("Done!")

if __name__ == "__main__":
    cli()
```

### Entry Point

```toml
# pyproject.toml
[project.scripts]
my-cli = "my_project.cli:cli"
```

## Error Handling Patterns

### Custom Exceptions

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """Raised when resource is not found."""
    def __init__(self, resource: str, identifier: str | int):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")

# Usage
def get_user(user_id: int) -> User:
    user = database.get(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```

### Result Pattern (Alternative to Exceptions)

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

# Usage
match divide(10, 2):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

## Running the Project

### Development

```bash
# Run main module
uv run python -m my_project

# Run CLI command
uv run my-cli greet World

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Type check
uv run mypy src/
```

### Build & Publish

```bash
# Build package
uv build

# Publish to PyPI
uv publish

# Or with twine
uv run twine upload dist/*
```

## Quick Reference

| Task | Command |
|------|---------|
| Create project | `uv init my-project` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Sync dependencies | `uv sync` |
| Run script | `uv run python script.py` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy src/` |
| Build | `uv build` |
| Publish | `uv publish` |

## Resources

- **uv Documentation**: https://docs.astral.sh/uv/
- **Ruff Documentation**: https://docs.astral.sh/ruff/
- **Pydantic v2**: https://docs.pydantic.dev/latest/
- **pytest**: https://docs.pytest.org/
- **mypy**: https://mypy.readthedocs.io/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
