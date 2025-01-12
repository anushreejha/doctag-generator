"""
Processes text files by removing irrelevant lines, cropping content before 
'Introduction' section and saving the cleaned text for tag generation.
"""

import os

def process_file(file_path, output_dir):
    """
    Processes a single file by:
    - Removing lines with only numbers, single characters, or dots ("...").
    - Cropping content until the "Introduction" section.
    - Saving the processed content to an output directory.

    :param file_path: Path of the file to process.
    :param output_dir: Directory where the processed file should be saved.
    """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        stripped_line = line.strip()

        # Skip lines with only numbers or single characters
        if stripped_line.isdigit() or len(stripped_line) == 1:
            continue

        # Skip lines with only a single period (.) or multiple dots (...)
        if stripped_line == '.' or stripped_line == '...':
            continue

        # Stop processing when the "Introduction" section is found
        if stripped_line.lower() == "introduction":
            break

        # Append cleaned line to the result
        processed_lines.append(line)

    _, file_name = os.path.split(file_path)
    processed_file_path = os.path.join(output_dir, file_name.replace('.txt', '_processed.txt'))

    os.makedirs(output_dir, exist_ok=True)

    # Save processed content to new file
    with open(processed_file_path, 'w') as processed_file:
        processed_file.writelines(processed_lines)

def process_files_in_directory(input_dir, output_dir):
    """
    Processes all text files in input directory and saves to output directory.

    :param input_dir: Directory containing the input text files.
    :param output_dir: Directory where processed files should be saved.
    """

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):  
                file_path = os.path.join(root, file)
                process_file(file_path, output_dir)
