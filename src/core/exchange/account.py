"""
Account operations client for Deribit exchange.

Handles account-related operations like balance and trading fees.
"""

from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class AccountClient:
    """
    Client for accessing account-related operations on Deribit.
    
    Provides methods for retrieving account balances, trading fees,
    and other account information through WebSocket API.
    """
    
    def __init__(self, exchange_client):
        """Initialize account client"""
        self.exchange = exchange_client
        self.currency = exchange_client.currency
        
    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance information"""
        try:
            result = await self.exchange.request(
                'private/get_account_summary',
                {
                    'currency': self.currency,
                    'extended': True
                },
                auth=True
            )
            
            return {
                'total_balance': float(result['equity']),
                'available_balance': float(result['available_funds']),
                'margin_balance': float(result['margin_balance']),
                'unrealized_pnl': float(result['total_pl']),
                'currency': self.currency
            }
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            raise
            
    async def get_trading_fees(self) -> Dict[str, float]:
        """Get trading fee rates"""
        try:
            result = await self.exchange.request(
                'private/get_account_summary',
                {
                    'currency': self.currency,
                    'extended': True
                },
                auth=True
            )
            
            return {
                'maker_fee': float(result['maker_fee']),
                'taker_fee': float(result['taker_fee'])
            }
        except Exception as e:
            logger.error(f"Error getting trading fees: {e}")
            raise 