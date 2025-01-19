class BaseStrategy:
    def __init__(self, exchange, risk_manager):
        self.exchange = exchange
        self.risk_manager = risk_manager
        self.positions = {}
        
    async def analyze(self, market_data):
        """Analyze market data and generate signals"""
        raise NotImplementedError
        
    async def execute(self, signal):
        """Execute trading signals with risk management"""
        raise NotImplementedError 