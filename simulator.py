import numpy as np
from orderbook import OrderBook
from utils import poisson_arrival, random_trader_action

class Simulator:
    def __init__(self, T=1000, dt=1, seed=None):
        self.T = T
        self.dt = dt
        self.time = 0
        self.orderbook = OrderBook()
        self.snapshots = []
        self.prices = []
        self.trades = []
        self.rng = np.random.default_rng(seed)

    def run(self):
        for t in range(self.T):
            self.time = t * self.dt
            # Simulate random order arrivals
            n_limit = poisson_arrival(lam=2, rng=self.rng)
            n_market = poisson_arrival(lam=1, rng=self.rng)
            for _ in range(n_limit):
                side, price, size = random_trader_action(self.orderbook, self.rng, order_type='limit')
                self.orderbook.add_order(side, price, size, 'limit', self.time)
            for _ in range(n_market):
                side, price, size = random_trader_action(self.orderbook, self.rng, order_type='market')
                trades = self.orderbook.add_order(side, price, size, 'market', self.time)
                if trades:
                    self.trades.extend(trades)
            self.snapshots.append(self.orderbook.snapshot())
            self.prices.append(self.orderbook.get_mid_price())

    def get_snapshots(self):
        return self.snapshots

    def get_prices(self):
        return self.prices

    def get_trades(self):
        return self.orderbook.trade_history

    def save_trade_history(self, filename):
        self.orderbook.save_trade_history(filename)
