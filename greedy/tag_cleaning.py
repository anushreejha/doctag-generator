"""
Processes and cleans extracted tags from JSON files in a directory.
"""

import os
import json
import spacy

# Load the spaCy English model (for English words detection)
nlp = spacy.load("en_core_web_sm")

NOISE_WORDS = {"the", "and", "li", "la", "al", "you", "i", "lu", "chen", "english", "mas"}


def is_english(word):
    """
    Checks whether a word is English using spaCy's language detection.

    :param word: Word to evaluate.
    :return: True if the word is English, False otherwise.
    """

    doc = nlp(word)
    return doc[0].lang_ == "en" if doc else False


def clean_tag(tag):
    """
    Cleans a tag by:
    - Removing single-character words.
    - Removing some unwanted/noise words.
    - Preserving only English single word tags.
    - Filtering out non-English words longer than 4 characters, except for single-word tags.

    :param tag: Original tag to clean.
    :return: Cleaned tag or None if the tag is invalid.
    """

    words = tag.split()

    # Remove single-character words
    words = [word for word in words if len(word) > 1]

    # Remove unwanted words
    words = [word for word in words if word.lower() not in NOISE_WORDS]
    
    # For single-word tags, preserve only if it's an English word (reduces noise word tags)
    if len(words) == 1:  
        return tag if is_english(tag) else None

    # For multiple-word tags, retain words that are either <= 4 characters or English words 
    # (to make sure including terms like "nlp", "llm" which aren't proper words but to prevent 
    # including noise words)
    cleaned_words = [word for word in words if len(word) <= 4 or is_english(word)]
    return " ".join(cleaned_words) if cleaned_words else None


def process_tags(tags_directory, min_tags=5):
    """
    Processes JSON files in the directory to clean and remove noise tags.

    :param tags_directory: Directory containing the JSON files with extracted tags.
    :param min_tags: Minimum number of tags to ensure in each file (default is 5).
    """

    for filename in os.listdir(tags_directory):
        if filename.endswith('.json'):  
            file_path = os.path.join(tags_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            cleaned_topics = {}

            # Clean and validate each tag
            for tag, score in data.get("topics", {}).items():
                cleaned_tag = clean_tag(tag)
                if cleaned_tag:  
                    cleaned_topics[cleaned_tag] = score

            # # Ensure at least 5 tags are present by adding fallback tags
            # if len(cleaned_topics) < min_tags:
            #     fallback_tags = [f"fallback_tag_{i+1}" for i in range(min_tags - len(cleaned_topics))]
            #     for tag in fallback_tags:
            #         cleaned_topics[tag] = 0.1  # Assign a low default score to fallback tags

            # Save the cleaned tags to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({"topics": cleaned_topics}, file, indent=4)
