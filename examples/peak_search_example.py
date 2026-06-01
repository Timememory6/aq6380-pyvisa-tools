from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from aq6380_tools import find_peak_near


def load_spectrum_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    wavelengths: list[float] = []
    powers: list[float] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wavelengths.append(float(row["wavelength_nm"]))
            powers.append(float(row["power_dbm"]))
    return np.asarray(wavelengths), np.asarray(powers)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find the strongest CSV trace point near a target wavelength.")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--target-nm", type=float, required=True)
    parser.add_argument("--half-window-nm", type=float, default=0.025)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    wavelengths_nm, powers_dbm = load_spectrum_csv(args.csv)
    peak = find_peak_near(wavelengths_nm, powers_dbm, args.target_nm, args.half_window_nm)
    status = "found" if peak.found else "nearest"
    print(
        f"{status}: target={peak.target_nm:.6f} nm "
        f"peak={peak.wavelength_nm:.6f} nm "
        f"offset={peak.offset_nm:+.6f} nm "
        f"power={peak.power_dbm:.3f} dBm"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
