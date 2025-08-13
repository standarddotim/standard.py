# Install dependencies
uv sync --dev

# Run all tests
uv run pytest src/tests/

# Run specific test categories
uv run pytest src/tests/ -m "not integration"  # Unit tests only
uv run pytest src/tests/ --run-integration     # Include integration tests
uv run pytest src/tests/ -v                    # Verbose output

# Run specific test files
uv run pytest src/tests/test_setup.py -v
uv run pytest src/tests/test_contract.py -v
