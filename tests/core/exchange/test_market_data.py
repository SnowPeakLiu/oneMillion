"""
Tests for market data operations of the exchange client.
"""

import pytest
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_get_current_price(exchange_client, mock_spot_api):
    """Test getting current price"""
    # Setup mock
    mock_ticker = Mock()
    mock_ticker.last = "50000.0"
    mock_spot_api.list_tickers.return_value = [mock_ticker]
    
    # Test
    price = await exchange_client.get_current_price()
    
    # Verify
    assert price == 50000.0
    mock_spot_api.list_tickers.assert_called_once()

@pytest.mark.asyncio
async def test_get_orderbook(exchange_client, mock_spot_api):
    """Test getting orderbook"""
    # Setup mock
    mock_orderbook = {
        'bids': [['49000.0', '1.0'], ['48000.0', '2.0']],
        'asks': [['51000.0', '1.0'], ['52000.0', '2.0']]
    }
    mock_spot_api.list_order_book.return_value = mock_orderbook
    
    # Test
    orderbook = await exchange_client.get_orderbook(depth=2)
    
    # Verify
    assert len(orderbook['bids']) == 2
    assert len(orderbook['asks']) == 2
    assert orderbook['bids'][0] == [49000.0, 1.0]
    assert orderbook['asks'][0] == [51000.0, 1.0]

@pytest.mark.asyncio
async def test_get_current_price_error(exchange_client, mock_spot_api):
    """Test error handling when getting current price"""
    from gate_api.exceptions import GateApiException
    
    # Setup mock to raise exception
    mock_spot_api.list_tickers.side_effect = GateApiException(
        "API Error", "500", "Internal Error"
    )
    
    # Test
    price = await exchange_client.get_current_price()
    
    # Verify
    assert price is None 