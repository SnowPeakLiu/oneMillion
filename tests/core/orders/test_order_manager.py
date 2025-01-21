"""Tests for the order management module."""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, AsyncMock

from core.orders.order_manager import OrderManager
from core.exchange.client import ExchangeClient
from core.risk.risk_manager import RiskManager

@pytest.fixture
def mock_exchange():
    """Create a mock exchange client."""
    mock = Mock(spec=ExchangeClient)
    mock.market = Mock()
    mock.market.place_market_order = AsyncMock()
    mock.market.place_limit_order = AsyncMock()
    mock.market.cancel_order = AsyncMock()
    return mock

@pytest.fixture
def mock_risk_manager():
    """Create a mock risk manager."""
    mock = Mock(spec=RiskManager)
    mock.validate_order = AsyncMock()
    return mock

@pytest.fixture
def order_manager(mock_exchange, mock_risk_manager):
    """Create an order manager with mock dependencies."""
    return OrderManager(mock_exchange, mock_risk_manager)

@pytest.mark.asyncio
async def test_place_market_order_success(order_manager, mock_exchange, mock_risk_manager):
    """Test successful market order placement."""
    # Setup
    mock_risk_manager.validate_order.return_value = True
    mock_exchange.market.place_market_order.return_value = {
        'id': '123',
        'side': 'buy',
        'quantity': '0.1',
        'type': 'market'
    }
    
    # Execute
    order = await order_manager.place_market_order('buy', Decimal('0.1'))
    
    # Verify
    assert order is not None
    assert order['id'] == '123'
    assert len(order_manager.get_active_orders()) == 1
    mock_risk_manager.validate_order.assert_called_once()
    mock_exchange.market.place_market_order.assert_called_once()

@pytest.mark.asyncio
async def test_place_market_order_risk_reject(order_manager, mock_risk_manager):
    """Test market order rejected by risk manager."""
    # Setup
    mock_risk_manager.validate_order.return_value = False
    
    # Execute
    order = await order_manager.place_market_order('buy', Decimal('0.1'))
    
    # Verify
    assert order is None
    assert len(order_manager.get_active_orders()) == 0

@pytest.mark.asyncio
async def test_place_limit_order_success(order_manager, mock_exchange, mock_risk_manager):
    """Test successful limit order placement."""
    # Setup
    mock_risk_manager.validate_order.return_value = True
    mock_exchange.market.place_limit_order.return_value = {
        'id': '456',
        'side': 'sell',
        'quantity': '0.1',
        'price': '50000',
        'type': 'limit'
    }
    
    # Execute
    order = await order_manager.place_limit_order(
        'sell',
        Decimal('0.1'),
        Decimal('50000')
    )
    
    # Verify
    assert order is not None
    assert order['id'] == '456'
    assert len(order_manager.get_active_orders()) == 1
    mock_risk_manager.validate_order.assert_called_once()
    mock_exchange.market.place_limit_order.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_order_success(order_manager, mock_exchange):
    """Test successful order cancellation."""
    # Setup
    mock_exchange.market.cancel_order.return_value = True
    order_manager._active_orders = {
        '789': {'id': '789', 'side': 'buy', 'quantity': '0.1'}
    }
    
    # Execute
    result = await order_manager.cancel_order('789')
    
    # Verify
    assert result is True
    assert len(order_manager.get_active_orders()) == 0
    mock_exchange.market.cancel_order.assert_called_once_with('789')

@pytest.mark.asyncio
async def test_cancel_nonexistent_order(order_manager):
    """Test cancellation of non-existent order."""
    result = await order_manager.cancel_order('999')
    assert result is False

@pytest.mark.asyncio
async def test_place_market_order_invalid_side(order_manager):
    """Test market order with invalid side."""
    with pytest.raises(ValueError):
        await order_manager.place_market_order('invalid', Decimal('0.1'))

@pytest.mark.asyncio
async def test_place_market_order_invalid_quantity(order_manager):
    """Test market order with invalid quantity."""
    with pytest.raises(ValueError):
        await order_manager.place_market_order('buy', Decimal('-0.1'))

@pytest.mark.asyncio
async def test_place_limit_order_invalid_price(order_manager):
    """Test limit order with invalid price."""
    with pytest.raises(ValueError):
        await order_manager.place_limit_order(
            'buy',
            Decimal('0.1'),
            Decimal('-50000')
        ) 