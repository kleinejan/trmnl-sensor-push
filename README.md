# TRMNL Entity Push Integration

A Home Assistant custom integration that pushes sensor data to TRMNL devices with grouped JSON payloads.

## Features

- **Custom Sensor Groups**: Organize sensors using Home Assistant labels (e.g., "temperatures", "garbage", "humidity")
- **Grouped JSON Output**: Creates structured payloads like `{"temperatures": [{"name": "toilet", "value": "25°C"}]}`
- **2KB Payload Management**: Automatically handles TRMNL's payload size limits
- **Minimal Data Format**: Sends only essential data (name + value) for efficiency
- **Flexible Configuration**: Multi-select sensor groups with custom values

## Installation

### HACS (Recommended)
1. Add this repository to HACS as a custom repository
2. Install "TRMNL Entity Push" from HACS
3. Restart Home Assistant

### Manual Installation
1. Copy the `trmnl_sensor_push` folder to `custom_components/`
2. Restart Home Assistant

## Configuration

1. **Create Labels**: Go to Settings → Labels and create groups like "temperatures", "garbage"
2. **Label Entities**: Assign labels to your sensors
3. **Add Integration**: Settings → Devices & Services → Add Integration → "TRMNL Entity Push"
4. **Configure**: Enter your TRMNL webhook URL and select sensor groups

## Example Output

```json
{
  "temperatures": [
    {"name": "Living Room", "value": "23.5°C"},
    {"name": "Bedroom", "value": "22°C"}
  ],
  "garbage": [
    {"name": "Garbage Day", "value": "2 days"}
  ]
}
```

## Requirements

- Home Assistant 2023.1.0+
- TRMNL webhook URL
- Sensors labeled with appropriate groups

## License

MIT License