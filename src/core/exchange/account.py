"""
Account operations for Gate.io exchange.

Handles account-related operations like fees and balances.
"""

from typing import Dict, Optional
from gate_api.exceptions import GateApiException
from utils.logger import get_logger

logger = get_logger(__name__)

class AccountClient:
    """
    Handles account operations for Gate.io exchange.
    
    Args:
        spot_api: Gate.io spot API instance
        trading_pair: Trading pair to use
        
    Example:
        client = AccountClient(spot_api, "BTC_USDT")
        fees = await client.get_trading_fees()
    """
    
    def __init__(self, spot_api, trading_pair: str):
        self.spot_api = spot_api
        self.trading_pair = trading_pair
        
    async def get_trading_fees(self) -> Optional[Dict]:
        """
        Get trading fee rates for the configured pair.
        
        Returns:
            Dictionary containing maker and taker fees or None if error occurs
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