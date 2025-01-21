import asyncio
import logging
from exchange_client import ExchangeClient
from decimal import Decimal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ConfigTest')

async def test_exchange_configuration():
    logger.info("Starting exchange configuration test...")
    
    try:
        # Initialize exchange client
        client = ExchangeClient()
        logger.info("✓ Successfully initialized exchange client")
        
        # Test 1: Get current price
        price = await client.get_current_price()
        if price:
            logger.info(f"✓ Price check passed: Current {client.trading_pair} price: {price}")
        else:
            logger.error("✗ Failed to get current price")
            
        # Test 2: Get balance
        balance = await client.get_balance()
        if balance:
            logger.info(f"✓ Balance check passed: {balance}")
        else:
            logger.error("✗ Failed to get balance")
            
        # Test 3: Get order book
        orderbook = await client.get_orderbook(depth=5)
        if orderbook:
            logger.info(f"✓ Orderbook check passed: {len(orderbook['bids'])} bids, {len(orderbook['asks'])} asks")
        else:
            logger.error("✗ Failed to get orderbook")
            
        # Test 4: Get trading fees
        fees = await client.get_trading_fees()
        if fees:
            logger.info(f"✓ Fee structure check passed: {fees}")
        else:
            logger.error("✗ Failed to get trading fees")
            
        # Test 5: Get historical data
        candles = await client.get_historical_data(interval='1h', limit=10)
        if candles:
            logger.info(f"✓ Historical data check passed: Retrieved {len(candles)} candles")
        else:
            logger.error("✗ Failed to get historical data")
            
        # Test 6: Test order validation (without placing actual orders)
        test_quantity = Decimal('0.001')  # Small test quantity
        test_price = Decimal(str(price)) if price else Decimal('30000')  # Use current price or fallback
        
        is_valid = client.validate_order('buy', test_quantity, test_price)
        logger.info(f"✓ Order validation check: {'passed' if is_valid else 'failed'}")
        
        logger.info("\nConfiguration Test Summary:")
        logger.info(f"Trading Pair: {client.trading_pair}")
        logger.info(f"Environment: {'TESTNET' if client.config.host.find('testnet') != -1 else 'PRODUCTION'}")
        logger.info(f"API Host: {client.config.host}")
        
    except Exception as e:
        logger.error(f"Configuration test failed with error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_exchange_configuration()) 