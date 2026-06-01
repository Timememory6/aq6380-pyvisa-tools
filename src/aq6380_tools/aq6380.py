from __future__ import annotations

import csv
import re
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyvisa


def normalize_tcpip_resource(address: str) -> str:
    """Accept an IP address or VISA resource string and return a TCPIP resource."""
    text = str(address).strip()
    if "::" in text:
        return text
    match = re.search(r"(\d+\.\d+\.\d+\.\d+)", text)
    if not match:
        raise ValueError(f"Could not find an IPv4 address in {address!r}")
    return f"TCPIP0::{match.group(1)}::inst0::INSTR"


@dataclass(frozen=True)
class SweepConfig:
    center_nm: float
    span_nm: float
    points: int = 1001
    resolution_nm: float = 0.005
    sweep_time_s: float = 0.5
    sensitivity: str | None = None


@dataclass(frozen=True)
class Spectrum:
    wavelength_nm: np.ndarray
    power_dbm: np.ndarray

    def save_csv(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["wavelength_nm", "power_dbm"])
            writer.writerows(zip(self.wavelength_nm, self.power_dbm))
        return out


class AQ6380:
    """Small PyVISA wrapper for common Yokogawa AQ6380 sweep operations."""

    def __init__(self, address: str, timeout_ms: int = 60_000, retries: int = 3):
        self.resource_name = normalize_tcpip_resource(address)
        self.rm = pyvisa.ResourceManager()
        self.dev = self._open_with_retries(timeout_ms=timeout_ms, retries=retries)

    def _open_with_retries(self, timeout_ms: int, retries: int):
        last_error: Exception | None = None
        for attempt in range(1, int(retries) + 1):
            try:
                dev = self.rm.open_resource(self.resource_name)
                dev.timeout = int(timeout_ms)
                dev.chunk_size = 1024 * 1024
                dev.write_termination = "\n"
                dev.read_termination = "\n"
                return dev
            except pyvisa.errors.VisaIOError as exc:
                last_error = exc
                if attempt < retries:
                    time.sleep(1.0)
        raise RuntimeError(f"Failed to open VISA resource {self.resource_name}") from last_error

    def identify(self) -> str:
        return str(self.dev.query("*IDN?")).strip()

    def set_sensitivity(self, mode: str) -> None:
        self.dev.write(f":SENSe:SENSe {str(mode).strip().upper()}")

    def single_sweep(self, config: SweepConfig) -> Spectrum:
        d = self.dev
        if config.sensitivity:
            self.set_sensitivity(config.sensitivity)

        d.write("*CLS")
        d.write(f":SENS:WAV:CENT {config.center_nm:.6f}NM")
        d.write(f":SENS:WAV:SPAN {config.span_nm:.6f}NM")
        d.write(f":SENS:SWE:POIN {int(config.points)}")
        d.write(f":SENS:BAND:RES {config.resolution_nm:.4f}NM")
        d.write(f":SENS:SWE:TIME {config.sweep_time_s:.6f}")
        d.write(":FORMAT:DATA REAL,32")
        d.write(":INIT:SMOD SING")
        d.write(":INIT")
        d.query("*OPC?")

        old_read_termination = d.read_termination
        d.read_termination = None
        try:
            power_dbm = d.query_binary_values(
                f":TRACE:DATA:Y? TRA,1,{int(config.points)}",
                datatype="f",
                is_big_endian=False,
                header_fmt="ieee",
                expect_termination=False,
            )
        finally:
            d.read_termination = old_read_termination
            d.write(":FORMAT ASC")

        wavelength_nm = np.linspace(
            config.center_nm - 0.5 * config.span_nm,
            config.center_nm + 0.5 * config.span_nm,
            len(power_dbm),
            dtype=float,
        )
        return Spectrum(wavelength_nm=wavelength_nm, power_dbm=np.asarray(power_dbm, dtype=float))

    def close(self) -> None:
        self.dev.close()

    def __enter__(self) -> "AQ6380":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
