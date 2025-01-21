"""Tests for the position management module."""

import pytest
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta

from core.position.position_manager import Position, PositionManager
from core.exchange.client import ExchangeClient

# Position class tests
def test_position_initialization():
    """Test position object initialization."""
    position = Position(
        symbol='BTC-PERPETUAL',
        side='buy',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    assert position.symbol == 'BTC-PERPETUAL'
    assert position.side == 'buy'
    assert position.size == Decimal('0.1')
    assert position.entry_price == Decimal('50000')
    assert position.current_price is None
    assert position.last_update is None

def test_position_value_calculation():
    """Test position value calculation."""
    position = Position(
        symbol='BTC-PERPETUAL',
        side='buy',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    # Without current price
    assert position.value is None
    
    # With current price
    position.update_price(Decimal('55000'))
    assert position.value == Decimal('5500')  # 0.1 * 55000

def test_position_pnl_calculation():
    """Test PnL calculations for both long and short positions."""
    # Long position
    long_pos = Position(
        symbol='BTC-PERPETUAL',
        side='buy',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    # Without current price
    assert long_pos.unrealized_pnl is None
    
    # Profit scenario
    long_pos.update_price(Decimal('55000'))
    assert long_pos.unrealized_pnl == Decimal('500')  # (55000 - 50000) * 0.1
    
    # Loss scenario
    long_pos.update_price(Decimal('45000'))
    assert long_pos.unrealized_pnl == Decimal('-500')  # (45000 - 50000) * 0.1
    
    # Short position
    short_pos = Position(
        symbol='BTC-PERPETUAL',
        side='sell',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    # Profit scenario
    short_pos.update_price(Decimal('45000'))
    assert short_pos.unrealized_pnl == Decimal('500')  # (50000 - 45000) * 0.1
    
    # Loss scenario
    short_pos.update_price(Decimal('55000'))
    assert short_pos.unrealized_pnl == Decimal('-500')  # (50000 - 55000) * 0.1

def test_position_update_price():
    """Test position price updates."""
    position = Position(
        symbol='BTC-PERPETUAL',
        side='buy',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    before_update = datetime.utcnow()
    position.update_price(Decimal('55000'))
    after_update = datetime.utcnow()
    
    assert position.current_price == Decimal('55000')
    assert before_update <= position.last_update <= after_update

# PositionManager class tests
@pytest.fixture
def mock_exchange():
    """Create a mock exchange client."""
    mock = Mock(spec=ExchangeClient)
    mock.market = Mock()
    mock.market.get_current_price = AsyncMock()
    return mock

@pytest.fixture
def position_manager(mock_exchange):
    """Create a position manager with mock dependencies."""
    return PositionManager(mock_exchange)

@pytest.mark.asyncio
async def test_open_position_success(position_manager, mock_exchange):
    """Test successful position opening."""
    mock_exchange.market.get_current_price.return_value = 55000
    
    position = await position_manager.open_position(
        symbol='BTC-PERPETUAL',
        side='buy',
        size=Decimal('0.1'),
        entry_price=Decimal('50000')
    )
    
    assert position is not None
    assert position.symbol == 'BTC-PERPETUAL'
    assert position.current_price == Decimal('55000')
    assert len(position_manager.get_all_positions()) == 1

@pytest.mark.asyncio
async def test_open_position_invalid_inputs(position_manager):
    """Test position opening with invalid inputs."""
    # Invalid side
    with pytest.raises(ValueError, match="Invalid side"):
        await position_manager.open_position(
            'BTC-PERPETUAL',
            'invalid',
            Decimal('0.1'),
            Decimal('50000')
        )
    
    # Invalid size
    with pytest.raises(ValueError, match="Invalid size"):
        await position_manager.open_position(
            'BTC-PERPETUAL',
            'buy',
            Decimal('-0.1'),
            Decimal('50000')
        )
    
    # Invalid price
    with pytest.raises(ValueError, match="Invalid entry price"):
        await position_manager.open_position(
            'BTC-PERPETUAL',
            'buy',
            Decimal('0.1'),
            Decimal('-50000')
        )

@pytest.mark.asyncio
async def test_close_position_success(position_manager, mock_exchange):
    """Test successful position closing."""
    # Setup initial position
    mock_exchange.market.get_current_price.return_value = 55000
    await position_manager.open_position(
        'BTC-PERPETUAL',
        'buy',
        Decimal('0.1'),
        Decimal('50000')
    )
    
    # Close position
    result = await position_manager.close_position('BTC-PERPETUAL')
    assert result is True
    assert len(position_manager.get_all_positions()) == 0

@pytest.mark.asyncio
async def test_close_nonexistent_position(position_manager):
    """Test closing a position that doesn't exist."""
    result = await position_manager.close_position('NONEXISTENT')
    assert result is False

@pytest.mark.asyncio
async def test_update_positions(position_manager, mock_exchange):
    """Test updating multiple positions."""
    # Setup positions
    mock_exchange.market.get_current_price.return_value = 50000
    await position_manager.open_position(
        'BTC-PERPETUAL',
        'buy',
        Decimal('0.1'),
        Decimal('50000')
    )
    await position_manager.open_position(
        'ETH-PERPETUAL',
        'sell',
        Decimal('1.0'),
        Decimal('3000')
    )
    
    # Update with new prices
    mock_exchange.market.get_current_price.return_value = 55000
    await position_manager.update_positions()
    
    # Verify updates
    btc_pos = position_manager.get_position('BTC-PERPETUAL')
    eth_pos = position_manager.get_position('ETH-PERPETUAL')
    
    assert btc_pos.current_price == Decimal('55000')
    assert eth_pos.current_price == Decimal('55000')

@pytest.mark.asyncio
async def test_position_value_aggregation(position_manager, mock_exchange):
    """Test total value calculation across positions."""
    mock_exchange.market.get_current_price.return_value = 50000
    
    # Open multiple positions
    await position_manager.open_position(
        'BTC-PERPETUAL',
        'buy',
        Decimal('0.1'),
        Decimal('50000')
    )
    await position_manager.open_position(
        'ETH-PERPETUAL',
        'sell',
        Decimal('1.0'),
        Decimal('3000')
    )
    
    # Calculate total value
    total = position_manager.get_total_value()
    expected = Decimal('0.1') * Decimal('50000') + Decimal('1.0') * Decimal('50000')
    assert total == expected

@pytest.mark.asyncio
async def test_error_handling_no_price(position_manager, mock_exchange):
    """Test handling when price data is unavailable."""
    mock_exchange.market.get_current_price.return_value = None
    
    position = await position_manager.open_position(
        'BTC-PERPETUAL',
        'buy',
        Decimal('0.1'),
        Decimal('50000')
    )
    
    assert position is not None
    assert position.current_price is None
    assert position.value is None
    assert position.unrealized_pnl is None 