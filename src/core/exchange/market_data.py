"""
Market data client for Deribit exchange.

Handles real-time market data operations like current price and order book.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class OrderBook:
    """Order book data structure"""
    bids: List[Tuple[float, float]]  # price, size
    asks: List[Tuple[float, float]]  # price, size
    timestamp: int

class MarketDataClient:
    """
    Client for accessing real-time market data from Deribit.
    
    Provides methods for retrieving current price and order book data
    through WebSocket API.
    """
    
    def __init__(self, exchange_client):
        """Initialize market data client"""
        self.exchange = exchange_client
        self.instrument_name = exchange_client.instrument_name
        
    async def get_current_price(self) -> float:
        """Get current market price for the instrument"""
        try:
            result = await self.exchange.request(
                'public/ticker',
                {'instrument_name': self.instrument_name}
            )
            return float(result['last_price'])
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            raise
            
    async def get_orderbook(self, depth: int = 10) -> OrderBook:
        """Get current order book for the instrument"""
        try:
            result = await self.exchange.request(
                'public/get_order_book',
                {
                    'instrument_name': self.instrument_name,
                    'depth': depth
                }
            )
            
            return OrderBook(
                bids=[(float(price), float(size)) for price, size in result['bids']],
                asks=[(float(price), float(size)) for price, size in result['asks']],
                timestamp=result['timestamp']
            )
        except Exception as e:
            logger.error(f"Error getting order book: {e}")
            raise 