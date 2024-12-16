import csv
import re
import PyPDF2
import os
import time

# Function to parse tasks using regex patterns
def parse_tasks(text, patterns):
    parsed_data = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            # Handle Drill Type column for Supporting Drills
            if "Battle Drill" in match.group('title'):
                parsed_data.append([
                    match.group('step') if match.group('step') else '',
                    match.group('task'),
                    match.group('title'),
                    "Battle Drill",  # Extra column for Drill Type
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

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

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
    # Supporting Collective Tasks and Individual Tasks
    r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)',
    # Supporting Drills (Handles Drill Type "Battle Drill")
    r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
]

# Function to get file input from the user
def get_file_input():
    print("Choose the file type to parse:")
    print("1. Text File (.txt)")
    print("2. PDF File (.pdf)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        file_path = input("Enter the path to the text file (.txt): ").strip()
    elif choice == "2":
        file_path = input("Enter the path to the PDF file (.pdf): ").strip()
    else:
        print("Invalid choice. Exiting.")
        exit()

    if not os.path.isfile(file_path):
        print("Error: File not found. Please provide a valid file path.")
        exit()

    return choice, file_path

# Main Program Execution
if __name__ == "__main__":
    choice, input_file = get_file_input()

    # Extract text based on file type
    if choice == "1":  # Text file
        with open(input_file, 'r') as file:
            text = file.read()
    elif choice == "2":  # PDF file
        text = extract_text_from_pdf(input_file)

    # Parse the tasks
    parsed_tasks = parse_tasks(text, patterns)

    # Remove duplicates
    unique_tasks = remove_duplicates(parsed_tasks)

    # Generate unique output file name
    output_file = f"tasks_output_{int(time.time())}.csv"

    # Write parsed data to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write rows with varying columns
        for row in unique_tasks:
            writer.writerow(row)

    print(f"Data has been successfully saved to {output_file}")
