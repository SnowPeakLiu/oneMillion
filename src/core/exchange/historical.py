"""
Historical data operations for Gate.io exchange.

Handles retrieval of historical market data like candlesticks.
"""

from typing import Dict, List, Optional
from gate_api.exceptions import GateApiException
from utils.logger import get_logger

logger = get_logger(__name__)

class HistoricalDataClient:
    """
    Handles historical data operations for Gate.io exchange.
    
    Args:
        spot_api: Gate.io spot API instance
        trading_pair: Trading pair to use
        
    Example:
        client = HistoricalDataClient(spot_api, "BTC_USDT")
        candles = await client.get_historical_data('1h', 24)
    """
    
    def __init__(self, spot_api, trading_pair: str):
        self.spot_api = spot_api
        self.trading_pair = trading_pair
        self.interval_map = {
            '1m': '60',
            '5m': '300',
            '15m': '900',
            '30m': '1800',
            '1h': '3600',
            '4h': '14400',
            '1d': '86400'
        }
        
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
        """
        try:
            candlesticks = self.spot_api.list_candlesticks(
                currency_pair=self.trading_pair,
                interval=self.interval_map.get(interval, '3600'),
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