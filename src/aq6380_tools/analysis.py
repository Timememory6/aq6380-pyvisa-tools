from __future__ import annotations

from dataclasses import dataclass

import numpy as np

LIGHT_SPEED_M_PER_S = 299_792_458.0


@dataclass(frozen=True)
class Peak:
    wavelength_nm: float
    power_dbm: float


@dataclass(frozen=True)
class MatchedPeak:
    target_nm: float
    wavelength_nm: float
    power_dbm: float
    offset_nm: float
    found: bool


def dbm_to_mw(dbm: float) -> float:
    return 10 ** (float(dbm) / 10.0)


def dbm_to_w(dbm: float) -> float:
    return dbm_to_mw(dbm) / 1000.0


def sideband_wavelengths_nm(carrier_nm: float, rf_ghz: float, order: int = 1) -> tuple[float, float]:
    """Return shorter and longer wavelength sidebands around a carrier."""
    carrier_m = float(carrier_nm) * 1e-9
    delta_m = (carrier_m**2 / LIGHT_SPEED_M_PER_S) * (float(rf_ghz) * 1e9) * int(order)
    return (carrier_m - delta_m) * 1e9, (carrier_m + delta_m) * 1e9


def find_peak_near(
    wavelengths_nm: np.ndarray,
    powers_dbm: np.ndarray,
    target_nm: float,
    half_window_nm: float,
) -> MatchedPeak:
    """Find the strongest trace point within a window around a target wavelength."""
    if len(wavelengths_nm) != len(powers_dbm):
        raise ValueError("wavelengths_nm and powers_dbm must have the same length")
    if len(wavelengths_nm) == 0:
        return MatchedPeak(target_nm, float("nan"), float("nan"), float("nan"), False)

    offsets = np.abs(np.asarray(wavelengths_nm, dtype=float) - float(target_nm))
    in_window = np.where(offsets <= float(half_window_nm))[0]
    if len(in_window) == 0:
        idx = int(np.argmin(offsets))
        found = False
    else:
        idx = int(in_window[np.argmax(np.asarray(powers_dbm, dtype=float)[in_window])])
        found = True

    wavelength_nm = float(wavelengths_nm[idx])
    return MatchedPeak(
        target_nm=float(target_nm),
        wavelength_nm=wavelength_nm,
        power_dbm=float(powers_dbm[idx]),
        offset_nm=wavelength_nm - float(target_nm),
        found=found,
    )
