"""
Gate.io exchange client module for handling basic market operations.

Provides interface for market data retrieval and basic exchange operations.

Example:
    client = ExchangeClient()
    price = await client.get_current_price()
"""

from typing import Dict, List, Optional
from decimal import Decimal
import gate_api
from gate_api.exceptions import GateApiException
from gate_api import ApiClient, SpotApi, Configuration

from config_local import EXCHANGE_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

class ExchangeClient:
    """
    Gate.io exchange client for market operations.
    
    Handles connection to Gate.io API and provides methods for
    market data retrieval and basic exchange operations.
    
    Example:
        client = ExchangeClient()
        price = await client.get_current_price()
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
        
        env = "TESTNET" if EXCHANGE_CONFIG['use_testnet'] else "PRODUCTION"
        logger.info(f"Initializing Gate.io client in {env} environment")
        
    async def get_current_price(self) -> Optional[float]:
        """
        Get current price for configured trading pair.
        
        Returns:
            Current price as float or None if error occurs
            
        Example:
            price = await client.get_current_price()
            if price:
                print(f"Current BTC price: {price}")
        """
        try:
            ticker = self.spot_api.list_tickers(currency_pair=self.trading_pair)
            price = float(ticker[0].last)
            logger.info(f"Current price for {self.trading_pair}: {price}")
            return price
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_current_price: {e}")
            return None
            
    async def get_orderbook(self, depth: int = 10) -> Optional[Dict]:
        """
        Get order book data for configured trading pair.
        
        Args:
            depth: Number of price levels to retrieve
            
        Returns:
            Dictionary containing bids and asks or None if error occurs
            
        Example:
            orderbook = await client.get_orderbook(depth=5)
            if orderbook:
                print(f"Top bid: {orderbook['bids'][0]}")
        """
        try:
            orderbook = self.spot_api.list_order_book(
                currency_pair=self.trading_pair,
                limit=depth
            )
            return {
                'bids': [[float(p), float(v)] for p, v in orderbook['bids']],
                'asks': [[float(p), float(v)] for p, v in orderbook['asks']]
            }
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_orderbook: {e}")
            return None
            
    async def get_historical_data(
        self,
        interval: str = '1h',
        limit: int = 100
    ) -> Optional[List[Dict]]:
        """
        Get historical candlestick data.
        
        Args:
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 4h, 1d)
            limit: Number of candles to retrieve
            
        Returns:
            List of candlestick data or None if error occurs
            
        Example:
            candles = await client.get_historical_data('1h', 24)
            if candles:
                print(f"24h price range: {candles[0]['low']} - {candles[0]['high']}")
        """
        try:
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
            
            return [{
                'timestamp': candle[0],
                'volume': float(candle[1]),
                'close': float(candle[2]),
                'high': float(candle[3]),
                'low': float(candle[4]),
                'open': float(candle[5])
            } for candle in candlesticks]
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_historical_data: {e}")
            return None
            
    async def get_trading_fees(self) -> Optional[Dict]:
        """
        Get trading fee rates for the configured pair.
        
        Returns:
            Dictionary containing maker and taker fees or None if error occurs
            
        Example:
            fees = await client.get_trading_fees()
            if fees:
                print(f"Maker fee: {fees['maker_fee']}%")
        """
        try:
            fee_info = self.spot_api.get_fee(currency_pair=self.trading_pair)
            return {
                'maker_fee': float(fee_info.maker_fee),
                'taker_fee': float(fee_info.taker_fee)
            }
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_trading_fees: {e}")
            return None 