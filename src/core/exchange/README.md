# Gate.io Exchange Integration

This module provides a comprehensive interface to the Gate.io exchange API, with specialized clients for different types of operations.

## Architecture

The module is organized into specialized clients:

- `ExchangeClient`: Main client that integrates all operations
- `MarketDataClient`: Real-time market data operations
- `HistoricalDataClient`: Historical data retrieval
- `AccountClient`: Account-related operations

### File Structure

```
exchange/
├── __init__.py
├── client.py        # Main ExchangeClient
├── market_data.py   # Market data operations
├── historical.py    # Historical data operations
├── account.py       # Account operations
└── README.md
```

## Usage

### Basic Setup

```python
from core.exchange.client import ExchangeClient

# Initialize the client
client = ExchangeClient()
```

### Market Data Operations

```python
# Get current price
price = await client.market.get_current_price()

# Get orderbook
orderbook = await client.market.get_orderbook(depth=10)
```

### Historical Data Operations

```python
# Get hourly candles
candles = await client.historical.get_historical_data('1h', limit=24)

# Available intervals: 1m, 5m, 15m, 30m, 1h, 4h, 1d
```

### Account Operations

```python
# Get trading fees
fees = await client.account.get_trading_fees()
```

## Configuration

Configuration is managed through `config_local.py`:

```python
EXCHANGE_CONFIG = {
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret',
    'use_testnet': True,  # Set to False for production
    'trading_pair': 'BTC_USDT'
}
```

## Error Handling

All API calls are wrapped with proper error handling:

- API errors are caught and logged
- Methods return `None` on error
- Detailed error messages are logged using the logger utility

## Testing

Each component has its own test suite:

```bash
# Run all tests
pytest tests/core/exchange/

# Run specific test files
pytest tests/core/exchange/test_client.py
pytest tests/core/exchange/test_market_data.py
pytest tests/core/exchange/test_historical.py
pytest tests/core/exchange/test_account.py
```

## Best Practices

1. Always check for `None` return values indicating errors
2. Use testnet for development and testing
3. Handle rate limits appropriately
4. Log all important operations and errors
5. Keep files under 200 lines following code standards 