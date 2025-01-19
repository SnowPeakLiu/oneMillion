# Coding Standards

## File Organization
- Maximum file length: 200 lines
- If a file exceeds 200 lines, split it into logical modules
- Keep one class per file (with rare exceptions for closely related helper classes)

## Code Structure
### File Sections
1. Imports
2. Type definitions/constants
3. Class/function definitions
4. Main logic (if applicable)

### Module Organization
```
src/
├── core/           # Core components (max 200 lines each)
│   ├── exchange.py     # Base exchange operations
│   ├── orders.py       # Order management
│   ├── risk.py         # Risk management
│   └── monitor.py      # System monitoring
├── strategies/     # Trading strategies
│   ├── base.py        # Strategy interface
│   ├── momentum.py    # Momentum strategies
│   └── mean_rev.py    # Mean reversion strategies
└── utils/         # Utilities
    ├── logger.py      # Logging configuration
    ├── validation.py  # Input validation
    └── config.py      # Configuration management
```

## Coding Style
### Python Standards
- Follow PEP 8 guidelines
- Use type hints for all function parameters and returns
- Maximum line length: 88 characters (Black formatter standard)
- Use docstrings for all public methods

### Naming Conventions
```python
# Classes: PascalCase
class TradingStrategy:

# Functions/Methods: snake_case
def calculate_position_size():

# Variables: snake_case
current_price = 0.0

# Constants: UPPER_CASE
MAX_POSITION_SIZE = 0.1

# Private methods/variables: _leading_underscore
def _validate_input():
_cache = {}
```

## Documentation
### Required Documentation
- Module-level docstring explaining purpose
- Class-level docstring with usage example
- Function docstrings with:
  - Parameters
  - Return values
  - Exceptions raised
  - Usage example for complex functions

### Example
```python
"""
Order management module for handling trading operations.

Example:
    order_manager = OrderManager(exchange_client)
    await order_manager.place_order(side='buy', quantity=0.1)
"""

class OrderManager:
    """
    Manages order creation, validation, and tracking.
    
    Args:
        exchange_client: ExchangeClient instance
        
    Example:
        manager = OrderManager(client)
        await manager.place_order(side='buy', quantity=0.1)
    """
```

## Error Handling
- Use specific exception types
- Always log exceptions with context
- Handle errors at appropriate levels
- Include error recovery strategies

## Testing
### Test File Organization
- Tests parallel source file structure
- One test file per source file
- Test file names: `test_<source_file>.py`

### Required Tests
- Unit tests for all public methods
- Integration tests for key workflows
- Edge case testing for critical functions
- Performance tests for time-critical operations

## Logging
### Log Levels
- DEBUG: Detailed debugging information
- INFO: General operational events
- WARNING: Unexpected but handled events
- ERROR: Serious issues requiring attention
- CRITICAL: System-breaking issues

### Log Format
```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

## Version Control
### Commit Messages
Format: `<type>(<scope>): <description>`

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code restructuring
- docs: Documentation
- test: Test addition/modification
- chore: Maintenance tasks

Example:
```
feat(orders): Add limit order functionality
fix(risk): Correct position size calculation
docs(api): Update trading endpoints
```

### Branch Naming
- feature/: New features
- fix/: Bug fixes
- refactor/: Code restructuring
- docs/: Documentation updates

Example:
```
feature/limit-orders
fix/position-calculation
docs/api-documentation
```

## Code Review
### Review Checklist
1. Follows 200-line limit
2. Proper error handling
3. Complete documentation
4. Test coverage
5. Type hints present
6. No security vulnerabilities
7. Performance considerations
8. Logging appropriately used

## Security
- No API keys in code
- Use environment variables
- Validate all inputs
- Rate limit API calls
- Log security events 