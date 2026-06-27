# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.5] - 2026-06-27
### Changed
- Enabled mypy strict mode for comprehensive type checking.

## [0.2.4] - 2026-06-16
### Added
- Python 3.10–3.14 classifier and CI support.
- Dependabot for automated updates.
### Changed
- Standardized CI and publish workflows; switched to `uv publish`.
- Bumped minimum dev dependency floors (pytest ≥ 9.1.0, ruff ≥ 0.15.17, mypy ≥ 2.1.0).

## [0.2.3] - 2026-05-22
### Added
- Six new date input formats to `ThaDT`.
### Fixed
- Silent year-1900 bug in `ThaDT` when parsing two-digit year strings.

## [0.2.2] - 2026-05-22
### Added
- DD-Mon format auto-detection to `ThaDT` (e.g., `15-Jun`).

## [0.2.1] - 2026-05-17
### Changed
- Renamed `DictUtils` → `ThaDict`, `ListUtils` → `ThaList`, `TypeUtils` → `ThaType`.

## [0.2.0] - 2026-05-17
### Added
- `ThaStr` for string utilities.
- `ThaNum` for numeric utilities.
- `ThaDT` for date/time parsing and formatting.
- Row-level helper methods to `ThaDict` and `ThaType`.

## [0.1.1] - 2026-05-17
### Added
- `ListUtils`, `DictUtils`, and `TypeUtils` helper classes.

## [0.1.0] - 2026-05-17
### Added
- Initial release with `ThaStr` and `ThaNum` utilities.
