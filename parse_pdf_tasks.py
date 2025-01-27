import csv
import re
import os
import time

# Function to parse tasks using regex patterns
def parse_tasks(text, patterns):
    parsed_data = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            parsed_data.append([
                match.group('step') if match.group('step') else '',  # Handle missing Step Numbers
                match.group('task'),
                match.group('title'),
                match.group('proponent'),
                match.group('status')
            ])
    return parsed_data

# Remove duplicate entries
def remove_duplicates(data):
    unique_data = []
    seen = set()
    for row in data:
        row_tuple = tuple(row)  # Convert list to tuple for set comparison
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    return unique_data

# Patterns for SCT, SIT, and SD
patterns = [
    r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)',
    r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]

# Function to get file input from the user
def get_file_input():
    file_path = input("Enter the path to the text file (.txt): ").strip()

    if not os.path.isfile(file_path):
        print("Error: File not found. Please provide a valid file path.")
        exit()

    return file_path

# Main Program Execution
if __name__ == "__main__":
    input_file = get_file_input()

    # Extract text from the text file
    with open(input_file, 'r') as file:
        text = file.read()

    # Parse the tasks
    parsed_tasks = parse_tasks(text, patterns)

    # Remove duplicates
    unique_tasks = remove_duplicates(parsed_tasks)

    # Generate unique output file name
    output_file = f"tasks_output_{int(time.time())}.csv"

    # Write parsed data to CSV file (without headers)
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(unique_tasks)

    print(f"Data has been successfully saved to {output_file}")
