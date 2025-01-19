"""
Gate.io exchange integration package.

This package provides a comprehensive interface to the Gate.io exchange API,
organized into specialized clients for different types of operations.

Modules:
    client: Main exchange client that integrates all operations
    market_data: Real-time market data operations
    historical: Historical data retrieval operations
    account: Account-related operations

Example:
    from core.exchange.client import ExchangeClient
    
    client = ExchangeClient()
    price = await client.market.get_current_price()
    candles = await client.historical.get_historical_data('1h')
    fees = await client.account.get_trading_fees()
"""

from .client import ExchangeClient
from .market_data import MarketDataClient
from .historical import HistoricalDataClient
from .account import AccountClient

__all__ = [
    'ExchangeClient',
    'MarketDataClient',
    'HistoricalDataClient',
    'AccountClient'
] 