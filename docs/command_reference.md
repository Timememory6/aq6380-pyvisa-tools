# Command Reference

This page lists the SCPI commands used by the examples. Check the Yokogawa
AQ6380 programming manual for complete details.

## Sweep Setup

```text
*CLS
:SENS:WAV:CENT <value>NM
:SENS:WAV:SPAN <value>NM
:SENS:SWE:POIN <points>
:SENS:BAND:RES <value>NM
:SENS:SWE:TIME <seconds>
```

## Single Sweep

```text
:INIT:SMOD SING
:INIT
*OPC?
```

## Trace Readout

```text
:FORMAT:DATA REAL,32
:TRACE:DATA:Y? TRA,1,<points>
:FORMAT ASC
```

## Sensitivity

```text
:SENSe:SENSe <mode>
```

Common modes depend on instrument configuration. Confirm valid values on your
instrument before automating measurements.
