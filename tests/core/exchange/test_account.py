"""
Tests for account operations using Deribit WebSocket API.
"""

import pytest
from unittest.mock import patch, AsyncMock

from core.exchange.account import AccountClient

@pytest.fixture
async def mock_exchange():
    """Create a mock exchange client"""
    mock = AsyncMock()
    mock.currency = 'BTC'
    mock.request = AsyncMock()
    return mock

@pytest.fixture
async def account_client(mock_exchange):
    """Create an account client with mocked exchange"""
    return AccountClient(mock_exchange)

@pytest.mark.asyncio
async def test_get_balance(account_client, mock_exchange):
    """Test getting account balance"""
    mock_exchange.request.return_value = {
        'equity': '1.5',
        'available_funds': '1.0',
        'margin_balance': '1.2',
        'total_pl': '0.3'
    }
    
    balance = await account_client.get_balance()
    assert balance['total_balance'] == 1.5
    assert balance['available_balance'] == 1.0
    assert balance['margin_balance'] == 1.2
    assert balance['unrealized_pnl'] == 0.3
    assert balance['currency'] == 'BTC'
    
    mock_exchange.request.assert_called_once_with(
        'private/get_account_summary',
        {
            'currency': 'BTC',
            'extended': True
        },
        auth=True
    )

@pytest.mark.asyncio
async def test_get_trading_fees(account_client, mock_exchange):
    """Test getting trading fees"""
    mock_exchange.request.return_value = {
        'maker_fee': '-0.00025',
        'taker_fee': '0.00075'
    }
    
    fees = await account_client.get_trading_fees()
    assert fees['maker_fee'] == -0.00025
    assert fees['taker_fee'] == 0.00075
    
    mock_exchange.request.assert_called_once_with(
        'private/get_account_summary',
        {
            'currency': 'BTC',
            'extended': True
        },
        auth=True
    ) 