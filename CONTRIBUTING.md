# Contributing

Thanks for your interest in improving aq6380-pyvisa-tools.

This repository is focused on reusable, public instrument-control utilities for
Yokogawa AQ6380 optical spectrum analyzers. Contributions should avoid private
lab details and unpublished experiment-specific analysis logic.

## Good Contributions

- AQ6380 connection and sweep examples
- Clear documentation for common SCPI workflows
- Generic spectrum CSV import/export utilities
- Basic optical peak detection helpers
- Tests for pure-Python analysis functions
- Safer error handling around VISA operations

## Not Suitable for This Repository

- Private instrument addresses or lab network maps
- Proprietary measurement data
- Unpublished research workflows
- Credentials, tokens, or personal information
- Large generated datasets

## Development

Install in editable mode:

```powershell
python -m pip install -e .[dev]
```

Run tests:

```powershell
python -m pytest
```

Run a syntax check:

```powershell
python -m compileall src examples tests
```

## Pull Request Checklist

- Keep examples generic and reproducible.
- Do not include private measurement data.
- Add or update tests for analysis helpers.
- Update README or docs when behavior changes.
