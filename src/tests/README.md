# StandardWeb3 Test Suite

This directory contains comprehensive tests for the StandardWeb3 Python client library.

## Test Structure

- `test_setup.py` - Client initialization and configuration tests
- `test_contract.py` - Contract function and trading operation tests
- `test_api.py` - API endpoint and data fetching tests
- `test_websocket.py` - WebSocket connection and real-time data tests
- `conftest.py` - Shared fixtures and test configuration

## Running Tests

### Prerequisites

Make sure you have the development dependencies installed:

```bash
pip install -e .[dev]
```

### Basic Test Execution

Run all tests:
```bash
pytest src/tests/
```

Run specific test file:
```bash
pytest src/tests/test_setup.py
```

Run with verbose output:
```bash
pytest -v src/tests/
```

### Test Categories

The tests are organized with markers for different categories:

- **Unit tests** (default): Fast, isolated tests with mocked dependencies
- **Integration tests**: Tests that require actual network connections
- **Slow tests**: Tests that may take longer to execute

Run only unit tests:
```bash
pytest -m "not integration and not slow" src/tests/
```

Run integration tests (requires network and environment setup):
```bash
pytest --run-integration src/tests/
```

Run slow tests:
```bash
pytest --run-slow src/tests/
```

### Environment Configuration

For tests that require actual blockchain connections (integration tests), create a `.env.test` file in the project root:

```bash
# Copy the example and fill in your values
cp .env.example .env.test
```

Required environment variables for integration tests:
```env
PRIVATE_KEY=0x... # Test private key (use test account only!)
RPC_URL=https://... # RPC endpoint URL
ADDRESS=0x... # Test account address
API_KEY=... # API key (if required)
```

### Test Coverage

Generate test coverage report:
```bash
pytest --cov=standardweb3 --cov-report=html src/tests/
```

View coverage report:
```bash
open htmlcov/index.html
```

## Test Features

### Mocking Strategy

- **Contract functions**: Mocked to avoid actual blockchain transactions during unit tests
- **API calls**: Mocked with realistic response data
- **WebSocket connections**: Mocked to test connection logic without actual network calls

### Fixtures

The `conftest.py` file provides shared fixtures:

- `test_config`: Common test configuration constants
- `basic_client`: Basic mocked StandardClient
- `full_client`: Fully mocked client with all components
- `mock_*_data`: Pre-built mock data objects for different API responses

### Parameterized Tests

Many tests use pytest's parametrize feature to test multiple scenarios:

- Different network configurations
- Various trading parameters
- Multiple API endpoints with similar patterns

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<Module>Functions`
- Test methods: `test_<specific_functionality>`

### Example Test Structure

```python
class TestNewFeature:
    """Test cases for new feature."""

    @pytest.mark.asyncio
    async def test_new_async_function(self, mock_client):
        """Test description."""
        # Arrange
        mock_client.api.new_function.return_value = expected_result

        # Act
        result = await mock_client.new_function(param1, param2)

        # Assert
        assert result == expected_result
        mock_client.api.new_function.assert_called_once_with(param1, param2)
```

### Adding Integration Tests

Mark integration tests that require network access:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_call(self, environment_variables):
    """Integration test with real API."""
    if not environment_variables["private_key"]:
        pytest.skip("Integration test requires PRIVATE_KEY")

    # Your integration test code here
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure dev dependencies are installed
2. **Environment variable errors**: Check that `.env.test` is properly configured
3. **Network timeout errors**: Increase timeout for slow networks or skip network tests

### Debug Mode

Run tests with debugging enabled:
```bash
pytest -s --tb=long src/tests/
```

### Specific Test Selection

Run tests matching a pattern:
```bash
pytest -k "test_market_buy" src/tests/
```

Run tests for specific functionality:
```bash
pytest -k "contract" src/tests/  # All contract-related tests
pytest -k "api" src/tests/       # All API-related tests
```

## Contributing

When adding new functionality to StandardWeb3:

1. Add corresponding unit tests with mocked dependencies
2. Add integration tests if the feature requires network interaction
3. Update test fixtures in `conftest.py` if needed
4. Follow the existing test patterns and naming conventions
5. Ensure all tests pass before submitting changes

## Test Philosophy

- **Fast feedback**: Unit tests should run quickly with mocked dependencies
- **Comprehensive coverage**: Test both success and error scenarios
- **Realistic mocking**: Mock data should reflect actual API responses
- **Isolation**: Tests should not depend on external state or each other
- **Clear assertions**: Test failures should clearly indicate what went wrong
