# --- Markowitz Efficient Frontier Plot ---
def plot_efficient_frontier(num_portfolios=5000, seed=42):
    """
    Simulate random portfolios and plot the Markowitz Efficient Frontier with colored scatter and efficient frontier curve.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(seed)

    # Example: 4 assets with random returns and covariances
    n_assets = 4
    mean_returns = np.array([0.12, 0.18, 0.15, 0.10])
    cov_matrix = np.array([
        [0.0064, 0.0008, 0.0011, 0.0],
        [0.0008, 0.0025, 0.0018, 0.0],
        [0.0011, 0.0018, 0.0100, 0.0],
        [0.0,    0.0,    0.0,    0.0050]
    ])

    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = portfolio_return / portfolio_vol
        results[0,i] = portfolio_vol
        results[1,i] = portfolio_return
        results[2,i] = sharpe
        weights_record.append(weights)

    # Find efficient frontier (max return for each volatility)
    sorted_indices = np.argsort(results[0])
    vols_sorted = results[0][sorted_indices]
    returns_sorted = results[1][sorted_indices]
    # For each unique volatility, keep the max return
    unique_vols, idx = np.unique(np.round(vols_sorted, 5), return_index=True)
    eff_frontier = np.maximum.accumulate(returns_sorted[idx])

    # Plot
    plt.figure(figsize=(10,7))
    sc = plt.scatter(results[0], results[1], c=results[2], cmap='plasma', s=5, alpha=0.5)
    plt.plot(unique_vols, eff_frontier, color='green', ls='--', lw=1.5)
    plt.colorbar(sc, label='Sharpe Ratio')
    plt.xlabel('Volatility', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.title('Efficient Frontier', fontsize=16)
    plt.grid(False)
    plt.tight_layout()
    plt.show()

# --- GBM Simulation and Plotting (screenshot style) ---
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import lognorm


# --- Improved GBM Simulation and Plotting (matches reference image) ---
def plot_gbm_paths(
    n_paths=60, n_steps=100, T=1.0, mu=0.2, sigma=0.3, x0=2.0, seed=42
):
    """
    Simulate and plot Geometric Brownian Motion paths with histogram and PDF of terminal values.
    Matches the style of the provided screenshot exactly.
    """
    np.random.seed(seed)
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)
    X = np.zeros((n_paths, n_steps + 1))
    X[:, 0] = x0
    for i in range(1, n_steps + 1):
        Z = np.random.randn(n_paths)
        X[:, i] = X[:, i - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    XT = X[:, -1]
    s = sigma * np.sqrt(T)
    scale = x0 * np.exp((mu - 0.5 * sigma ** 2) * T)
    mean_XT = x0 * np.exp(mu * T)

    # Plotting
    fig = plt.figure(figsize=(10, 7))
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.03)

    # Left: Simulated paths
    ax0 = fig.add_subplot(gs[0, 0])
    # Color gradient for paths
    colors = plt.cm.coolwarm(np.linspace(0, 1, n_paths))
    for i in range(n_paths):
        ax0.plot(t, X[i], color=colors[i], alpha=0.7, linewidth=1)
    # Expected value line
    ax0.plot(t, x0 * np.exp(mu * t), color='#1f77b4', ls='--', lw=2, label=r"$E[X_t]$")
    ax0.set_xlabel(r"$t$", fontsize=14)
    ax0.set_ylabel(r"$X(t)$", fontsize=14)
    ax0.set_title("Geometric Brownian Motion\nSimulated Paths $X_t, t \in [t_0, T]$", fontsize=15, pad=15)
    ax0.legend(loc='upper left', fontsize=12)
    ax0.grid(False)

    # Right: Histogram and PDF of terminal values
    ax1 = fig.add_subplot(gs[0, 1], sharey=ax0)
    # Histogram with color gradient
    n_bins = 15
    counts, bins, patches = ax1.hist(
        XT, bins=n_bins, density=True, orientation='horizontal',
        color='orange', alpha=0.5, edgecolor='none'
    )
    # Color the histogram bars
    for c, p in zip(plt.cm.coolwarm(np.linspace(0, 1, n_bins)), patches):
        plt.setp(p, 'facecolor', c)

    # PDF overlay
    x_vals = np.linspace(min(XT), max(XT), 200)
    pdf_vals = lognorm.pdf(x_vals, s=s, scale=scale)
    ax1.plot(pdf_vals, x_vals, color='orange', lw=2, label=r"$X_T$ pdf")
    # Expected value line
    ax1.axhline(mean_XT, color='#1f77b4', ls='--', lw=2, label=r"$E[X_T]$")

    # Remove axis clutter
    ax1.set_xlabel("")
    ax1.set_ylabel("")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title(r"$X_T$", fontsize=15, pad=15)
    ax1.legend(loc='upper right', fontsize=12)
    ax1.grid(False)

    # Layout and style tweaks
    for spine in ax1.spines.values():
        spine.set_visible(False)
    for spine in ax0.spines.values():
        spine.set_visible(False)

    plt.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12, wspace=0.03)
    plt.show()


if __name__ == "__main__":
    # plot_gbm_paths()
    plot_efficient_frontier()
import numpy as np
from collections import deque

class Order:
    def __init__(self, order_id, side, price, size, order_type, timestamp):
        self.order_id = order_id
        self.side = side  # 'buy' or 'sell'
        self.price = price
        self.size = size
        self.order_type = order_type  # 'limit' or 'market'
        self.timestamp = timestamp

class OrderBook:
    def __init__(self):
        self.bids = {}  # price: deque of orders
        self.asks = {}
        self.order_id_counter = 0
        self.trade_history = []

    def add_order(self, side, price, size, order_type, timestamp):
        order_id = self.order_id_counter
        self.order_id_counter += 1
        order = Order(order_id, side, price, size, order_type, timestamp)
        if order_type == 'limit':
            book = self.bids if side == 'buy' else self.asks
            if price not in book:
                book[price] = deque()
            book[price].append(order)
            return order_id
        else:
            trades = self.match_order(order)
            return trades

    def match_order(self, order):
        trades = []
        if order.side == 'buy':
            # Market buy: match with lowest ask
            while order.size > 0 and self.asks:
                best_ask = min(self.asks)
                ask_queue = self.asks[best_ask]
                while ask_queue and order.size > 0:
                    resting_order = ask_queue[0]
                    trade_size = min(order.size, resting_order.size)
                    trades.append((order.timestamp, 'buy', best_ask, trade_size))
                    self.trade_history.append((order.timestamp, 'buy', best_ask, trade_size))
                    order.size -= trade_size
                    resting_order.size -= trade_size
                    if resting_order.size == 0:
                        ask_queue.popleft()
                    if order.size == 0:
                        break
                if not ask_queue:
                    del self.asks[best_ask]
                if order.size == 0:
                    break
        else:
            # Market sell: match with highest bid
            while order.size > 0 and self.bids:
                best_bid = max(self.bids)
                bid_queue = self.bids[best_bid]
                while bid_queue and order.size > 0:
                    resting_order = bid_queue[0]
                    trade_size = min(order.size, resting_order.size)
                    trades.append((order.timestamp, 'sell', best_bid, trade_size))
                    self.trade_history.append((order.timestamp, 'sell', best_bid, trade_size))
                    order.size -= trade_size
                    resting_order.size -= trade_size
                    if resting_order.size == 0:
                        bid_queue.popleft()
                    if order.size == 0:
                        break
                if not bid_queue:
                    del self.bids[best_bid]
                if order.size == 0:
                    break
        return trades

    def get_best_bid(self):
        return max(self.bids) if self.bids else None

    def get_best_ask(self):
        return min(self.asks) if self.asks else None

    def get_spread(self):
        bid = self.get_best_bid()
        ask = self.get_best_ask()
        if bid is not None and ask is not None:
            return ask - bid
        return None

    def get_mid_price(self):
        bid = self.get_best_bid()
        ask = self.get_best_ask()
        if bid is not None and ask is not None:
            return (bid + ask) / 2
        return None

    def get_depth(self, depth=10):
        bid_prices = sorted(self.bids.keys(), reverse=True)[:depth]
        ask_prices = sorted(self.asks.keys())[:depth]
        bid_depth = [(p, sum(o.size for o in self.bids[p])) for p in bid_prices]
        ask_depth = [(p, sum(o.size for o in self.asks[p])) for p in ask_prices]
        return bid_depth, ask_depth

    def get_volume_imbalance(self):
        bid_vol = sum(sum(o.size for o in q) for q in self.bids.values())
        ask_vol = sum(sum(o.size for o in q) for q in self.asks.values())
        if bid_vol + ask_vol == 0:
            return 0
        return (bid_vol - ask_vol) / (bid_vol + ask_vol)

    def snapshot(self):
        return {
            'best_bid': self.get_best_bid(),
            'best_ask': self.get_best_ask(),
            'spread': self.get_spread(),
            'mid_price': self.get_mid_price(),
            'imbalance': self.get_volume_imbalance(),
        }

    def save_trade_history(self, filename):
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'side', 'price', 'size'])
            for trade in self.trade_history:
                writer.writerow(trade)
