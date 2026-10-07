"""Small statistics helpers: mean/median with confidence intervals."""
import numpy as np
from scipy import stats as _ss


def mean_ci(x, conf=0.95):
    """Mean and two-sided CI (t-distribution). Returns (mean, lo, hi)."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    m = float(x.mean())
    if n == 1:
        return m, m, m
    se = float(x.std(ddof=1) / np.sqrt(n))
    h = se * _ss.t.ppf((1 + conf) / 2.0, n - 1)
    return m, m - h, m + h


def median_iqr(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    return float(np.median(x)), float(np.percentile(x, 25)), float(np.percentile(x, 75))


def fmt(m, lo, hi, digits=2):
    return f"{m:.{digits}f} [{lo:.{digits}f}, {hi:.{digits}f}]"
