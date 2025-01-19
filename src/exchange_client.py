from gate_api import ApiClient, SpotApi, Configuration
from gate_api.exceptions import GateApiException
from config import EXCHANGE_CONFIG

class ExchangeClient:
    def __init__(self):
        # Create authentication configuration
        config = Configuration(
            key=EXCHANGE_CONFIG['api_key'],
            secret=EXCHANGE_CONFIG['api_secret']
        )
        
        # Initialize API client
        self.client = ApiClient(config)
        self.spot_api = SpotApi(self.client)
        self.trading_pair = EXCHANGE_CONFIG['trading_pair']
    
    def get_current_price(self):
        """Get current price for trading pair"""
        try:
            ticker = self.spot_api.list_tickers(currency_pair=self.trading_pair)
            return float(ticker[0].last)
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return None
    
    def get_historical_data(self, interval='1h', limit=100):
        """Get historical kline/candlestick data"""
        try:
            # Convert timeframe to seconds
            interval_map = {
                '1m': '60',
                '5m': '300',
                '15m': '900',
                '30m': '1800',
                '1h': '3600',
                '4h': '14400',
                '1d': '86400'
            }
            
            candlesticks = self.spot_api.list_candlesticks(
                currency_pair=self.trading_pair,
                interval=interval_map.get(interval, '3600'),
                limit=limit
            )
            return candlesticks
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return None 