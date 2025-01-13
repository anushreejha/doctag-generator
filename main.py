"""
Runs the complete pipeline to generate tags for technical research papers.
"""

import os
import json
from clean_text import clean_text
from extract_topics import extract_topics
from dynamic_stopwords import dynamic_stopwords
from semantic_scoring import score_topics
from process_file import process_files_in_directory  # Pre-process raw files
from tag_cleaning import process_tags  # Final cleaning of saved tags

def main_pipeline(raw_text):
    """
    Executes the pipeline for cleaning text, extracting topics, and scoring them.

    :param raw_text: Raw input text to be processed.
    :return: Dictionary of scored topics sorted by relevance.
    """
    # Step 1: Clean the text
    cleaned_text = clean_text(raw_text)

    # Step 2: Extract topics using NER and frequent word analysis
    extracted_topics = extract_topics(cleaned_text)

    # Step 3: Filter out frequent but irrelevant topics
    filtered_topics = dynamic_stopwords(extracted_topics)

    # Step 4: Score topics based on semantic relevance to the raw text
    final_topics = score_topics(filtered_topics, raw_text)

    return final_topics

def process_files(input_dir, output_dir, tags_dir):
    """
    Processes all text files in the input directory, generates tags, and saves them as JSON.
    Also pre-processes raw files before running the pipeline.

    :param input_dir: Directory containing raw text files.
    :param output_dir: Directory to save pre-processed text files.
    :param tags_dir: Directory to save generated topic tags in JSON format.
    """
    # Step 1: Pre-process raw files (removes irrelevant lines and prepares cleaned text)
    process_files_in_directory(input_dir, output_dir)

    # Step 2: Process each cleaned file to extract and save tags
    os.makedirs(tags_dir, exist_ok=True)

    for file_name in os.listdir(output_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, 'r', encoding='utf-8') as file:
                raw_text = file.read()

            # Run the pipeline to extract and score topics
            topics = main_pipeline(raw_text)

            # Save the topics to a JSON file
            output_file_name = file_name.replace(".txt", ".json")
            output_path = os.path.join(tags_dir, output_file_name)

            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump({"topics": topics}, json_file, indent=4)

            print(f"Tags for {file_name} saved to {output_path}.")

    # Step 3: Perform final cleaning on all tags in the tags directory
    process_tags(tags_dir)

if __name__ == "__main__":
    # Specify directories for raw inputs, pre-processed files, and generated tags
    raw_inputs_dir = "raw_inputs"
    processed_dir = "processed_inputs"
    tags_dir = "tags"

    # Execute the pipeline
    process_files(raw_inputs_dir, processed_dir, tags_dir)
