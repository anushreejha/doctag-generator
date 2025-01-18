"""
Executes the pipeline for processing text, generating tags, and cleaning tags.

Pipeline:
1. Preprocess text files in the 'inputs' directory and save cleaned outputs to 'processed_inputs'.
2. Generate relevant tags for the preprocessed text and save them to 'tags'.
3. Clean the generated tags by standardizing and removing noise words.
"""

import os
from preprocess_text import process_text_file  
from qwen_model import load_model, generate_tags, process_files as generate_tags_from_files  
from clean_tags import process_files as clean_tags_from_files  
import torch


def run_preprocess_text(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace('.txt', '_processed.txt')
            output_path = os.path.join(output_dir, output_filename)
            process_text_file(input_path, output_path)


def run_generate_tags(input_dir, output_dir, tokenizer, model, device):
    """Generate tags for processed text files."""
    generate_tags_from_files(input_dir, output_dir, tokenizer, model, device)


def run_clean_tags(input_dir):
    """Clean tags in the generated JSON files."""
    clean_tags_from_files(input_dir)


def main():
    input_dir = 'inputs'                        # Raw text files directory
    processed_input_dir = 'processed_inputs'    # Processed text files directory
    tags_dir = 'tags'                           # Final tags directory

    # Preprocess text files
    run_preprocess_text(input_dir, processed_input_dir)

    # Load model and generate tags
    model, tokenizer = load_model()  # Model loading happens here
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    run_generate_tags(processed_input_dir, tags_dir, tokenizer, model, device)  # Pass model and tokenizer here

    # Clean tags
    run_clean_tags(tags_dir)

    print("Tag generation process completed.")


if __name__ == "__main__":
    main()
