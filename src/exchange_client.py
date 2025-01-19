from typing import Dict, List, Optional, Any
from decimal import Decimal
import time
import logging
import gate_api
from gate_api.exceptions import GateApiException
from gate_api import ApiClient, SpotApi, Configuration
from config_local import EXCHANGE_CONFIG, TRADING_CONFIG, RISK_CONFIG

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GateIO_TestNet')

class ExchangeClient:
    def __init__(self):
        """Initialize Gate.io API client with configuration"""
        # Create API configuration
        self.config = Configuration(
            key=EXCHANGE_CONFIG['api_key'],
            secret=EXCHANGE_CONFIG['api_secret'],
            host=EXCHANGE_CONFIG['test_base_url'] if EXCHANGE_CONFIG['use_testnet'] else EXCHANGE_CONFIG['base_url']
        )
        
        # Initialize API client
        self.client = ApiClient(self.config)
        self.spot_api = SpotApi(self.client)
        self.trading_pair = EXCHANGE_CONFIG['trading_pair']
        
        # Initialize state
        self.positions: Dict[str, Any] = {}
        self.orders: Dict[str, Any] = {}
        self.balance: Dict[str, Decimal] = {}
        
        # Log initialization
        env = "TESTNET" if EXCHANGE_CONFIG['use_testnet'] else "PRODUCTION"
        logger.info(f"Initializing Gate.io client in {env} environment")
        if EXCHANGE_CONFIG['use_testnet']:
            logger.warning("Running in TESTNET mode - Using test configuration")
        
    def _check_testnet_limits(self, quantity: Decimal, price: Optional[Decimal] = None) -> bool:
        """Additional safety checks for testnet"""
        if not EXCHANGE_CONFIG['use_testnet']:
            return True
            
        try:
            # Check if order size is reasonable for testing
            if price:
                order_value = quantity * price
                if order_value > Decimal('1000'):  # Max $1000 per order in testnet
                    logger.warning(f"Order value {order_value} exceeds testnet limit of $1000")
                    return False
                    
            # Check daily trade count
            today_trades = len([o for o in self.orders.values() 
                              if time.time() - o.create_time < 86400])
            if today_trades >= RISK_CONFIG['max_daily_trades']:
                logger.warning("Daily trade limit reached in testnet")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error in testnet limits check: {e}")
            return False
            
    async def get_current_price(self) -> Optional[float]:
        """Get current price for trading pair"""
        try:
            ticker = self.spot_api.list_tickers(currency_pair=self.trading_pair)
            price = float(ticker[0].last)
            logger.info(f"Current price for {self.trading_pair}: {price}")
            return price
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_current_price: {e}")
            return None
            
    async def get_orderbook(self, depth: int = 10) -> Optional[Dict]:
        """Get order book data"""
        try:
            orderbook = self.spot_api.list_order_book(
                currency_pair=self.trading_pair,
                limit=depth
            )
            return {
                'bids': [[float(p), float(v)] for p, v in orderbook['bids']],
                'asks': [[float(p), float(v)] for p, v in orderbook['asks']]
            }
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return None
            
    async def get_balance(self) -> Optional[Dict[str, Decimal]]:
        """Get account balance with testnet logging"""
        try:
            accounts = self.spot_api.list_spot_accounts()
            self.balance = {
                acc.currency: Decimal(acc.available) 
                for acc in accounts
            }
            
            if EXCHANGE_CONFIG['use_testnet']:
                logger.info(f"Testnet balance: {self.balance}")
            return self.balance
            
        except GateApiException as e:
            logger.error(f"Gate.io API error in get_balance: {e}")
            return None
            
    async def place_order(
        self,
        side: str,
        quantity: Decimal,
        price: Optional[Decimal] = None
    ) -> Optional[Dict]:
        """Place a new order with testnet safety checks"""
        try:
            # Validate against testnet limits
            if not self._check_testnet_limits(quantity, price):
                logger.warning("Order rejected due to testnet limits")
                return None
                
            # Normal order placement logic
            order = {
                'currency_pair': self.trading_pair,
                'side': side.lower(),
                'amount': str(quantity),
                'type': TRADING_CONFIG['order_type'],
                'time_in_force': TRADING_CONFIG['time_in_force']
            }
            
            if price:
                order['price'] = str(price)
            
            logger.info(f"Placing order: {order}")
            result = self.spot_api.create_order(order)
            self.orders[result.id] = result
            
            order_info = {
                'id': result.id,
                'status': result.status,
                'side': result.side,
                'price': float(result.price) if result.price else None,
                'amount': float(result.amount),
                'filled': float(result.filled_total)
            }
            logger.info(f"Order placed successfully: {order_info}")
            return order_info
            
        except GateApiException as e:
            logger.error(f"Gate.io API error in place_order: {e}")
            return None
            
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order"""
        try:
            self.spot_api.cancel_order(
                order_id=order_id,
                currency_pair=self.trading_pair
            )
            if order_id in self.orders:
                del self.orders[order_id]
            return True
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return False
            
    async def get_historical_data(
        self,
        interval: str = '1h',
        limit: int = 100
    ) -> Optional[List[Dict]]:
        """Get historical candlestick data"""
        try:
            # Convert timeframe to seconds
            interval_map = {
                '1m': '60',
                '5m': '300',
                '15m': '900',
                '30m': '1800',
                '1h': '3600',
                '4h': '14400',
                '1d': '86400'
            }
            
            candlesticks = self.spot_api.list_candlesticks(
                currency_pair=self.trading_pair,
                interval=interval_map.get(interval, '3600'),
                limit=limit
            )
            
            return [{
                'timestamp': candle[0],
                'volume': float(candle[1]),
                'close': float(candle[2]),
                'high': float(candle[3]),
                'low': float(candle[4]),
                'open': float(candle[5])
            } for candle in candlesticks]
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return None
            
    async def get_trading_fees(self) -> Optional[Dict]:
        """Get trading fee rates"""
        try:
            fee_info = self.spot_api.get_fee(currency_pair=self.trading_pair)
            return {
                'maker_fee': float(fee_info.maker_fee),
                'taker_fee': float(fee_info.taker_fee)
            }
        except GateApiException as e:
            print(f"Gate.io API error: {e}")
            return None
            
    def validate_order(
        self,
        side: str,
        quantity: Decimal,
        price: Optional[Decimal] = None
    ) -> bool:
        """Validate order parameters against risk management rules"""
        try:
            # Additional testnet validation
            if EXCHANGE_CONFIG['use_testnet'] and not self._check_testnet_limits(quantity, price):
                return False
                
            # Check if we have enough balance
            if side.lower() == 'buy':
                required_balance = quantity * (price or Decimal('0'))
                if self.balance.get('USDT', Decimal('0')) < required_balance:
                    logger.warning(f"Insufficient USDT balance for buy order")
                    return False
            else:
                base_currency = self.trading_pair.split('_')[0]
                if self.balance.get(base_currency, Decimal('0')) < quantity:
                    logger.warning(f"Insufficient {base_currency} balance for sell order")
                    return False
                    
            # Check position size against risk limits
            position_value = quantity * (price or Decimal('0'))
            if position_value > Decimal(str(RISK_CONFIG['max_position_size'])) * self.get_total_balance():
                logger.warning(f"Order size {position_value} exceeds position size limit")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error in order validation: {e}")
            return False
            
    def get_total_balance(self) -> Decimal:
        """Calculate total balance in USDT"""
        try:
            total = Decimal('0')
            for currency, amount in self.balance.items():
                if currency == 'USDT':
                    total += amount
                else:
                    # Get current price for the currency
                    price = self.get_current_price()
                    if price:
                        total += amount * Decimal(str(price))
            return total
        except Exception as e:
            print(f"Balance calculation error: {e}")
            return Decimal('0') 