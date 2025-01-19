# Configuration settings
EXCHANGE_CONFIG = {
    'api_key': 'your_gate_io_api_key',
    'api_secret': 'your_gate_io_api_secret',
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