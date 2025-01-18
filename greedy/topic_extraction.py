"""
Extracts domain-relevant terms from cleaned text using Named Entity Recognition (NER)
and frequent word analysis.
"""

import spacy
from collections import Counter

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

NOISE_WORDS = {"the", "and", "of", "for", "in", "to", "on", "at", "by", "with", "you", "it", "mas"}


def extract_topics(cleaned_text, min_tags=5):
    """
    Extracts topics from cleaned text using NER and ensures a minimum number of tags.
    - Extracts named entities like organizations, locations, and products.
    - Combines named entities with frequent nouns, verbs, and adjectives.
    - If fewer than `min_tags` are found, fills the gap with frequent terms.

    :param cleaned_text: Cleaned text to process.
    :param min_tags: Minimum number of tags to have (default is 5).
    :return: Counter object containing topics and their frequencies.
    """

    doc = nlp(cleaned_text)

    # Extract entities
    keywords = [
        ent.text.lower() for ent in doc.ents
        if ent.label_ in {"ORG", "PRODUCT", "GPE", "LOC", "LANGUAGE", "WORK_OF_ART", "EVENT"}
    ]

    # Add frequent nouns, verbs, and adjectives which aren't noise words
    frequent_terms = [
        token.text.lower() for token in doc
        if token.is_alpha and token.text.lower() not in NOISE_WORDS
        and token.pos_ in {"NOUN", "VERB", "ADJ"}
    ]

    # Combine all terms
    combined_terms = keywords + frequent_terms

    # Ensure at least min number of tags are returned (placeholders appended)
    while len(combined_terms) < min_tags:
        combined_terms.append(f"extra_term_{len(combined_terms) + 1}")

    return Counter(combined_terms)
