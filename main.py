import matplotlib.pyplot as plt
from simulator import Simulator
import numpy as np

if __name__ == '__main__':
    sim = Simulator(T=500, dt=1, seed=42)
    sim.run()
    prices = sim.get_prices()
    trades = sim.get_trades()
    snapshots = sim.get_snapshots()

    # 3D FFT Visualization of Mid Price (Line Plot Style)
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.cm as cm
    N = len(prices)
    window_size = 64
    stride = 4
    fft_matrix = []
    times = []
    for start in range(0, N - window_size, stride):
        window = prices[start:start+window_size]
        if None in window:
            continue
        # Mid prices sit near ~100, so the DC (bin 0) magnitude dwarfs every
        # other bin by ~2-3 orders of magnitude and swamps the whole plot
        # into a flat wall. Demean each window first so the plotted surface
        # shows the actual price fluctuations the FFT is meant to reveal.
        window_demeaned = np.asarray(window) - np.mean(window)
        fft_vals = np.abs(np.fft.fft(window_demeaned))[:window_size//2]
        fft_matrix.append(fft_vals)
        times.append(start)
    fft_matrix = np.array(fft_matrix)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = cm.rainbow(np.linspace(0, 1, len(fft_matrix)))
    freq_bins = np.arange(fft_matrix.shape[1])
    for i, (fft_vals, t, color) in enumerate(zip(fft_matrix, times, colors)):
        ax.plot(freq_bins, [t]*len(freq_bins), fft_vals, color=color, linewidth=1)
    ax.set_title('Fast Fourier Transform (FFT) of Mid Price Over Time')
    ax.set_xlabel('Frequency Bin')
    ax.set_ylabel('Time Index')
    ax.set_zlabel('Amplitude')
    plt.tight_layout()
    plt.show()
