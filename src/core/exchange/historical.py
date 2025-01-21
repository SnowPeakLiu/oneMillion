"""
Historical data client for Deribit exchange.

Handles retrieval of historical market data like candlesticks.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)

class HistoricalDataClient:
    """
    Client for accessing historical market data from Deribit.
    
    Provides methods for retrieving historical candlestick data
    through WebSocket API.
    """
    
    VALID_INTERVALS = {
        '1m': 1,
        '3m': 3,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1h': 60,
        '2h': 120,
        '4h': 240,
        '6h': 360,
        '12h': 720,
        '1d': 1440
    }
    
    def __init__(self, exchange_client):
        """Initialize historical data client"""
        self.exchange = exchange_client
        self.instrument_name = exchange_client.instrument_name
        
    async def get_historical_data(self, interval: str = '1h', start_time: int = None, end_time: int = None) -> List[Dict[str, Any]]:
        """
        Get historical candlestick data.
        
        Args:
            interval: Time interval (e.g. '1h', '1d')
            start_time: Start timestamp in milliseconds
            end_time: End timestamp in milliseconds
            
        Returns:
            List of candlestick data
        """
        if interval not in self.VALID_INTERVALS:
            raise ValueError(f"Invalid interval. Must be one of {list(self.VALID_INTERVALS.keys())}")
            
        try:
            # If no time range specified, get last 24 hours
            if not start_time:
                end_time = int(datetime.now().timestamp() * 1000)
                start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours
                
            result = await self.exchange.request(
                'public/get_tradingview_chart_data',
                {
                    'instrument_name': self.instrument_name,
                    'start_timestamp': start_time,
                    'end_timestamp': end_time,
                    'resolution': str(self.VALID_INTERVALS[interval])
                }
            )
            
            return result['ticks']
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            raise 