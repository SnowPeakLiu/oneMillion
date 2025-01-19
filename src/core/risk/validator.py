"""
Risk management module for trading operations.

Provides risk validation and position sizing functionality.

Example:
    validator = RiskValidator(exchange_client)
    if await validator.validate_order('buy', Decimal('0.1'), Decimal('50000')):
        # Place order
"""

from typing import Dict, Optional
from decimal import Decimal
import time

from config_local import RISK_CONFIG, EXCHANGE_CONFIG
from core.exchange.client import ExchangeClient
from utils.logger import get_logger

logger = get_logger(__name__)

class RiskValidator:
    """
    Validates trading operations against risk management rules.
    
    Handles position sizing, risk limits, and trading constraints.
    
    Args:
        exchange: ExchangeClient instance for market data
        
    Example:
        validator = RiskValidator(exchange_client)
        is_valid = await validator.validate_order('buy', Decimal('0.1'))
    """
    
    def __init__(self, exchange: ExchangeClient):
        self.exchange = exchange
        self.daily_trades = []
        
    def _check_testnet_limits(self, quantity: Decimal, price: Optional[Decimal] = None) -> bool:
        """
        Additional safety checks for testnet environment.
        
        Args:
            quantity: Order quantity
            price: Optional order price
            
        Returns:
            True if within testnet limits, False otherwise
        """
        if not EXCHANGE_CONFIG['use_testnet']:
            return True
            
        try:
            # Check order size
            if price:
                order_value = quantity * price
                if order_value > Decimal('1000'):
                    logger.warning(f"Order value {order_value} exceeds testnet limit")
                    return False
                    
            # Check daily trade count
            current_time = time.time()
            self.daily_trades = [t for t in self.daily_trades if current_time - t < 86400]
            
            if len(self.daily_trades) >= RISK_CONFIG['max_daily_trades']:
                logger.warning("Daily trade limit reached")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error in testnet validation: {e}")
            return False
            
    async def validate_order(
        self,
        side: str,
        quantity: Decimal,
        price: Optional[Decimal] = None
    ) -> bool:
        """
        Validate order against risk management rules.
        
        Args:
            side: Order side ('buy' or 'sell')
            quantity: Order quantity
            price: Optional limit price
            
        Returns:
            True if order passes all risk checks, False otherwise
            
        Example:
            if await validator.validate_order('buy', Decimal('0.1'), Decimal('50000')):
                print("Order passes risk checks")
        """
        try:
            # Testnet validation
            if not self._check_testnet_limits(quantity, price):
                return False
                
            # Get current balance
            balance = await self.exchange.get_balance()
            if not balance:
                logger.error("Failed to retrieve balance")
                return False
                
            # Check balance
            if side.lower() == 'buy':
                required_balance = quantity * (price or Decimal('0'))
                if balance.get('USDT', Decimal('0')) < required_balance:
                    logger.warning(f"Insufficient USDT balance for buy order")
                    return False
            else:
                base_currency = self.exchange.trading_pair.split('_')[0]
                if balance.get(base_currency, Decimal('0')) < quantity:
                    logger.warning(f"Insufficient {base_currency} balance for sell order")
                    return False
                    
            # Check position size
            total_balance = self._calculate_total_balance(balance, price)
            position_value = quantity * (price or Decimal('0'))
            max_position = Decimal(str(RISK_CONFIG['max_position_size'])) * total_balance
            
            if position_value > max_position:
                logger.warning(
                    f"Position size {position_value} exceeds limit of {max_position}"
                )
                return False
                
            # Record trade attempt for daily limit
            if EXCHANGE_CONFIG['use_testnet']:
                self.daily_trades.append(time.time())
                
            return True
            
        except Exception as e:
            logger.error(f"Error in order validation: {e}")
            return False
            
    def _calculate_total_balance(
        self,
        balance: Dict[str, Decimal],
        current_price: Optional[Decimal]
    ) -> Decimal:
        """
        Calculate total balance in USDT.
        
        Args:
            balance: Balance dictionary from exchange
            current_price: Current price for conversion
            
        Returns:
            Total balance in USDT
        """
        try:
            total = Decimal('0')
            for currency, amount in balance.items():
                if currency == 'USDT':
                    total += amount
                elif current_price and currency == self.exchange.trading_pair.split('_')[0]:
                    total += amount * current_price
            return total
        except Exception as e:
            logger.error(f"Error calculating total balance: {e}")
            return Decimal('0') 