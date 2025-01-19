"""
Main Gate.io exchange client.

Integrates market data, historical data, and account operations.
"""

import gate_api
from gate_api import ApiClient, SpotApi, Configuration

from config_local import EXCHANGE_CONFIG
from utils.logger import get_logger
from .market_data import MarketDataClient
from .historical import HistoricalDataClient
from .account import AccountClient

logger = get_logger(__name__)

class ExchangeClient:
    """
    Main Gate.io exchange client integrating all operations.
    
    Provides access to market data, historical data, and account operations
    through specialized client instances.
    
    Example:
        client = ExchangeClient()
        price = await client.market.get_current_price()
        candles = await client.historical.get_historical_data('1h')
        fees = await client.account.get_trading_fees()
    """
    
    def __init__(self):
        """Initialize Gate.io API client with configuration"""
        self.config = Configuration(
            key=EXCHANGE_CONFIG['api_key'],
            secret=EXCHANGE_CONFIG['api_secret'],
            host=EXCHANGE_CONFIG['test_base_url'] if EXCHANGE_CONFIG['use_testnet'] 
                else EXCHANGE_CONFIG['base_url']
        )
        
        self.client = ApiClient(self.config)
        self.spot_api = SpotApi(self.client)
        self.trading_pair = EXCHANGE_CONFIG['trading_pair']
        
        # Initialize specialized clients
        self.market = MarketDataClient(self.spot_api, self.trading_pair)
        self.historical = HistoricalDataClient(self.spot_api, self.trading_pair)
        self.account = AccountClient(self.spot_api, self.trading_pair)
        
        env = "TESTNET" if EXCHANGE_CONFIG['use_testnet'] else "PRODUCTION"
        logger.info(f"Initializing Gate.io client in {env} environment") 