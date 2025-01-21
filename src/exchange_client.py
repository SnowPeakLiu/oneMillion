from typing import Dict, List, Optional, Any
from decimal import Decimal
import time
import logging
import requests
import hashlib
import hmac
import json
import websockets
import asyncio
from urllib.parse import urlencode
from gate_api.exceptions import GateApiException
from gate_api import ApiClient, SpotApi, Configuration
from src.core.config_local import EXCHANGE_CONFIG, TRADING_CONFIG, RISK_CONFIG
import urllib3
from urllib3.exceptions import MaxRetryError, NewConnectionError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Deribit_Client')

class ExchangeClient:
    def __init__(self):
        """Initialize Deribit API client with configuration"""
        self.ws_url = EXCHANGE_CONFIG['ws_url']
        self.client_id = EXCHANGE_CONFIG['client_id']
        self.client_secret = EXCHANGE_CONFIG['client_secret']
        self.instrument = EXCHANGE_CONFIG['instrument_name']
        
        # WebSocket connection
        self.ws = None
        self.ws_connected = False
        self.request_id = 1
        
        # Initialize state
        self.access_token = None
        self.refresh_token = None
        
        logger.info(f"Initializing Deribit client for {self.instrument}")

    def _get_request_id(self) -> int:
        """Generate unique request ID"""
        self.request_id += 1
        return self.request_id

    async def _call_api(self, msg: Dict) -> Optional[Dict]:
        """Make API call using WebSocket"""
        if not self.ws:
            self.ws = await websockets.connect(self.ws_url)
            self.ws_connected = True
            
        try:
            await self.ws.send(json.dumps(msg))
            response = await self.ws.recv()
            return json.loads(response)
        except Exception as e:
            logger.error(f"API call error: {e}")
            return None

    async def authenticate(self) -> bool:
        """Authenticate with Deribit API"""
        auth_msg = {
            "jsonrpc": "2.0",
            "id": self._get_request_id(),
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        }
        
        response = await self._call_api(auth_msg)
        if response and 'result' in response:
            self.access_token = response['result']['access_token']
            self.refresh_token = response['result']['refresh_token']
            logger.info("Successfully authenticated")
            return True
        else:
            logger.error(f"Authentication failed: {response.get('error') if response else 'No response'}")
            return False

    async def get_current_price(self) -> Optional[float]:
        """Get current price for instrument"""
        msg = {
            "jsonrpc": "2.0",
            "id": self._get_request_id(),
            "method": "public/ticker",
            "params": {
                "instrument_name": self.instrument
            }
        }
        
        response = await self._call_api(msg)
        if response and 'result' in response:
            return float(response['result']['last_price'])
        return None

    async def get_balance(self) -> Optional[Dict]:
        """Get account balance"""
        msg = {
            "jsonrpc": "2.0",
            "id": self._get_request_id(),
            "method": "private/get_account_summary",
            "params": {
                "currency": EXCHANGE_CONFIG['currency'],
                "extended": True
            }
        }
        
        response = await self._call_api(msg)
        if response and 'result' in response:
            result = response['result']
            return {
                'equity': Decimal(str(result['equity'])),
                'available_funds': Decimal(str(result['available_funds'])),
                'margin_balance': Decimal(str(result['margin_balance'])),
                'currency': result['currency']
            }
        return None

    async def get_orderbook(self, depth: int = 10) -> Optional[Dict]:
        """Get order book data"""
        msg = {
            "jsonrpc": "2.0",
            "id": self._get_request_id(),
            "method": "public/get_order_book",
            "params": {
                "instrument_name": self.instrument,
                "depth": depth
            }
        }
        
        response = await self._call_api(msg)
        if response and 'result' in response:
            return {
                'bids': [[float(bid[0]), float(bid[1])] for bid in response['result']['bids']],
                'asks': [[float(ask[0]), float(ask[1])] for ask in response['result']['asks']]
            }
        return None

    async def get_position(self) -> Optional[Dict]:
        """Get current position"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._get_request_id(),
                "method": "private/get_position",
                "params": {
                    "instrument_name": self.instrument
                }
            }
            
            await self.ws.send(json.dumps(request))
            response = await self.ws.recv()
            result = json.loads(response)
            
            if 'result' in result:
                position = result['result']
                return {
                    'size': float(position['size']),
                    'size_currency': float(position['size_currency']),
                    'entry_price': float(position['average_price']),
                    'liquidation_price': float(position['estimated_liquidation_price']),
                    'unrealized_pnl': float(position['total_profit_loss']),
                    'leverage': float(position['leverage'])
                }
            else:
                logger.error(f"Failed to get position: {result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting position: {str(e)}")
            return None

    async def place_order(
        self,
        side: str,
        amount: Decimal,
        price: Optional[Decimal] = None,
        order_type: str = "limit",
        post_only: bool = False,
        reduce_only: bool = False
    ) -> Optional[Dict]:
        """Place a new order"""
        try:
            params = {
                "instrument_name": self.instrument,
                "amount": float(amount),
                "type": order_type,
                "post_only": post_only,
                "reduce_only": reduce_only
            }
            
            if price:
                params["price"] = float(price)
            
            request = {
                "jsonrpc": "2.0",
                "id": self._get_request_id(),
                "method": f"private/{side}",
                "params": params
            }
            
            await self.ws.send(json.dumps(request))
            response = await self.ws.recv()
            result = json.loads(response)
            
            if 'result' in result:
                order = result['result']['order']
                return {
                    'order_id': order['order_id'],
                    'price': float(order['price']),
                    'amount': float(order['amount']),
                    'filled': float(order['filled_amount']),
                    'status': order['order_state']
                }
            else:
                logger.error(f"Failed to place order: {result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return None

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._get_request_id(),
                "method": "private/cancel",
                "params": {
                    "order_id": order_id
                }
            }
            
            await self.ws.send(json.dumps(request))
            response = await self.ws.recv()
            result = json.loads(response)
            
            if 'result' in result:
                return True
            else:
                logger.error(f"Failed to cancel order: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error canceling order: {str(e)}")
            return False

    async def close(self):
        """Close WebSocket connection"""
        if self.ws and self.ws_connected:
            await self.ws.close()
            self.ws_connected = False