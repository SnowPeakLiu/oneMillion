"""
Shared test fixtures for exchange client tests.
"""

import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_spot_api():
    """Create a mock spot API"""
    return Mock()

@pytest.fixture
def exchange_client(mock_spot_api):
    """Create an exchange client with mocked API"""
    with patch('gate_api.ApiClient'), \
         patch('gate_api.SpotApi', return_value=mock_spot_api):
        from core.exchange.client import ExchangeClient
        client = ExchangeClient()
        return client 