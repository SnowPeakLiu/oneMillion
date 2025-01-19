# Setup Guide

## Prerequisites
- Python 3.8+
- Gate.io account with API access

## Installation Steps
1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install gate-api
   pip install pandas numpy
   ```

3. **Configure API Keys**
   - Create API keys on Gate.io:
     1. Log in to your Gate.io account
     2. Go to API Keys section
     3. Create new API key with trading permissions
     4. Save your API key and secret safely
   - Copy `src/config.py`
   - Replace placeholder API credentials with your own

## Security Considerations
- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement IP restrictions on Gate.io API keys
- Enable 2FA on your Gate.io account
- Set appropriate API key permissions (only enable what you need)

## Development Setup
1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd crypto-trading-bot
   ```

2. **Setup Pre-commit Hooks** (Recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Testing
- Unit tests implementation pending
- Integration tests implementation pending 