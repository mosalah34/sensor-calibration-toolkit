"""Linear calibration: corrected = gain * raw + offset."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinearCalibration:
    gain: float = 1.0
    offset: float = 0.0

    def apply(self, raw: float) -> float:
        return self.gain * raw + self.offset

    def invert(self, corrected: float) -> float:
        if self.gain == 0:
            raise ZeroDivisionError("gain is zero, cannot invert")
        return (corrected - self.offset) / self.gain


def two_point(raw_low: float, ref_low: float, raw_high: float, ref_high: float) -> LinearCalibration:
    """Calibrate from two (raw, reference) pairs, e.g. ice water and boiling water."""
    if raw_high == raw_low:
        raise ValueError("raw points must differ")
    gain = (ref_high - ref_low) / (raw_high - raw_low)
    return LinearCalibration(gain, ref_low - gain * raw_low)


def least_squares(raw: list[float], ref: list[float]) -> LinearCalibration:
    """Fit gain and offset to many (raw, reference) pairs."""
    n = len(raw)
    if n != len(ref) or n < 2:
        raise ValueError("need at least two matching pairs")
    mx, my = sum(raw) / n, sum(ref) / n
    sxx = sum((x - mx) ** 2 for x in raw)
    if sxx == 0:
        raise ValueError("raw values must not all be equal")
    gain = sum((x - mx) * (y - my) for x, y in zip(raw, ref)) / sxx
    return LinearCalibration(gain, my - gain * mx)
