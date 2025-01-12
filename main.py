"""
Runs the complete pipeline to generate tags.
"""

import os
import json
from text_cleaning import clean_text
from topic_extraction import extract_topics
from dynamic_stopwords import dynamic_stopwords
from semantic_scoring import score_topics
from process_file import process_files_in_directory
from tag_cleaning import process_tags

def main(raw_text):
    """
    Executes the pipeline for cleaning text, extracting topics and scoring them.

    :param raw_text: Raw input text to be processed.
    :return: Dictionary of scored topics sorted by relevance.
    """

    # Clean the raw text
    cleaned_text = clean_text(raw_text)

    # Extract topics
    extracted_topics = extract_topics(cleaned_text)

    # Apply dynamic stopword filtering to remove irrelevant topics
    filtered_topics = dynamic_stopwords(extracted_topics)

    # Score the remaining topics based on semantic relevance
    final_topics = score_topics(filtered_topics, raw_text)

    return final_topics

if __name__ == "__main__":
    # Preprocess raw input files
    input_directory = 'raw_inputs'  # Input directory for raw files (in .txt format)
    output_directory = 'inputs'    # Directory for cleaned text files
    process_files_in_directory(input_directory, output_directory)

    # Process cleaned files and extract tags
    tags_dir = "tags"  # Directory for topic tags (json files)
    os.makedirs(tags_dir, exist_ok=True)

    for input_file in os.listdir(output_directory):
        if input_file.endswith(".txt"):  
            input_path = os.path.join(output_directory, input_file)

            with open(input_path, "r") as file:
                raw_text = file.read()

            # Execute the pipeline 
            topics = main(raw_text)

            # Save the topics to JSON files
            output_file_name = os.path.splitext(input_file)[0] + ".json"
            output_path = os.path.join(tags_dir, output_file_name)

            with open(output_path, "w") as json_file:
                json.dump({"topics": topics}, json_file, indent=4)

            # Further cleaning of tags
            process_tags(tags_dir)

            print(f"Tags for {input_file} saved to {output_path}.")
