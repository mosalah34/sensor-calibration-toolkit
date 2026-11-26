# sensor-calibration-toolkit

Dependency-free Python helpers for turning raw sensor readings (for example ADC counts from an ESP32) into trustworthy values.

## What is inside

| Piece | Purpose |
|---|---|
| `two_point(raw_low, ref_low, raw_high, ref_high)` | Gain and offset from two known reference points |
| `least_squares(raw, ref)` | Best-fit gain and offset from many reference pairs |
| `LinearCalibration` | `apply(raw)` and `invert(corrected)` |
| `MovingMedian` | Removes single-sample spikes |
| `MovingAverage` | Smooths noise |
| `Deadband` | Stops a displayed value flickering on tiny changes |

## Example

```python
from sensor_calib import two_point, MovingMedian

# raw ADC readings taken while the probe sat in ice water (0 C) and a 100 C reference
cal = two_point(raw_low=412, ref_low=0.0, raw_high=3010, ref_high=100.0)
filt = MovingMedian(5)

for raw in [1600, 1602, 3999, 1601, 1603]:   # 3999 is a glitch
    print(round(cal.apply(filt.update(raw)), 2))
```

The numbers above are made-up example values, not measurements from a real sensor.

## Tests

```bash
pip install pytest
pytest
```

The tests check the maths against known lines, error handling, and that the median filter rejects a spike while the average does not. The only noise used is a seeded random generator.

## Limits

- Linear calibration only. Sensors with a strong curve need a lookup table or polynomial.
- Not tested on real hardware. Calibrate against your own references.
- Python 3.9 or newer. To use on a microcontroller, port the same logic to MicroPython or C.
