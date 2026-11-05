import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # headless: no display needed, and plt.show() becomes a no-op

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
