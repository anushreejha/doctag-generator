"""
Cleans raw text by removing noise, irrelevant content and non-alphabetic characters.
"""

import re


def clean_text(raw_text):
    """
    Cleans parsed text by:
    - Removing URLs, citations, inline references and hyphen line breaks.
    - Removing non-alphabet characters (numbers included).
    - Omitting extra spaces.

    :param raw_text: Input raw text to clean.
    :return: Cleaned text as a single string.
    """

    text = re.sub(r'http[s]?://\S+', '', raw_text)  # Remove URLs
    text = re.sub(r'\(\w+ et al\., \d{4}\)', '', text)  # Remove citations
    text = re.sub(r'\[\d+\]', '', text)  # Remove inline references
    text = re.sub(r'-\n', '', text)  # Remove hyphen line breaks
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Remove non-alphabetic characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces

    return text
