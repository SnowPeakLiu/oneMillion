"""
Tests for the Gate.io exchange client module.
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from core.exchange.client import ExchangeClient

@pytest.fixture
def mock_spot_api():
    """Create a mock spot API"""
    return Mock()

@pytest.fixture
def exchange_client(mock_spot_api):
    """Create an exchange client with mocked API"""
    with patch('gate_api.ApiClient'), \
         patch('gate_api.SpotApi', return_value=mock_spot_api):
        client = ExchangeClient()
        return client

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
async def test_get_historical_data(exchange_client, mock_spot_api):
    """Test getting historical data"""
    # Setup mock
    mock_candles = [
        [1600000000, "100.0", "50000.0", "51000.0", "49000.0", "49500.0"],
        [1600003600, "200.0", "51000.0", "52000.0", "50000.0", "50500.0"]
    ]
    mock_spot_api.list_candlesticks.return_value = mock_candles
    
    # Test
    candles = await exchange_client.get_historical_data('1h', 2)
    
    # Verify
    assert len(candles) == 2
    assert candles[0]['timestamp'] == 1600000000
    assert candles[0]['volume'] == 100.0
    assert candles[0]['close'] == 50000.0

@pytest.mark.asyncio
async def test_get_trading_fees(exchange_client, mock_spot_api):
    """Test getting trading fees"""
    # Setup mock
    mock_fees = Mock()
    mock_fees.maker_fee = "0.001"
    mock_fees.taker_fee = "0.002"
    mock_spot_api.get_fee.return_value = mock_fees
    
    # Test
    fees = await exchange_client.get_trading_fees()
    
    # Verify
    assert fees['maker_fee'] == 0.001
    assert fees['taker_fee'] == 0.002 