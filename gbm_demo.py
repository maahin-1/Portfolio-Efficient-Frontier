import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
n_paths = 50
T = 1.0
N = 252
mu = 0.2
sigma = 0.4
S0 = 2.0

dt = T / N
t = np.linspace(0, T, N+1)

# Simulate GBM paths
paths = np.zeros((n_paths, N+1))
paths[:, 0] = S0
for i in range(n_paths):
    for j in range(1, N+1):
        z = np.random.normal()
        paths[i, j] = paths[i, j-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

# Final values
X_T = paths[:, -1]

# Plot
fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.05)
ax0 = fig.add_subplot(gs[0])
ax1 = fig.add_subplot(gs[1], sharey=ax0)

# Path plot
for i in range(n_paths):
    ax0.plot(t, paths[i], color=plt.cm.coolwarm((paths[i,-1]-min(X_T))/(max(X_T)-min(X_T))), alpha=0.7)
ax0.set_xlabel(r'$t$')
ax0.set_ylabel(r'$X(t)$')
ax0.set_title('Geometric Brownian Motion\nSimulated Paths $X_t, t \in [t_0, T]$')

# Histogram and PDF
bins = np.linspace(min(X_T), max(X_T), 20)
ax1.hist(X_T, bins=bins, orientation='horizontal', color='orange', alpha=0.6, density=True, label=r'$X_T$ pdf')
mean_XT = np.mean(X_T)
ax1.axhline(mean_XT, color='dodgerblue', linestyle='--', label=r'$\mathbb{E}[X_T]$')

# Theoretical PDF
mu_T = np.log(S0) + (mu - 0.5 * sigma**2) * T
sigma_T = sigma * np.sqrt(T)
x = np.linspace(min(X_T), max(X_T), 200)
pdf = (1/(x*sigma_T*np.sqrt(2*np.pi))) * np.exp(-(np.log(x)-mu_T)**2/(2*sigma_T**2))
ax1.plot(pdf, x, color='orange', lw=2)

ax1.set_xlabel('')
ax1.set_ylabel('')
ax1.set_xticks([])
ax1.set_title(r'$X_T$')
ax1.legend(loc='upper left')
plt.tight_layout()
plt.show()
