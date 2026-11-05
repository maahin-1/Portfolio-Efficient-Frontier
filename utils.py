import numpy as np

def poisson_arrival(lam=1, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    return rng.poisson(lam)

def random_trader_action(orderbook, rng, order_type='limit'):
    side = rng.choice(['buy', 'sell'])
    best_bid = orderbook.get_best_bid() or 100
    best_ask = orderbook.get_best_ask() or 101
    if order_type == 'limit':
        if side == 'buy':
            price = best_bid - rng.integers(0, 3)
        else:
            price = best_ask + rng.integers(0, 3)
    else:  # market
        price = None
    size = rng.integers(1, 10)
    return side, price, size
