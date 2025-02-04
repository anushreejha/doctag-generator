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
    """Crop content, only include content until Introduction section of file."""
    match = re.search(r'^\d*\.?\s*Introduction$', content, re.IGNORECASE | re.MULTILINE)
    return content[:match.start()] if match else content

def process_text(content):
    cropped_content = crop_file(content)
    processed_lines = [line for line in cropped_content.splitlines() if not omit_line(line)]
    return '\n'.join(processed_lines)

def process_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
                processed_content = process_text(content)
                
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            
            print(f"Processed: {filename} -> {output_path}")

if __name__ == "__main__":
    INPUT_DIR = "inputs"
    OUTPUT_DIR = "processed_inputs"
    process_files(INPUT_DIR, OUTPUT_DIR)
