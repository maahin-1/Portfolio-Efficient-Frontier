from simulator import Simulator


def test_simulator_runs_deterministically_with_seed():
    sim_a = Simulator(T=100, dt=1, seed=42)
    sim_a.run()
    sim_b = Simulator(T=100, dt=1, seed=42)
    sim_b.run()
    assert sim_a.get_prices() == sim_b.get_prices()


def test_simulator_produces_a_price_series_and_snapshots():
    sim = Simulator(T=100, dt=1, seed=1)
    sim.run()
    prices = sim.get_prices()
    snapshots = sim.get_snapshots()
    assert len(prices) == 100
    assert len(snapshots) == 100
    assert all('mid_price' in s for s in snapshots)


def test_simulator_generates_at_least_some_trades_over_a_long_run():
    sim = Simulator(T=500, dt=1, seed=42)
    sim.run()
    assert len(sim.get_trades()) > 0


def test_different_seeds_give_different_price_paths():
    sim_a = Simulator(T=100, dt=1, seed=1)
    sim_a.run()
    sim_b = Simulator(T=100, dt=1, seed=2)
    sim_b.run()
    assert sim_a.get_prices() != sim_b.get_prices()
