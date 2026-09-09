# ha-smart-ion

Smart iON Modbus project scaffold.

This repository is organized into three deliverables:

1. `device-library/` — a standalone Modbus device library generated from `docs/smart-ion-registers.yaml`.
2. `homeassistant-core/` — a Home Assistant core-style integration that consumes the device library.
3. `custom-integration/` — a vendorized custom integration for HACS testing.

## Source of truth

- `docs/smart-ion-registers.yaml`

## Current supported device map

- 8 coil switches at addresses `0x000` through `0x007`
- 1 holding-register sensor at address `0x100`

## Next steps

- Expand the register map from the PDF in `docs/`.
- Generate the standalone device library models and helpers.
- Add the Home Assistant integration packages and CI.

