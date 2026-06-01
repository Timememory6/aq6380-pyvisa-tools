from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from aq6380_tools import AQ6380, SweepConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture one AQ6380 spectrum sweep and save it as CSV.")
    parser.add_argument("--address", required=True, help="IP address or VISA resource string.")
    parser.add_argument("--center-nm", type=float, required=True)
    parser.add_argument("--span-nm", type=float, required=True)
    parser.add_argument("--points", type=int, default=1001)
    parser.add_argument("--resolution-nm", type=float, default=0.005)
    parser.add_argument("--sweep-time-s", type=float, default=0.5)
    parser.add_argument("--sensitivity", default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output or Path(f"spectrum_{datetime.now():%Y%m%d_%H%M%S}.csv")
    config = SweepConfig(
        center_nm=args.center_nm,
        span_nm=args.span_nm,
        points=args.points,
        resolution_nm=args.resolution_nm,
        sweep_time_s=args.sweep_time_s,
        sensitivity=args.sensitivity,
    )

    with AQ6380(args.address) as osa:
        print(osa.identify())
        spectrum = osa.single_sweep(config)
    spectrum.save_csv(output)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
