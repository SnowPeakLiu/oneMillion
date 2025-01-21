import asyncio
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.exchange_client import ExchangeClient
from decimal import Decimal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ConfigTest')

async def test_exchange_configuration():
    logger.info("Starting exchange configuration test...")
    client = None
    
    try:
        # Initialize and authenticate
        client = ExchangeClient()
        authenticated = await client.authenticate()
        if not authenticated:
            logger.error("Failed to authenticate")
            return
        
        # Test 1: Get current price
        price = await client.get_current_price()
        if price:
            logger.info(f"✓ Price check passed: Current {client.instrument} price: {price}")
        else:
            logger.error("✗ Failed to get current price")
            
        # Test 2: Get balance
        balance = await client.get_balance()
        if balance:
            logger.info(f"✓ Balance check passed:")
            logger.info(f"Equity: {balance['equity']} {balance['currency']}")
            logger.info(f"Available: {balance['available_funds']} {balance['currency']}")
        else:
            logger.error("✗ Failed to get balance")
            
        # Test 3: Get order book
        orderbook = await client.get_orderbook(depth=5)
        if orderbook:
            logger.info(f"✓ Orderbook check passed: {len(orderbook['bids'])} bids, {len(orderbook['asks'])} asks")
        else:
            logger.error("✗ Failed to get orderbook")
            
    except Exception as e:
        logger.error(f"Configuration test failed with error: {e}")
        raise
    finally:
        if client:
            await client.close()

if __name__ == "__main__":
    asyncio.run(test_exchange_configuration()) 