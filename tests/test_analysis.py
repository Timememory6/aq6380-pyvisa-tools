import numpy as np

from aq6380_tools import dbm_to_mw, dbm_to_w, find_peak_near, sideband_wavelengths_nm


def test_dbm_conversions():
    assert dbm_to_mw(0.0) == 1.0
    assert dbm_to_w(30.0) == 1.0


def test_sideband_wavelengths_are_ordered():
    shorter, longer = sideband_wavelengths_nm(1550.0, 10.0)
    assert shorter < 1550.0
    assert longer > 1550.0


def test_find_peak_near_uses_strongest_point_in_window():
    wavelengths = np.asarray([1549.99, 1550.00, 1550.01])
    powers = np.asarray([-20.0, -10.0, -15.0])
    peak = find_peak_near(wavelengths, powers, 1550.0, 0.02)
    assert peak.found
    assert peak.wavelength_nm == 1550.0
    assert peak.power_dbm == -10.0
