"""
Runs the complete pipeline to generate tags.
"""

import os
import json
from text_cleaning import clean_text
from topic_extraction import extract_topics
from dynamic_stopwords import dynamic_stopwords
from semantic_scoring import score_topics
from process_file import process_input_files
from tag_cleaning import process_tags  


def main_pipeline(raw_text):
    """
    Executes the pipeline for cleaning text, extracting topics and scoring them.

    :param raw_text: Raw input text to be processed.
    :return: Dictionary of scored topics sorted by relevance.
    """

    # Clean the raw text 
    cleaned_text = clean_text(raw_text)

    # Extract topics using NER and frequent word analysis
    extracted_topics = extract_topics(cleaned_text)

    # Filter out frequent but irrelevant topics
    filtered_topics = dynamic_stopwords(extracted_topics)

    # Score topics based on semantic relevance to the raw text
    final_topics = score_topics(filtered_topics, raw_text, cleaned_text)

    return final_topics


def process_files(input_dir, output_dir, tags_dir):
    """
    Pre-processes raw files before running the pipeline, then processes all text files in the 
    input directory, generates tags and saves them as JSON.

    :param input_dir: Directory containing raw text files.
    :param output_dir: Directory to save pre-processed text files.
    :param tags_dir: Directory to save generated topic tags in JSON format.
    """
    
    # Pre-process raw files (removes irrelevant lines and prepares cleaned text)
    process_input_files(input_dir, output_dir)

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

    # Perform final cleaning on all tags in JSON files
    process_tags(tags_dir)


if __name__ == "__main__":
    raw_inputs_dir = "raw_inputs"       # Raw inputs directory
    processed_dir = "processed_inputs"  # Processed inputs directory
    tags_dir = "tags"                   # Tags directory

    # Run the pipeline
    process_files(raw_inputs_dir, processed_dir, tags_dir)
