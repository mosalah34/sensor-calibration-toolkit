import random
import pytest
from sensor_calib import *


def test_two_point_maps_reference_points():
    c = two_point(102, 0.0, 3010, 100.0)
    assert c.apply(102) == pytest.approx(0.0)
    assert c.apply(3010) == pytest.approx(100.0)


def test_invert_roundtrip():
    c = LinearCalibration(2.5, -4)
    assert c.invert(c.apply(7.0)) == pytest.approx(7.0)


def test_least_squares_recovers_line():
    rng = random.Random(1)
    raw = [i * 10 for i in range(50)]
    ref = [0.05 * x + 3 + rng.gauss(0, 0.01) for x in raw]
    c = least_squares(raw, ref)
    assert c.gain == pytest.approx(0.05, abs=1e-3)
    assert c.offset == pytest.approx(3, abs=0.05)


def test_bad_inputs():
    with pytest.raises(ValueError):
        two_point(5, 0, 5, 1)
    with pytest.raises(ValueError):
        least_squares([1, 1, 1], [1, 2, 3])
    with pytest.raises(ValueError):
        least_squares([1], [1])


def test_median_rejects_spike_average_does_not():
    med, avg = MovingMedian(5), MovingAverage(5)
    for v in [10, 10, 10, 10]:
        med.update(v); avg.update(v)
    assert med.update(100) == 10
    assert avg.update(100) > 20


def test_deadband_holds_then_moves():
    d = Deadband(0.5)
    assert d.update(20.0) == 20.0
    assert d.update(20.3) == 20.0
    assert d.update(20.6) == 20.6
