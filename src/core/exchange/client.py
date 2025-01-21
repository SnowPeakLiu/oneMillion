"""
Main Deribit exchange client.

Integrates market data, historical data, and account operations.
"""

import aiohttp
import asyncio
import json
import time
import hmac
import hashlib
import base64
from typing import Dict, Any

from config_local import EXCHANGE_CONFIG
from utils.logger import get_logger
from .market_data import MarketDataClient
from .historical import HistoricalDataClient
from .account import AccountClient

logger = get_logger(__name__)

class ExchangeClient:
    """
    Main Deribit exchange client integrating all operations.
    
    Provides access to market data, historical data, and account operations
    through specialized client instances.
    
    Example:
        client = ExchangeClient()
        price = await client.market.get_current_price()
        candles = await client.historical.get_historical_data('1h')
        fees = await client.account.get_trading_fees()
    """
    
    TESTNET_URL = 'wss://test.deribit.com/ws/api/v2'
    PRODUCTION_URL = 'wss://www.deribit.com/ws/api/v2'
    
    def __init__(self):
        """Initialize the exchange client with configuration"""
        self.config = EXCHANGE_CONFIG
        self.use_testnet = self.config.get('use_testnet', True)
        self.ws_url = self.TESTNET_URL if self.use_testnet else self.PRODUCTION_URL
        self.env = 'TESTNET' if self.use_testnet else 'PRODUCTION'
        
        logger.info(f'Initializing Deribit client in {self.env} environment')
        
        self.client_id = EXCHANGE_CONFIG['client_id']
        self.client_secret = EXCHANGE_CONFIG['client_secret']
        self.instrument_name = EXCHANGE_CONFIG['instrument_name']
        self.currency = EXCHANGE_CONFIG['currency']
        
        # Initialize specialized clients
        self.market = MarketDataClient(self)
        self.historical = HistoricalDataClient(self)
        self.account = AccountClient(self)
        
    async def _get_auth_headers(self) -> Dict[str, Any]:
        """Generate authentication headers for API requests"""
        timestamp = int(time.time() * 1000)
        nonce = str(timestamp)
        
        signature_string = f'{timestamp}\n{nonce}\n'
        signature = hmac.new(
            bytes(self.client_secret, 'utf-8'),
            bytes(signature_string, 'utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'client_id': self.client_id,
            'timestamp': str(timestamp),
            'nonce': nonce,
            'signature': signature
        }
        
    async def request(self, method: str, params: Dict[str, Any] = None, auth: bool = False) -> Dict[str, Any]:
        """Make a request to the Deribit API"""
        request_id = int(time.time() * 1000)
        message = {
            'jsonrpc': '2.0',
            'id': request_id,
            'method': method,
            'params': params or {}
        }
        
        if auth:
            message['params'].update(await self._get_auth_headers())
            
        session = aiohttp.ClientSession()
        try:
            ws = await session.ws_connect(self.ws_url)
            try:
                await ws.send_json(message)
                response = await ws.receive_json()
                return response.get('result')
            finally:
                await ws.close()
        finally:
            await session.close() 