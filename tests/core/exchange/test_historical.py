"""
Tests for historical data operations using Deribit WebSocket API.
"""

import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta

from core.exchange.historical import HistoricalDataClient

@pytest.fixture
async def mock_exchange():
    """Create a mock exchange client"""
    mock = AsyncMock()
    mock.instrument_name = 'BTC-PERPETUAL'
    mock.request = AsyncMock()
    return mock

@pytest.fixture
async def historical_client(mock_exchange):
    """Create a historical data client with mocked exchange"""
    return HistoricalDataClient(mock_exchange)

@pytest.mark.asyncio
async def test_get_historical_data(historical_client, mock_exchange):
    """Test getting historical candlestick data"""
    mock_exchange.request.return_value = {
        'ticks': [
            {
                'timestamp': 1234567890000,
                'open': '50000',
                'high': '51000',
                'low': '49000',
                'close': '50500',
                'volume': '100'
            }
        ]
    }
    
    candles = await historical_client.get_historical_data('1h')
    assert len(candles) == 1
    assert isinstance(candles[0], dict)
    mock_exchange.request.assert_called_once()

@pytest.mark.asyncio
async def test_get_historical_data_invalid_interval(historical_client):
    """Test error handling for invalid interval"""
    with pytest.raises(ValueError, match='Invalid interval'):
        await historical_client.get_historical_data('invalid')

@pytest.mark.asyncio
async def test_get_historical_data_error(historical_client, mock_exchange):
    """Test error handling when getting historical data"""
    mock_exchange.request.side_effect = Exception('API error')
    
    with pytest.raises(Exception):
        await historical_client.get_historical_data('1h') 