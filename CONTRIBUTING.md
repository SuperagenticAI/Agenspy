# Contributing to Agenspy

👍 First off, thanks for taking the time to contribute! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [CLI Development](#cli-development)

## Code of Conduct

This project and everyone participating in it are governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/superagenticai/agenspy.git
   cd agenspy
   ```

3. **Set up your development environment**:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode with dev dependencies
   pip install -e ".[dev]"

   # Install pre-commit hooks
   pip install pre-commit
   pre-commit install
   ```

4. **Verify your setup**:
   ```bash
   agenspy --help
   ```

## Development Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run checks before committing**:
   ```bash
   # Format code
   black .

   # Lint code
   ruff check .

   # Type checking
   mypy .

   # Run tests
   pytest
   ```

4. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve issue with protocol handling"
   ```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation in the `docs/` directory
3. Add tests for any new functionality
4. Ensure all tests pass
5. Update CHANGELOG.md following the Keep a Changelog format
6. Submit a pull request to the main repository

## Coding Standards

We maintain high code quality using these tools:

- **Code Formatting**: [Black](https://black.readthedocs.io/)
  ```bash
  black .
  ```

- **Linting**: [Ruff](https://github.com/charliermarsh/ruff)
  ```bash
  ruff check .
  ```

- **Type Checking**: [MyPy](http://mypy-lang.org/)
  ```bash
  mypy .
  ```

Additional guidelines:
- Follow PEP 8 style guide
- Maximum line length is 120 characters
- Use type hints for all function arguments and return values
- Write docstrings for all public methods and classes
- Keep functions focused and concise

## Testing Guidelines

- Write unit tests for all new features
- Tests should be placed in the `tests/` directory
- Use `pytest` for testing
- Maintain test coverage above 80%
- Use pytest fixtures for reusable test components
- Name tests descriptively following `test_<what>_<expected>` pattern

## CLI Development

Agenspy includes a CLI tool called `agenspy`. When making changes to the CLI:

- Keep commands and options consistent with existing patterns
- Add comprehensive help text for all commands
- Update the CLI documentation in `docs/cli.md`
- Test CLI commands thoroughly

## Documentation

- Update docstrings for any new/modified code
- Follow Google style docstrings
- Include code examples in docstrings
- Update the `docs/` directory for any new features
- Add examples to the `examples/` directory if applicable

Example docstring:
```python
def process_agent(self, input_data: Dict[str, Any]) -> AgentResponse:
    """Process input data through the agent pipeline.

    Args:
        input_data: Dictionary containing input data for processing

    Returns:
        AgentResponse: The processed agent response

    Example:
        >>> agent = Agent()
        >>> response = agent.process_agent({"query": "Hello"})
        >>> print(response.text)
    """
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a new release on GitHub
4. GitHub Actions will automatically publish to PyPI

## Getting Help

- Open an issue for bugs or feature requests
- Check our [documentation](https://agenspy.readthedocs.io)
- Join our community discussions

## License

By contributing to Agenspy, you agree that your contributions will be licensed under the MIT License.
