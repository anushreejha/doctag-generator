"""
Extracts domain-relevant terms from cleaned text using Named Entity Recognition (NER).
"""

import spacy
from collections import Counter

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

NOISE_WORDS = {"the", "and", "of", "for", "in", "to", "on", "at", "by", "with", "you", "it"}

def extract_topics(cleaned_text, min_tags=5):
    """
    Extracts topics from cleaned text using NER and ensures a minimum number of tags.
    - Extracts named entities like organizations, locations, and products.
    - If fewer than `min_tags` are found, generates fallback tags using frequent words.

    :param cleaned_text: Cleaned text to process.
    :param min_tags: Minimum number of tags to have (default is 5).
    :return: Counter object containing topics and their frequencies.
    """
    doc = nlp(cleaned_text)

    # Extract named entities relevant to technical papers
    keywords = [
        ent.text.lower() for ent in doc.ents
        if ent.label_ in {"ORG", "PRODUCT", "GPE", "LOC", "LANGUAGE", "WORK_OF_ART", "EVENT"}
    ]

    # Fallback to frequent nouns and verbs if not enough entities are found
    if len(keywords) < min_tags:
        frequent_words = [
            token.text.lower() for token in doc
            if token.is_alpha and token.text.lower() not in NOISE_WORDS
        ]
        keywords.extend(frequent_words[:min_tags - len(keywords)])

    return Counter(keywords)
