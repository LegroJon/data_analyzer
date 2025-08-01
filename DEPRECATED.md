# DEPRECATED FILES

The following files have been deprecated and replaced with the new modular structure:

## Deprecated Files:
- `parse_pdf_tasks.py` → Replaced by `src/task_parser.py`
- `parse_tasks_v1.py` → Replaced by `src/task_parser.py`

## Migration Guide:

### Old Usage:
```python
# Old way
python parse_tasks_v1.py
```

### New Usage:
```python
# New way
python src/task_parser.py

# Or using the API
from src.task_parser import TaskParser
parser = TaskParser()
tasks = parser.parse_file("input.txt", "original")
parser.save_to_csv(tasks, "output.csv", "original")
```

## Improvements in New Version:
- Better error handling
- Comprehensive logging
- Type hints and documentation
- Unit tests
- Configurable patterns
- More robust duplicate removal
- Cleaner code structure
- Better performance

## Files Moved:
- Input files: `data/input/`
- Output files: `data/output/`
- Documentation: `docs/`
- Configuration: `config/`

Please update any scripts or workflows to use the new structure.
