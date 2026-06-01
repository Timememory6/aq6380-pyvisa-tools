# Security Policy

## Reporting Security Issues

Please do not open a public issue for security-sensitive reports. Use GitHub's
private vulnerability reporting feature if it is available for this repository,
or contact the maintainer through GitHub.

## Sensitive Data

Do not commit:

- API keys or tokens
- private instrument IP address maps
- internal lab network details
- unpublished measurement data
- personal information

## Instrument Safety

This project sends SCPI commands to connected instruments. Review command
parameters before running examples against real hardware.
