import csv
import re
import os

# Function to parse tasks using regex patterns
def parse_tasks(text, patterns):
    parsed_data = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            # Collect fields dynamically based on the pattern
            parsed_row = [
                match.group('step').strip() if match.group('step') else '',
                match.group('task').strip(),
                match.group('title').strip(),
                match.group('proponent').strip() if 'proponent' in match.groupdict() else '',
                match.group('status').strip()
            ]
            parsed_data.append(parsed_row)
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
patterns_supporting_collective = [
    r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]
patterns_supporting_drill = [
    r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]
patterns_drill_task = [
    r'(?P<step>\d+)\s+(?P<task>\S+)\s+(?P<title>.+?)\s+(?P<proponent>\S+)\s+(?P<status>Approved)'
]

# Main program execution
if __name__ == "__main__":
    while True:
        print("Choose the type of task to parse:")
        print("1. Collective Task")
        print("2. Drill")
        print("3. Drill Task")
        print("4. Exit")
        task_choice = input("Enter 1, 2, 3, or 4: ").strip()

        # Map the user's choice to patterns and file suffix
        if task_choice == "1":
            selected_patterns = patterns_collective
            file_suffix = "Collective_Tasks"
            break
        elif task_choice == "2":
            selected_patterns = patterns_drill
            file_suffix = "Drill"
            break
        elif task_choice == "3":
            selected_patterns = patterns_drill_task
            file_suffix = "Drill_Tasks"
            break
        elif task_choice == "4":
            print("Exiting program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    # File input
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
    output_file = f"{base_name}_{file_suffix}.csv"

    # Write parsed data to a CSV file
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            if task_choice == "3":  # Drill Task has more columns
                writer.writerow(["Step ID", "Task ID", "Task Title", "Proponent", "Status"])
            else:
                writer.writerow(["Step ID", "Task ID", "Task Title", "Proponent", "Status"])

            # Write rows with parsed data
            for row in unique_tasks:
                writer.writerow(row)

        print(f"Data has been successfully saved to {output_file}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
