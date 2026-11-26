"""Streaming filters with an update(value) -> value interface."""
from __future__ import annotations

from collections import deque
from statistics import median


class MovingAverage:
    def __init__(self, size: int = 5):
        if size < 1:
            raise ValueError("size must be >= 1")
        self.buf = deque(maxlen=size)

    def update(self, value: float) -> float:
        self.buf.append(value)
        return sum(self.buf) / len(self.buf)


class MovingMedian:
    """Rejects single-sample spikes better than an average does."""

    def __init__(self, size: int = 5):
        if size < 1:
            raise ValueError("size must be >= 1")
        self.buf = deque(maxlen=size)

    def update(self, value: float) -> float:
        self.buf.append(value)
        return median(self.buf)


class Deadband:
    """Holds the last output until the input moves by more than `band`.

    Stops a displayed value from flickering on noise.
    """

    def __init__(self, band: float):
        if band < 0:
            raise ValueError("band must be >= 0")
        self.band = band
        self.out = None

    def update(self, value: float) -> float:
        if self.out is None or abs(value - self.out) > self.band:
            self.out = value
        return self.out
