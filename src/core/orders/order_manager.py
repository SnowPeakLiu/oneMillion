"""
Order management module for handling trading operations.

This module provides a comprehensive interface for managing orders including:
- Order placement (market and limit orders)
- Order cancellation
- Order tracking and status updates
- Order validation and risk checks
"""

from typing import Dict, List, Optional, Union
from decimal import Decimal
import asyncio
from datetime import datetime

from utils.logger import get_logger
from core.exchange.client import ExchangeClient
from core.risk.risk_manager import RiskManager

logger = get_logger(__name__)

class OrderManager:
    """
    Manages order creation, validation, tracking and execution.
    
    Handles all order-related operations including placement, cancellation,
    and status tracking. Integrates with risk management for pre-trade checks.
    
    Args:
        exchange_client: ExchangeClient instance for executing orders
        risk_manager: RiskManager instance for pre-trade validation
        
    Example:
        client = ExchangeClient()
        risk_mgr = RiskManager()
        order_mgr = OrderManager(client, risk_mgr)
        
        # Place a market order
        order = await order_mgr.place_market_order(
            side='buy',
            quantity=0.1
        )
    """
    
    def __init__(
        self,
        exchange_client: ExchangeClient,
        risk_manager: RiskManager
    ):
        self.exchange = exchange_client
        self.risk_manager = risk_manager
        self._active_orders: Dict[str, Dict] = {}
        
    async def place_market_order(
        self,
        side: str,
        quantity: Decimal
    ) -> Optional[Dict]:
        """
        Place a market order.
        
        Args:
            side: Order side ('buy' or 'sell')
            quantity: Order quantity in base currency
            
        Returns:
            Order details if successful, None if failed
            
        Raises:
            ValueError: If side or quantity is invalid
        """
        # Validate inputs
        if side not in ['buy', 'sell']:
            raise ValueError(f"Invalid side: {side}")
        if quantity <= 0:
            raise ValueError(f"Invalid quantity: {quantity}")
            
        try:
            # Risk check
            if not await self.risk_manager.validate_order(side, quantity):
                logger.warning(f"Order rejected by risk manager: {side} {quantity}")
                return None
                
            # Place order
            order = await self.exchange.market.place_market_order(
                side=side,
                quantity=quantity
            )
            
            if order:
                self._active_orders[order['id']] = order
                logger.info(f"Market order placed: {order['id']}")
                return order
                
            logger.error("Failed to place market order")
            return None
            
        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            return None
            
    async def place_limit_order(
        self,
        side: str,
        quantity: Decimal,
        price: Decimal
    ) -> Optional[Dict]:
        """
        Place a limit order.
        
        Args:
            side: Order side ('buy' or 'sell')
            quantity: Order quantity in base currency
            price: Limit price
            
        Returns:
            Order details if successful, None if failed
            
        Raises:
            ValueError: If parameters are invalid
        """
        # Validate inputs
        if side not in ['buy', 'sell']:
            raise ValueError(f"Invalid side: {side}")
        if quantity <= 0:
            raise ValueError(f"Invalid quantity: {quantity}")
        if price <= 0:
            raise ValueError(f"Invalid price: {price}")
            
        try:
            # Risk check
            if not await self.risk_manager.validate_order(side, quantity, price):
                logger.warning(f"Order rejected by risk manager: {side} {quantity} @ {price}")
                return None
                
            # Place order
            order = await self.exchange.market.place_limit_order(
                side=side,
                quantity=quantity,
                price=price
            )
            
            if order:
                self._active_orders[order['id']] = order
                logger.info(f"Limit order placed: {order['id']}")
                return order
                
            logger.error("Failed to place limit order")
            return None
            
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return None
            
    async def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an active order.
        
        Args:
            order_id: ID of order to cancel
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            if order_id not in self._active_orders:
                logger.warning(f"Order not found: {order_id}")
                return False
                
            success = await self.exchange.market.cancel_order(order_id)
            if success:
                del self._active_orders[order_id]
                logger.info(f"Order cancelled: {order_id}")
                return True
                
            logger.error(f"Failed to cancel order: {order_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False
            
    def get_active_orders(self) -> List[Dict]:
        """Get list of currently active orders."""
        return list(self._active_orders.values()) 