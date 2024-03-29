# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Deprecated

- `get_location_weather` method will be deprecated in version 1.0.0.
  
- `get_zip_weather` method will be deprecated in version 1.0.0.

- `compact_mode` will be deprecated in version 1.0.0.

## [0.3.3] - 2024-03-22

### Added

- Logging.

## [0.3.2] - 2024-03-20

### Added

- `current_weather` method to enable weather requests based on either
  location name or zip/postal code.

### Deprecated

- `get_location_weather` method will be deprecated in version 1.0.0.
  
- `get_zip_weather` method will be deprecated in version 1.0.0.

- `compact_mode` will be deprecated in version 1.0.0.

## [0.3.1] - 2024-03-19

### Security

- Improved data handling by introducing locks for enhanced thread safety.

## [0.3.0] - 2024-03-16

### Added

- Weather requests by zip/postal code.

## [0.2.3] - 2024-03-14

### Fixed

- Fixed errors that occurred when changing the token of the Client instance.

## [0.2.2] - 2024-03-11

### Changed 

- Minor changes.

## [0.2.1] - 2024-03-11

### Changed 

- Minor changes.

## [0.2.0] - 2024-03-11

### Added

- JSON_Processor (to get weather in compact mode).

## [0.1.1] - 2024-03-11

### Changed 

- Minor changes.

## [0.1.0] - 2024-03-10

- Init project.
