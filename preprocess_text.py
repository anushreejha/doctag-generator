"""
Processes text files to clean content by:
1. Cropping text before the "Introduction" section.
2. Removing empty lines, single characters, and lines with only numbers or symbols.
"""

import os
import re


def omit_line(line):
    """Check if a line should be removed (only single character/numbers/symbols)."""
    removed_line = line.strip()
    return (
        not removed_line or
        len(removed_line) == 1 or
        re.fullmatch(r'[.,\-?!@#$%^&*()_+=\[\]{}<>|/\\:;\'"`~]+', removed_line) or
        re.fullmatch(r'[0-9]+(\.[0-9]+)?', removed_line)
    )


def crop_file(content):
    """Crop content to only include content until the 'Introduction' section."""
    match = re.search(r'^\\d*\\.?\\s*Introduction$', content, re.IGNORECASE | re.MULTILINE)
    return content[:match.start()] if match else content


def process_text_file(input_path, output_path):
    """Process the text file and saves the cleaned output."""
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    cropped_content = crop_file(content)
    processed_lines = [line for line in cropped_content.splitlines() if not omit_line(line)]

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_lines))


def main():
    input_dir = 'inputs'
    output_dir = 'processed_inputs'
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace('.txt', '_processed.txt')
            output_path = os.path.join(output_dir, output_filename)
            process_text_file(input_path, output_path)


if __name__ == '__main__':
    main()
