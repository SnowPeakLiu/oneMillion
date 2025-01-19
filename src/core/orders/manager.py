"""
Order management module for handling trading operations.

Provides order creation, tracking, and management functionality.

Example:
    order_manager = OrderManager(exchange_client)
    order = await order_manager.place_order('buy', Decimal('0.1'), Decimal('50000'))
"""

from typing import Dict, Optional
from decimal import Decimal
from gate_api.exceptions import GateApiException

from config_local import TRADING_CONFIG
from core.exchange.client import ExchangeClient
from utils.logger import get_logger

logger = get_logger(__name__)

class OrderManager:
    """
    Manages order creation, validation, and tracking.
    
    Handles all order-related operations including placement,
    cancellation, and status tracking.
    
    Args:
        exchange: ExchangeClient instance for API operations
        
    Example:
        manager = OrderManager(exchange_client)
        order = await manager.place_order('buy', Decimal('0.1'))
    """
    
    def __init__(self, exchange: ExchangeClient):
        self.exchange = exchange
        self.orders: Dict[str, Dict] = {}
        
    async def place_order(
        self,
        side: str,
        quantity: Decimal,
        price: Optional[Decimal] = None
    ) -> Optional[Dict]:
        """
        Place a new order with the exchange.
        
        Args:
            side: Order side ('buy' or 'sell')
            quantity: Order quantity
            price: Optional limit price (None for market orders)
            
        Returns:
            Order details dictionary or None if placement fails
            
        Example:
            order = await manager.place_order('buy', Decimal('0.1'), Decimal('50000'))
            if order:
                print(f"Order placed: {order['id']}")
        """
        try:
            order = {
                'currency_pair': self.exchange.trading_pair,
                'side': side.lower(),
                'amount': str(quantity),
                'type': TRADING_CONFIG['order_type'],
                'time_in_force': TRADING_CONFIG['time_in_force']
            }
            
            if price:
                order['price'] = str(price)
            
            logger.info(f"Placing order: {order}")
            result = self.exchange.spot_api.create_order(order)
            
            order_info = {
                'id': result.id,
                'status': result.status,
                'side': result.side,
                'price': float(result.price) if result.price else None,
                'amount': float(result.amount),
                'filled': float(result.filled_total)
            }
            
            self.orders[result.id] = order_info
            logger.info(f"Order placed successfully: {order_info}")
            return order_info
            
        except GateApiException as e:
            logger.error(f"Failed to place order: {e}")
            return None
            
    async def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an existing order.
        
        Args:
            order_id: ID of the order to cancel
            
        Returns:
            True if cancellation successful, False otherwise
            
        Example:
            if await manager.cancel_order('1234'):
                print("Order cancelled successfully")
        """
        try:
            self.exchange.spot_api.cancel_order(
                order_id=order_id,
                currency_pair=self.exchange.trading_pair
            )
            
            if order_id in self.orders:
                del self.orders[order_id]
                logger.info(f"Order {order_id} cancelled successfully")
            return True
            
        except GateApiException as e:
            logger.error(f"Failed to cancel order {order_id}: {e}")
            return False
            
    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Get details of a specific order.
        
        Args:
            order_id: ID of the order to retrieve
            
        Returns:
            Order details dictionary or None if not found
            
        Example:
            order = manager.get_order('1234')
            if order:
                print(f"Order status: {order['status']}")
        """
        return self.orders.get(order_id)
        
    def get_open_orders(self) -> Dict[str, Dict]:
        """
        Get all currently open orders.
        
        Returns:
            Dictionary of open orders indexed by order ID
            
        Example:
            open_orders = manager.get_open_orders()
            print(f"Number of open orders: {len(open_orders)}")
        """
        return {
            order_id: order_info 
            for order_id, order_info in self.orders.items()
            if order_info['status'] in ['open', 'partial']
        } 