# aq6380-pyvisa-tools

Python/PyVISA utilities for controlling Yokogawa AQ6380 optical spectrum
analyzers and saving reproducible spectrum data.

This project is intentionally focused on general instrument control and basic
optical-spectrum processing. It does not include unpublished research logic,
private measurement data, or lab-specific analysis workflows.

## Features

- Connect to a Yokogawa AQ6380 over VISA/TCPIP
- Run a single wavelength sweep
- Read binary trace data into NumPy arrays
- Save spectra to CSV
- Find peaks near target wavelengths
- Convert dBm to mW/W
- Calculate first-order sideband wavelength estimates

## Install

Create a Python environment, then install the package in editable mode:

```powershell
git clone https://github.com/Timememory6/aq6380-pyvisa-tools.git
cd aq6380-pyvisa-tools
python -m pip install -e .
```

PyVISA also needs a VISA backend, such as NI-VISA, Keysight IO Libraries, or a
compatible pyvisa-py setup.

## Quick Start

Run a basic sweep:

```powershell
python .\examples\aq6380_basic_sweep.py --address TCPIP0::192.168.0.10::inst0::INSTR --center-nm 1550 --span-nm 1.0
```

The script writes a CSV file with:

```text
wavelength_nm,power_dbm
```

## Peak Search Example

```powershell
python .\examples\peak_search_example.py --csv spectrum.csv --target-nm 1550.0
```

## Safety Notes

- Check instrument addresses before running examples.
- Start with conservative sweep settings.
- This package sends SCPI commands to connected instruments.
- Do not publish measurement data that contains private, proprietary, or
  unpublished research information.

## Project Scope

Good fits for this repository:

- AQ6380 connection examples
- Generic OSA sweep capture
- Spectrum CSV export
- Simple peak detection
- dBm/mW/W conversion helpers
- Documentation of common SCPI commands

Out of scope:

- Private lab automation workflows
- Unpublished experiment-specific algorithms
- Raw internal measurement datasets
- Credentials, IP maps, or lab network details

## License

MIT License. See [LICENSE](LICENSE).

## Contributing

Issues and pull requests are welcome for general AQ6380 control examples,
documentation improvements, and reusable spectrum-processing utilities. See
[CONTRIBUTING.md](CONTRIBUTING.md).
