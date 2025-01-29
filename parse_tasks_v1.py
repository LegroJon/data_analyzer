import csv
import re
import os

# Define your regex patterns here
PATTERNS = {
    'original': [
        r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)',
        # r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
    ],
    'drill': [
        r'^\s*(?:\d+\.\s+)?(?P<step>[\w-]+)\s+(?P<status>\S+)\s+(?P<title>.*)'
    ]

}

def parse_original_tasks(text, patterns):
    """Parses text using regex for the 'original' format."""
    parsed_data = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            parsed_data.append([
                match.group('step') if match.group('step') else '',
                match.groupdict().get('task', ''),
                match.groupdict().get('title', ''),
                match.groupdict().get('proponent', ''),
                match.groupdict().get('status', '')
            ])
    return parsed_data

def parse_drill_tasks(text, patterns):
    parsed_data = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.MULTILINE):
            parsed_data.append([
                match.group('step') or '',
                match.group('status') or '',
                match.group('title') or ''
            ])
    return parsed_data


def remove_duplicates(data):
    """Removes exact duplicate rows from a list of lists."""
    unique_data = []
    seen = set()
    for row in data:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    return unique_data

def main():
    # 1. Ask for the file path
    input_file = input("Enter the path to your text file (.txt): ").strip()
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # 2. Ask for the pattern type
    pattern_choice = input("Enter the pattern type (1 for 'original', 2 for 'drill'): ").strip()
    if pattern_choice == '1':
        pattern_type = 'original'
    elif pattern_choice == '2':
        pattern_type = 'drill'
    else:
        print("Error: Invalid pattern type. Choose either '1' for 'original' or '2' for 'drill'.")
        return

    # Read text
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Parse according to the chosen pattern
    if pattern_type == 'original':
        parsed_tasks = parse_original_tasks(text, PATTERNS[pattern_type])
    else:  # 'drill'
        parsed_tasks = parse_drill_tasks(text, PATTERNS[pattern_type])

    # Remove duplicates
    unique_tasks = remove_duplicates(parsed_tasks)

    # Generate a CSV filename
    output_file = os.path.splitext(input_file)[0] + "_output.csv"

    # Write parsed tasks to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(unique_tasks)

    print(f"Data successfully saved to '{output_file}'.")

if __name__ == "__main__":
    main()

