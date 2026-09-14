import math
import numpy as np
from scipy.stats import circvar

# , axis=None, nan_policy='propagate'
# print(f"{circvar(np.array([1, 1, 1]), high=np.pi, low=-np.pi):.6f}")

class StreamingCircVar:
    def __init__(self, low=0, high=2 * math.pi):
        """
        low, high: The bounds of your circular data (e.g., 0 to 360, or 0 to 2*pi).
        Matches the default behavior of scipy.stats.circvar.
        """
        self.low = low
        self.high = high
        self.bounds_range = high - low
        
        # Internal state variables
        self.n = 0
        self.sum_sin = 0.0
        self.sum_cos = 0.0

    def update(self, x):
        """Add a single new data point and return the current circular variance."""
        # 1. Map input to radians [0, 2*pi] matching scipy's internal normalization
        t = (x - self.low) * (2.0 * math.pi) / self.bounds_range
        
        # 2. Update streaming state
        self.n += 1
        self.sum_sin += math.sin(t)
        self.sum_cos += math.cos(t)
        
        # 3. Calculate circular variance
        return self.get_variance()

    def get_variance(self):
        if self.n == 0:
            return float('nan')
        
        # Mean resultant vector length (R_bar)
        r_bar = math.sqrt(self.sum_sin**2 + self.sum_cos**2) / self.n
        
        # Guarantee floating point accuracy bounds
        r_bar = min(r_bar, 1.0)
        
        # Circular variance formula used by SciPy
        return 1.0 - r_bar
