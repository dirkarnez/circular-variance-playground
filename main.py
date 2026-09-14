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
        t = x * ((2.0 * math.pi) / self.bounds_range)
        
        # 2. Update streaming state
        self.n += 1
        self.sum_sin += math.sin(t)
        self.sum_cos += math.cos(t)
        
        # 3. Calculate circular variance
        return self.get_variance()

    def get_variance(self):
        if self.n == 0:
            return float('nan')

        # def circvar()
        #     period = high - low
        #     scaled_samples = samples * ((2.0 * pi) / period)
        #     sin_samp = xp.sin(scaled_samples)
        #     cos_samp = xp.cos(scaled_samples)

        #     sin_mean = xp.mean(sin_samp, axis=axis)
        #     cos_mean = xp.mean(cos_samp, axis=axis)
        #     hypotenuse = (sin_mean**2. + cos_mean**2.)**0.5
        #     # hypotenuse can go slightly above 1 due to rounding errors
        #     R = xp.clip(hypotenuse, max=1.)
        #     res = 1. - R
        
        # 1. 100% 對齊 SciPy 的平均值做法
        sin_mean = self.sum_sin / self.n
        cos_mean = self.sum_cos / self.n
        
        # 2. 100% 對齊 SciPy 的開根號寫法 (不用 math.sqrt 或 math.hypot)
        hypotenuse = (sin_mean**2.0 + cos_mean**2.0)**0.5
        
        # 3. 100% 對齊 SciPy 的 xp.clip(..., max=1.)
        # 雖然你的 min(r_bar, 1.0) 邏輯相同，但這樣寫與源碼語意完全一致
        R = min(hypotenuse, 1.0)
        
        return 1.0 - R

def main():
    s=StreamingCircVar(high=np.pi, low=-np.pi)
    print(f"{s.update(1)}---vs----{circvar(np.array([1]), high=np.pi, low=-np.pi)}")
    print(f"{s.update(1)}---vs----{circvar(np.array([1, 1]), high=np.pi, low=-np.pi)}")
    print(f"{s.update(1)}---vs----{circvar(np.array([1, 1, 1]), high=np.pi, low=-np.pi)}")

if __name__ == "__main__":
    main()
