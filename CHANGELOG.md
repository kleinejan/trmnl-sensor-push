# Changelog

All notable changes to the TRMNL Entity Push integration will be documented in this file.

## [0.3.0] - 2025-06-24

### Added
- Grouped JSON payload structure organizing sensors by category
- Multi-group sensor selection with Home Assistant labels
- Group-aware payload size management for 2KB limits
- Custom sensor group support (temperatures, garbage, humidity, etc.)
- Automatic payload truncation while preserving group structure

### Changed
- Payload format now groups entities: `{"temperatures": [{"name": "toilet", "value": "25°C"}]}`
- Configuration flow supports multiple label selection with custom values
- Improved logging with group-specific information

### Maintained
- Backward compatibility with "TRMNL" label
- 30-minute update intervals
- Minimal payload format (name + value only)
- 2KB payload limit compliance

## [0.2.0] - 2025-06-24

### Added
- Custom sensor group configuration via Home Assistant labels
- Multi-select dropdown for sensor group selection
- Enhanced configuration validation
- Options flow for reconfiguration

### Changed
- Replaced single "TRMNL" label with configurable sensor groups
- Updated payload structure to include group metadata

## [0.1.0] - 2025-06-24

### Added
- Initial TRMNL Entity Push integration
- Basic webhook functionality
- Entity filtering by "TRMNL" label
- 30-minute update intervals
- Basic payload size management