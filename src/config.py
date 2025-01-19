# Configuration settings
EXCHANGE_CONFIG = {
    'api_key': '',  # DO NOT PUT REAL API KEYS HERE
    'api_secret': '',  # DO NOT PUT REAL API SECRETS HERE
    'trading_pair': 'BTC_USDT',  # Gate.io uses underscore instead of slash
    'timeframe': '1h'
}

# Trading parameters
TRADING_CONFIG = {
    'initial_balance': 1000,  # USDT
    'position_size': 0.1,     # 10% of balance per trade
    'stop_loss': 0.02,        # 2% stop loss
    'take_profit': 0.04       # 4% take profit
} 