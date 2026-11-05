import numpy as np

from orderbook import OrderBook
from utils import poisson_arrival, random_trader_action


def test_poisson_arrival_is_nonnegative_integer():
    rng = np.random.default_rng(0)
    for _ in range(50):
        n = poisson_arrival(lam=2, rng=rng)
        assert isinstance(n, (int, np.integer))
        assert n >= 0


def test_poisson_arrival_deterministic_with_seeded_rng():
    a = poisson_arrival(lam=3, rng=np.random.default_rng(42))
    b = poisson_arrival(lam=3, rng=np.random.default_rng(42))
    assert a == b


def test_random_trader_action_limit_order_has_price():
    rng = np.random.default_rng(1)
    ob = OrderBook()
    side, price, size = random_trader_action(ob, rng, order_type='limit')
    assert side in ('buy', 'sell')
    assert price is not None
    assert 1 <= size <= 9


def test_random_trader_action_market_order_has_no_price():
    rng = np.random.default_rng(1)
    ob = OrderBook()
    side, price, size = random_trader_action(ob, rng, order_type='market')
    assert price is None
    assert 1 <= size <= 9


def test_random_trader_action_uses_book_bid_ask_when_present():
    rng = np.random.default_rng(1)
    ob = OrderBook()
    ob.add_order('buy', 50, 5, 'limit', 0)
    ob.add_order('sell', 55, 5, 'limit', 0)
    # With a real spread in the book, limit prices should be anchored near it,
    # not the hard-coded 100/101 fallback used for an empty book.
    seen_near_book = False
    for _ in range(30):
        side, price, _ = random_trader_action(ob, rng, order_type='limit')
        if side == 'buy' and price is not None and 40 <= price <= 50:
            seen_near_book = True
        if side == 'sell' and price is not None and 55 <= price <= 65:
            seen_near_book = True
    assert seen_near_book
