import pytest

from orderbook import OrderBook


def test_limit_order_rests_in_book_until_matched():
    ob = OrderBook()
    ob.add_order('buy', 99, 10, 'limit', 0)
    assert ob.get_best_bid() == 99
    assert ob.get_best_ask() is None


def test_market_buy_matches_resting_limit_sell():
    ob = OrderBook()
    ob.add_order('sell', 101, 5, 'limit', 0)
    trades = ob.add_order('buy', None, 5, 'market', 1)
    assert trades == [(1, 'buy', 101, 5)]
    assert ob.get_best_ask() is None  # fully filled, level removed


def test_market_buy_partial_fill_leaves_remainder_resting():
    ob = OrderBook()
    ob.add_order('sell', 101, 10, 'limit', 0)
    trades = ob.add_order('buy', None, 4, 'market', 1)
    assert trades == [(1, 'buy', 101, 4)]
    bid_depth, ask_depth = ob.get_depth()
    assert ask_depth == [(101, 6)]  # 10 - 4 remaining


def test_market_buy_sweeps_multiple_price_levels_lowest_first():
    ob = OrderBook()
    ob.add_order('sell', 102, 5, 'limit', 0)
    ob.add_order('sell', 101, 5, 'limit', 0)  # better price, must fill first
    trades = ob.add_order('buy', None, 7, 'market', 1)
    assert trades == [(1, 'buy', 101, 5), (1, 'buy', 102, 2)]


def test_market_sell_matches_highest_bid_first():
    ob = OrderBook()
    ob.add_order('buy', 98, 5, 'limit', 0)
    ob.add_order('buy', 99, 5, 'limit', 0)  # better price for a seller
    trades = ob.add_order('sell', None, 7, 'market', 1)
    assert trades == [(1, 'sell', 99, 5), (1, 'sell', 98, 2)]


def test_fifo_within_same_price_level():
    ob = OrderBook()
    ob.add_order('sell', 101, 3, 'limit', 0)   # first in
    ob.add_order('sell', 101, 3, 'limit', 0)   # second in
    trades = ob.add_order('buy', None, 4, 'market', 1)
    # Should fully drain the first order (3) before touching the second (1).
    assert trades == [(1, 'buy', 101, 3), (1, 'buy', 101, 1)]


def test_market_order_with_empty_book_returns_no_trades():
    ob = OrderBook()
    trades = ob.add_order('buy', None, 5, 'market', 0)
    assert trades == []


def test_spread_and_mid_price():
    ob = OrderBook()
    ob.add_order('buy', 99, 10, 'limit', 0)
    ob.add_order('sell', 101, 10, 'limit', 0)
    assert ob.get_spread() == 2
    assert ob.get_mid_price() == 100.0


def test_spread_is_none_when_one_side_empty():
    ob = OrderBook()
    ob.add_order('buy', 99, 10, 'limit', 0)
    assert ob.get_spread() is None
    assert ob.get_mid_price() is None


def test_volume_imbalance_bounds_and_sign():
    ob = OrderBook()
    ob.add_order('buy', 99, 30, 'limit', 0)
    ob.add_order('sell', 101, 10, 'limit', 0)
    imbalance = ob.get_volume_imbalance()
    assert -1.0 <= imbalance <= 1.0
    assert imbalance > 0  # more buy volume resting than sell


def test_volume_imbalance_zero_when_book_empty():
    ob = OrderBook()
    assert ob.get_volume_imbalance() == 0


def test_snapshot_reports_consistent_state():
    ob = OrderBook()
    ob.add_order('buy', 99, 10, 'limit', 0)
    ob.add_order('sell', 101, 10, 'limit', 0)
    snap = ob.snapshot()
    assert snap['best_bid'] == 99
    assert snap['best_ask'] == 101
    assert snap['spread'] == 2
    assert snap['mid_price'] == 100.0


def test_trade_history_accumulates_across_orders():
    ob = OrderBook()
    ob.add_order('sell', 101, 5, 'limit', 0)
    ob.add_order('buy', None, 5, 'market', 1)
    ob.add_order('sell', 102, 3, 'limit', 2)
    ob.add_order('buy', None, 3, 'market', 3)
    assert len(ob.trade_history) == 2


def test_save_trade_history_writes_csv(tmp_path):
    ob = OrderBook()
    ob.add_order('sell', 101, 5, 'limit', 0)
    ob.add_order('buy', None, 5, 'market', 1)
    out = tmp_path / 'trades.csv'
    ob.save_trade_history(str(out))
    lines = out.read_text().strip().splitlines()
    assert lines[0] == 'timestamp,side,price,size'
    assert len(lines) == 2
