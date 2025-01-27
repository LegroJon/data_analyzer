import csv
import re
import os

# Function to parse tasks using regex patterns
def parse_tasks(text, patterns):
    parsed_data = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            if "Battle Drill" in match.group('title'):
                parsed_data.append([
                    match.group('step') if match.group('step') else '',
                    match.group('task'),
                    match.group('title'),
                    "Battle Drill",  # Drill Type
                    match.group('proponent'),
                    match.group('status')
                ])
            else:
                parsed_data.append([
                    match.group('step') if match.group('step') else '',
                    match.group('task'),
                    match.group('title'),
                    match.group('proponent'),
                    match.group('status')
                ])
    return parsed_data

# Function to remove duplicate entries from the parsed data
def remove_duplicates(data):
    unique_data = []
    seen = set()
    for row in data:
        row_tuple = tuple(row)  # Convert to tuple for set comparison
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    return unique_data

# Regex patterns for parsing tasks
patterns_collective = [
    r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]
patterns_drill = [
    r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]

# Main program execution
if __name__ == "__main__":
    # Task type selection with an exit option
    while True:
        print("Choose the type of task to parse:")
        print("1. Collective Task")
        print("2. Drill")
        print("3. Exit")
        task_choice = input("Enter 1, 2, or 3: ").strip()

        if task_choice == "1":
            selected_patterns = patterns_collective
            break
        elif task_choice == "2":
            selected_patterns = patterns_drill
            break
        elif task_choice == "3":
            print("Exiting program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # File input with an exit option
    while True:
        input_file = input("Enter the path to the text file (or type 'exit' to quit): ").strip()

        if input_file.lower() == "exit":
            print("Exiting program. Goodbye!")
            exit()

        if not os.path.isfile(input_file):
            print("Error: File not found. Please provide a valid file path or type 'exit' to quit.")
        elif not input_file.lower().endswith(".txt"):
            print("Error: The file must have a .txt extension.")
        else:
            break

    # Read text from the file
    try:
        with open(input_file, 'r') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading the text file: {e}")
        exit()

    # Parse the tasks
    parsed_tasks = parse_tasks(text, selected_patterns)

    # Remove duplicates
    unique_tasks = remove_duplicates(parsed_tasks)

    # Generate an output file name based on the input file name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_output.csv"

    # Write parsed data to a CSV file
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write rows with varying columns
            for row in unique_tasks:
                writer.writerow(row)

        print(f"Data has been successfully saved to {output_file}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
