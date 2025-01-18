"""
Processes JSON files containing tags to:
1. Convert tags to lowercase.
2. Replace underscores with spaces.
3. Remove noise words.
"""

import os
import json
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))


def convert_tags_to_lowercase(data):
    """Convert all tags to lowercase."""
    if "tags" in data:
        data["tags"] = [tag.lower() for tag in data["tags"]]
    return data


def replace_underscores_with_spaces(data):
    """Replace underscores in tags with spaces."""
    if "tags" in data:
        data["tags"] = [tag.replace('_', ' ') for tag in data["tags"]]
    return data


def remove_noise_words(data):
    """Remove noise words from tags."""
    if "tags" in data:
        data["tags"] = [tag for tag in data["tags"] if tag not in stopwords_set]
    return data


def process_json_file(input_path):
    """Process a single JSON file and save the cleaned output."""
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data = convert_tags_to_lowercase(data)
    data = replace_underscores_with_spaces(data)
    data = remove_noise_words(data)

    with open(input_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_files(input_dir):
    """Process all JSON files in a directory."""
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_dir, file_name)
            process_json_file(input_path)


def main():
    input_dir = "tags"
    process_files(input_dir)


if __name__ == "__main__":
    main()
