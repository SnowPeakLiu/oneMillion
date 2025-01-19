"""
Tests for historical data operations of the exchange client.
"""

import pytest
from gate_api.exceptions import GateApiException

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
    assert candles[0]['high'] == 51000.0
    assert candles[0]['low'] == 49000.0
    assert candles[0]['open'] == 49500.0

@pytest.mark.asyncio
async def test_get_historical_data_invalid_interval(exchange_client, mock_spot_api):
    """Test getting historical data with invalid interval"""
    # Test
    candles = await exchange_client.get_historical_data('invalid', 2)
    
    # Verify default interval is used (1h)
    mock_spot_api.list_candlesticks.assert_called_with(
        currency_pair=exchange_client.trading_pair,
        interval='3600',
        limit=2
    )

@pytest.mark.asyncio
async def test_get_historical_data_error(exchange_client, mock_spot_api):
    """Test error handling when getting historical data"""
    # Setup mock to raise exception
    mock_spot_api.list_candlesticks.side_effect = GateApiException(
        "API Error", "500", "Internal Error"
    )
    
    # Test
    candles = await exchange_client.get_historical_data('1h', 2)
    
    # Verify
    assert candles is None 