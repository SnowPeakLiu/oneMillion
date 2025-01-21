"""
Position management module for tracking and managing trading positions.

This module provides functionality for:
- Position tracking and updates
- Position size calculations
- PnL monitoring
- Position risk metrics
"""

from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime

from utils.logger import get_logger
from core.exchange.client import ExchangeClient

logger = get_logger(__name__)

class Position:
    """
    Represents a trading position.
    
    Tracks position details including size, entry price,
    current price, and calculated metrics like PnL.
    """
    
    def __init__(
        self,
        symbol: str,
        side: str,
        size: Decimal,
        entry_price: Decimal
    ):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.entry_price = entry_price
        self.current_price: Optional[Decimal] = None
        self.last_update: Optional[datetime] = None
        
    @property
    def value(self) -> Optional[Decimal]:
        """Calculate position value in quote currency."""
        if self.current_price is None:
            return None
        return self.size * self.current_price
        
    @property
    def unrealized_pnl(self) -> Optional[Decimal]:
        """Calculate unrealized PnL."""
        if self.current_price is None:
            return None
            
        if self.side == 'buy':
            return (self.current_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.current_price) * self.size
            
    def update_price(self, price: Decimal) -> None:
        """Update current price and timestamp."""
        self.current_price = price
        self.last_update = datetime.utcnow()

class PositionManager:
    """
    Manages trading positions and position-related operations.
    
    Handles position tracking, updates, and risk calculations
    for all open positions.
    
    Args:
        exchange_client: ExchangeClient instance for market data
        
    Example:
        client = ExchangeClient()
        pos_mgr = PositionManager(client)
        
        # Open a new position
        await pos_mgr.open_position('BTC-PERPETUAL', 'buy', 0.1, 50000)
    """
    
    def __init__(self, exchange_client: ExchangeClient):
        self.exchange = exchange_client
        self._positions: Dict[str, Position] = {}
        
    async def open_position(
        self,
        symbol: str,
        side: str,
        size: Decimal,
        entry_price: Decimal
    ) -> Optional[Position]:
        """
        Open a new position.
        
        Args:
            symbol: Trading pair symbol
            side: Position side ('buy' or 'sell')
            size: Position size
            entry_price: Entry price
            
        Returns:
            New Position instance if successful, None if failed
            
        Raises:
            ValueError: If parameters are invalid
        """
        # Validate inputs
        if side not in ['buy', 'sell']:
            raise ValueError(f"Invalid side: {side}")
        if size <= 0:
            raise ValueError(f"Invalid size: {size}")
        if entry_price <= 0:
            raise ValueError(f"Invalid entry price: {entry_price}")
            
        try:
            # Create position
            position = Position(
                symbol=symbol,
                side=side,
                size=size,
                entry_price=entry_price
            )
            
            # Get current price
            current_price = await self.exchange.market.get_current_price()
            if current_price:
                position.update_price(Decimal(str(current_price)))
                
            # Store position
            self._positions[symbol] = position
            logger.info(f"Opened {side} position: {size} {symbol} @ {entry_price}")
            return position
            
        except Exception as e:
            logger.error(f"Error opening position: {e}")
            return None
            
    async def close_position(self, symbol: str) -> bool:
        """
        Close an open position.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            True if closed successfully, False otherwise
        """
        try:
            if symbol not in self._positions:
                logger.warning(f"No open position for {symbol}")
                return False
                
            position = self._positions[symbol]
            current_price = await self.exchange.market.get_current_price()
            
            if current_price:
                position.update_price(Decimal(str(current_price)))
                pnl = position.unrealized_pnl
                logger.info(
                    f"Closed {position.side} position: {position.size} {symbol} "
                    f"PnL: {pnl if pnl is not None else 'N/A'}"
                )
                
            del self._positions[symbol]
            return True
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return False
            
    async def update_positions(self) -> None:
        """Update all position prices with current market data."""
        try:
            for symbol, position in self._positions.items():
                current_price = await self.exchange.market.get_current_price()
                if current_price:
                    position.update_price(Decimal(str(current_price)))
                    logger.debug(
                        f"Updated {symbol} position: "
                        f"Price: {current_price}, "
                        f"PnL: {position.unrealized_pnl}"
                    )
                    
        except Exception as e:
            logger.error(f"Error updating positions: {e}")
            
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position details for a symbol."""
        return self._positions.get(symbol)
        
    def get_all_positions(self) -> Dict[str, Position]:
        """Get all open positions."""
        return dict(self._positions)
        
    def get_total_value(self) -> Optional[Decimal]:
        """Calculate total value of all positions."""
        try:
            total = Decimal('0')
            for position in self._positions.values():
                value = position.value
                if value is not None:
                    total += value
            return total
            
        except Exception as e:
            logger.error(f"Error calculating total value: {e}")
            return None 