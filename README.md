# OneMillion Trading Bot

An automated cryptocurrency trading system focusing on BTC/USDT trading pair using Gate.io API.

## Features

- 🤖 Automated trading strategies
- 📊 Real-time market data analysis
- ⚡ Async operations for better performance
- 🛡️ Built-in risk management
- 📈 Technical analysis indicators
- 🔔 Real-time monitoring and alerts

## Project Structure

```
oneMillion/
├── src/
│   ├── core/           # Core trading components
│   ├── strategies/     # Trading strategies
│   ├── data/          # Data management
│   └── utils/         # Utility functions
├── docs/              # Documentation
└── tests/             # Test files
```

## Getting Started

### Prerequisites

- Python 3.8+
- Gate.io API account

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
# Install development dependencies
pip install -e ".[test]"
# Or just runtime dependencies
pip install -e .
```

4. Configure API credentials
- Copy `src/config.py` to `src/config_local.py`
- Add your Gate.io API credentials to `config_local.py`

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