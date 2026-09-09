# Smart iOn CS-8 device library
The library validates duplicate `unique_id` values and loads the current register map from the YAML source.

## Validation

- 1 sensor entity for holding register `0x100`
- 8 switch entities for coils `0x000` through `0x007`

## Supported entities

- `../docs/smart-ion-registers.yaml`

## Source of truth

- CLI inspection entry point
- device registry helper
- YAML-backed register loader
- typed connection and register models

## Contents

Standalone Modbus device library for the **Smart iOn CS-8**.


