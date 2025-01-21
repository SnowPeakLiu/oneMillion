"""
Tests for market data operations using Deribit WebSocket API.
"""

import pytest
from unittest.mock import patch, AsyncMock

from core.exchange.market_data import MarketDataClient, OrderBook

@pytest.fixture
async def mock_exchange():
    """Create a mock exchange client"""
    mock = AsyncMock()
    mock.instrument_name = 'BTC-PERPETUAL'
    mock.request = AsyncMock()
    return mock

@pytest.fixture
async def market_client(mock_exchange):
    """Create a market data client with mocked exchange"""
    return MarketDataClient(mock_exchange)

@pytest.mark.asyncio
async def test_get_current_price(market_client, mock_exchange):
    """Test getting current price"""
    mock_exchange.request.return_value = {
        'last_price': '50000.5'
    }
    
    price = await market_client.get_current_price()
    assert price == 50000.5
    mock_exchange.request.assert_called_once_with(
        'public/ticker',
        {'instrument_name': 'BTC-PERPETUAL'}
    )

@pytest.mark.asyncio
async def test_get_current_price_error(market_client, mock_exchange):
    """Test error handling when getting current price"""
    mock_exchange.request.side_effect = Exception('API error')
    
    with pytest.raises(Exception):
        await market_client.get_current_price()

@pytest.mark.asyncio
async def test_get_orderbook(market_client, mock_exchange):
    """Test getting order book data"""
    mock_exchange.request.return_value = {
        'bids': [['50000', '1.5'], ['49900', '2.0']],
        'asks': [['50100', '1.0'], ['50200', '2.5']],
        'timestamp': 1234567890
    }
    
    orderbook = await market_client.get_orderbook(depth=2)
    assert isinstance(orderbook, OrderBook)
    assert len(orderbook.bids) == 2
    assert len(orderbook.asks) == 2
    assert orderbook.bids[0] == (50000.0, 1.5)
    assert orderbook.asks[0] == (50100.0, 1.0)
    assert orderbook.timestamp == 1234567890
    
    mock_exchange.request.assert_called_once_with(
        'public/get_order_book',
        {
            'instrument_name': 'BTC-PERPETUAL',
            'depth': 2
        }
    ) 