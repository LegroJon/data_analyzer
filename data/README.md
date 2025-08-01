# Data Directory

This directory contains all input and output data files organized by type and purpose.

## Structure:

### `/input/` - Input Text Files
- Contains text files to be parsed
- Supported formats: `.txt`, `.text`
- Place your source data files here

### `/output/` - Generated CSV Files
- **`/demo/`** - Output files from demonstration runs
- **`/legacy/`** - Historical output files from previous versions
- Main directory for new parser output

### `/samples/` - Sample Data Files
- Example input files for testing and demonstration
- `sample_task_data_1.txt` - Original format examples
- `sample_task_data_2.txt` - Additional sample data

## Usage:

1. **Add input files** to `/input/` directory
2. **Run parser** using scripts or directly
3. **Find results** in `/output/` directory
4. **Reference samples** in `/samples/` for format examples

## File Naming Convention:

### Input Files:
- Descriptive names: `task_data_YYYY-MM-DD.txt`
- Format indicators: `original_format.txt`, `drill_format.txt`

### Output Files:
- Auto-generated: `[input_name]_parsed_[timestamp].csv`
- Demo files: `[input_name]_demo_[timestamp].csv`

## Notes:
- Files are automatically organized by the parser
- Legacy files are preserved in `/legacy/` subdirectory
- Demo outputs are isolated in `/demo/` subdirectory
