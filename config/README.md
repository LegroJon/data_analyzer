# Configuration Directory

This directory contains configuration files and settings for the data analyzer.

## Files:

### `settings.ini`
- Pattern definitions for different data formats
- Default configuration values
- Logging and output settings
- File size and validation limits

## Configuration Sections:

### [patterns]
- **original_patterns**: Regex patterns for military task format
- **drill_patterns**: Regex patterns for battle drill format

### [settings]
- **default_encoding**: File encoding (utf-8)
- **max_file_size_mb**: Maximum input file size
- **default_format**: Default output format
- **include_headers**: CSV header configuration

### [logging]
- **level**: Logging verbosity (INFO, DEBUG, WARNING, ERROR)
- **format**: Log message format string

### [output]
- **output_dir**: Default output directory path
- **input_dir**: Default input directory path
- **timestamp_format**: Format for timestamp in filenames

## Usage:

Configuration is automatically loaded by the parser. To customize:

1. Edit `settings.ini` with your preferred values
2. Restart the parser application
3. Settings will be applied automatically

## Notes:
- Changes take effect immediately
- Invalid settings will use defaults
- Comments in INI file start with `#`
