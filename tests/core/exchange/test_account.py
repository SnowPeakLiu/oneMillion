"""
Tests for account-related operations of the exchange client.
"""

import pytest
from unittest.mock import Mock
from gate_api.exceptions import GateApiException

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

@pytest.mark.asyncio
async def test_get_trading_fees_error(exchange_client, mock_spot_api):
    """Test error handling when getting trading fees"""
    # Setup mock to raise exception
    mock_spot_api.get_fee.side_effect = GateApiException(
        "API Error", "500", "Internal Error"
    )
    
    # Test
    fees = await exchange_client.get_trading_fees()
    
    # Verify
    assert fees is None 