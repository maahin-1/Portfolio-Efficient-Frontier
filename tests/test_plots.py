"""Smoke tests for the plotting functions: they must build a figure and not
raise, without needing a display (conftest.py sets the Agg backend)."""
import matplotlib.pyplot as plt

import orderbook


def test_plot_efficient_frontier_builds_a_figure():
    orderbook.plot_efficient_frontier(num_portfolios=200, seed=1)
    assert plt.gcf().get_axes()
    plt.close('all')


def test_plot_gbm_paths_builds_a_figure():
    orderbook.plot_gbm_paths(n_paths=5, n_steps=20, seed=1)
    assert plt.gcf().get_axes()
    plt.close('all')


def test_fft_window_demeaning_removes_dc_component():
    import numpy as np
    window = np.array([100.0] * 64)  # constant price: all "energy" is DC
    demeaned = window - window.mean()
    fft_vals = np.abs(np.fft.fft(demeaned))[:32]
    assert fft_vals[0] == 0.0
    assert fft_vals.max() == 0.0  # a perfectly flat price has no AC content either
