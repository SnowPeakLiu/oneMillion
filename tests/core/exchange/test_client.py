"""
Tests for the main Gate.io exchange client.

Tests initialization and integration of specialized clients.
"""

import pytest
from unittest.mock import patch

from core.exchange.client import ExchangeClient

@pytest.fixture
def exchange_client():
    """Create an exchange client with mocked API"""
    with patch('gate_api.ApiClient'), \
         patch('gate_api.SpotApi'), \
         patch('core.exchange.market_data.MarketDataClient'), \
         patch('core.exchange.historical.HistoricalDataClient'), \
         patch('core.exchange.account.AccountClient'):
        client = ExchangeClient()
        return client

def test_client_initialization(exchange_client):
    """Test client initialization and specialized client setup"""
    assert hasattr(exchange_client, 'market')
    assert hasattr(exchange_client, 'historical')
    assert hasattr(exchange_client, 'account')
    
def test_testnet_configuration():
    """Test testnet configuration setup"""
    with patch('gate_api.ApiClient') as mock_api_client, \
         patch('gate_api.SpotApi'), \
         patch('core.exchange.market_data.MarketDataClient'), \
         patch('core.exchange.historical.HistoricalDataClient'), \
         patch('core.exchange.account.AccountClient'), \
         patch('config_local.EXCHANGE_CONFIG', {
             'api_key': 'test_key',
             'api_secret': 'test_secret',
             'test_base_url': 'test_url',
             'base_url': 'prod_url',
             'use_testnet': True,
             'trading_pair': 'BTC_USDT'
         }):
        client = ExchangeClient()
        mock_api_client.assert_called_once()
        config = mock_api_client.call_args[0][0]
        assert config.host == 'test_url'
        
def test_production_configuration():
    """Test production configuration setup"""
    with patch('gate_api.ApiClient') as mock_api_client, \
         patch('gate_api.SpotApi'), \
         patch('core.exchange.market_data.MarketDataClient'), \
         patch('core.exchange.historical.HistoricalDataClient'), \
         patch('core.exchange.account.AccountClient'), \
         patch('config_local.EXCHANGE_CONFIG', {
             'api_key': 'test_key',
             'api_secret': 'test_secret',
             'test_base_url': 'test_url',
             'base_url': 'prod_url',
             'use_testnet': False,
             'trading_pair': 'BTC_USDT'
         }):
        client = ExchangeClient()
        mock_api_client.assert_called_once()
        config = mock_api_client.call_args[0][0]
        assert config.host == 'prod_url' 