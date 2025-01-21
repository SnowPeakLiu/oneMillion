# Configuration settings
EXCHANGE_CONFIG = {
    'api_key': '',  # DO NOT PUT REAL API KEYS HERE
    'api_secret': '',  # DO NOT PUT REAL API SECRETS HERE
    'instrument_name': 'BTC-PERPETUAL',  # Deribit uses BTC-PERPETUAL format
    'currency': 'BTC',  # Base currency
    'timeframe': '1h'
}

# Trading parameters
TRADING_CONFIG = {
    'initial_balance': 1,  # BTC
    'position_size': 0.1,  # 10% of balance per trade
    'stop_loss': 0.02,    # 2% stop loss
    'take_profit': 0.04,  # 4% take profit
    'leverage': 10,       # Default leverage
    'post_only': True,    # Default to post-only orders
    'reduce_only': False  # Default for reduce-only orders
} 