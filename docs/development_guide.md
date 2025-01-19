# Development Guide

## File Organization 📁
- Keep related files in the same directory
- Use meaningful file names that match class names
- Create __init__.py files for clean imports

## Code Navigation 🔍
- Use TODO comments that Cursor can track
- Create clear section separators in large files
- Keep main trading logic in separate files from utilities

## Testing Setup 🛠
- Keep test files adjacent to implementation files
- Use pytest for testing (Cursor has good integration)
- Create fixtures in conftest.py

## Code Style Guide
### Type Hints
```python
from typing import Dict, List, Optional
from decimal import Decimal

class Exchange:
    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        price: Optional[Decimal] = None
    ) -> Dict:
        """
        Place an order on the exchange.
        
        Args:
            symbol: Trading pair symbol
            side: 'buy' or 'sell'
            quantity: Order quantity
            price: Optional limit price
            
        Returns:
            Dict containing order details
        """
        pass
```

### Code Organization
```python
# region Exchange Operations
async def place_order():
    pass

async def cancel_order():
    pass
# endregion

# region Market Data
async def get_ticker():
    pass

async def get_orderbook():
    pass
# endregion
```

## Debug Configuration 🐛
- Set up launch.json for debugging
- Add conditional breakpoints for specific trading conditions
- Use logging points for non-breaking debug info

## Git Workflow 📝
### Commit Structure
- Group related changes
- Use meaningful commit messages
- Keep changes atomic

Example commit messages:
- feat(exchange): Implement order placement
- fix(risk): Update position size calculation
- test(strategy): Add unit tests for momentum

## Documentation 📚
Keep these docs updated:
- README.md: Project overview
- API.md: Interface documentation
- CONTRIBUTING.md: Development guidelines

## Productivity Tips ⚡️
- Use Cursor's AI for boilerplate code
- Leverage code snippets for common patterns
- Use multi-cursor editing for repetitive changes
