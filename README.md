# OneMillion Trading Bot

An automated cryptocurrency trading system focusing on BTC-PERPETUAL futures trading using Deribit's WebSocket API.

## Features

- 🤖 Automated trading strategies
- 📊 Real-time market data via WebSocket
- ⚡ Async operations for better performance
- 🛡️ Built-in risk management
- 📈 Technical analysis indicators
- 🔔 Real-time monitoring and alerts
- 💼 Perpetual futures trading
- 🔄 WebSocket-based real-time updates
- 🧪 Comprehensive test suite

## Project Structure

```
oneMillion/
├── src/
│   ├── core/           # Core trading components
│   │   ├── exchange/   # Exchange client and API integration
│   │   ├── orders/     # Order management
│   │   └── position/   # Position tracking
│   ├── strategies/     # Trading strategies
│   ├── data/          # Data management
│   └── utils/         # Utility functions
├── docs/              # Documentation
└── tests/             # Test files
```

## Getting Started

### Prerequisites

- Python 3.8+
- Deribit API account (testnet for development)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd oneMillion
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -e ".[test]"  # Install with test dependencies
```

### Configuration

1. Set up Deribit API credentials:
   - Create an account on [Deribit Testnet](https://test.deribit.com/)
   - Go to Account > API
   - Create new API key with appropriate permissions
   - Copy the client ID and client secret

2. Configure the bot:
   - Update `src/core/config_local.py` with your API credentials:
     ```python
     EXCHANGE_CONFIG = {
         'client_id': 'your_client_id',      # Your Deribit API client ID
         'client_secret': 'your_client_secret', # Your Deribit API client secret
         'instrument_name': 'BTC-PERPETUAL',
         'currency': 'BTC',
         'use_testnet': True  # Use True for testing
     }
     ```

### Testing

Run the test suite to verify your setup:
```bash
python -m pytest -v  # Run all tests
python -m pytest tests/test_exchange_config.py  # Test exchange configuration
```

## Development

See our [Development Guide](docs/development_guide.md) for detailed information about:
- Code organization
- Testing setup
- Git workflow
- Documentation standards

## Project Status

See our [Project Progress](docs/project_progress.md) for:
- Current development phase
- Completed features
- Upcoming tasks
- Technical debt

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Security Notes

- Never commit your API credentials
- Always use testnet for development
- Start with small position sizes
- Monitor your positions regularly
- Use appropriate risk management settings 