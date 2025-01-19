"""
Market data operations for Gate.io exchange.

Handles real-time market data retrieval like prices and orderbook.
"""

from typing import Dict, Optional
from gate_api.exceptions import GateApiException
from utils.logger import get_logger

logger = get_logger(__name__)

class MarketDataClient:
    """
    Handles market data operations for Gate.io exchange.
    
    Args:
        spot_api: Gate.io spot API instance
        trading_pair: Trading pair to use
        
    Example:
        client = MarketDataClient(spot_api, "BTC_USDT")
        price = await client.get_current_price()
    """
    
    def __init__(self, spot_api, trading_pair: str):
        self.spot_api = spot_api
        self.trading_pair = trading_pair
        
    async def get_current_price(self) -> Optional[float]:
        """
        Get current price for configured trading pair.
        
        Returns:
            Current price as float or None if error occurs
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