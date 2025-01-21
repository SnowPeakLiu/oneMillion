"""
Tests for the main Deribit exchange client.

Tests initialization and integration of specialized clients.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from core.exchange.client import ExchangeClient

class AsyncContextManagerMock:
    """Mock for async context managers"""
    def __init__(self):
        self.aenter = AsyncMock()
        self.aexit = AsyncMock()
        self.ws_connect = AsyncMock()
        self.close = AsyncMock()

    async def __aenter__(self):
        return await self.aenter()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.aexit(exc_type, exc_val, exc_tb)

@pytest.fixture
def mock_ws():
    """Create a mock WebSocket with predefined responses"""
    mock = AsyncMock()
    mock.receive_json.return_value = {
        'jsonrpc': '2.0',
        'id': 123,
        'result': {'test': 'data'}
    }
    mock.send_json = AsyncMock()
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock()
    mock.close = AsyncMock()
    return mock

@pytest.fixture
def mock_session(mock_ws):
    """Create a mock session with WebSocket support"""
    session = AsyncContextManagerMock()
    session.ws_connect = AsyncMock()
    session.ws_connect.return_value = mock_ws
    session.aenter.return_value = session
    return session

@pytest.fixture
async def exchange_client(mock_session):
    """Create an exchange client with mocked WebSocket"""
    with patch('aiohttp.ClientSession', return_value=mock_session):
        client = ExchangeClient()
        return client

@pytest.mark.asyncio
async def test_client_initialization(exchange_client):
    """Test client initialization and specialized client setup"""
    assert hasattr(exchange_client, 'market')
    assert hasattr(exchange_client, 'historical')
    assert hasattr(exchange_client, 'account')
    
@pytest.mark.asyncio
async def test_testnet_configuration(mock_session):
    """Test testnet configuration setup"""
    with patch('aiohttp.ClientSession', return_value=mock_session), \
         patch('core.exchange.market_data.MarketDataClient'), \
         patch('core.exchange.historical.HistoricalDataClient'), \
         patch('core.exchange.account.AccountClient'), \
         patch('config_local.EXCHANGE_CONFIG', {
             'client_id': 'test_id',
             'client_secret': 'test_secret',
             'instrument_name': 'BTC-PERPETUAL',
             'currency': 'BTC',
             'use_testnet': True
         }):
        client = ExchangeClient()
        assert client.ws_url == ExchangeClient.TESTNET_URL
        assert client.instrument_name == 'BTC-PERPETUAL'
        
@pytest.mark.asyncio
async def test_production_configuration(mock_session):
    """Test production configuration setup"""
    config = {
        'client_id': 'test_id',
        'client_secret': 'test_secret',
        'instrument_name': 'BTC-PERPETUAL',
        'currency': 'BTC',
        'use_testnet': False
    }
    
    with patch('aiohttp.ClientSession', return_value=mock_session), \
         patch('core.exchange.market_data.MarketDataClient'), \
         patch('core.exchange.historical.HistoricalDataClient'), \
         patch('core.exchange.account.AccountClient'), \
         patch('core.exchange.client.EXCHANGE_CONFIG', config):
        client = ExchangeClient()
        assert client.ws_url == ExchangeClient.PRODUCTION_URL
        assert client.env == 'PRODUCTION'
        
@pytest.mark.asyncio
async def test_request_method(mock_session, mock_ws):
    """Test the request method with authentication"""
    config = {
        'client_id': 'test_client',
        'client_secret': 'test_secret',
        'instrument_name': 'BTC-PERPETUAL',
        'currency': 'BTC',
        'use_testnet': True
    }
    
    with patch('aiohttp.ClientSession', return_value=mock_session), \
         patch('core.exchange.client.EXCHANGE_CONFIG', config):
        client = ExchangeClient()
        result = await client.request('test_method', {'param': 'value'}, auth=True)
        
        assert result == {'test': 'data'}
        mock_ws.send_json.assert_called_once()
        request_data = mock_ws.send_json.call_args[0][0]
        assert request_data['method'] == 'test_method'
        assert request_data['params']['param'] == 'value'
        assert 'client_id' in request_data['params']  # Check auth params are included 