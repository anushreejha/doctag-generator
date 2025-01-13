"""
Scores topics based on their semantic relevance to the raw text
using the pre-trained SentenceTransformer model. Replaces fallback tags with extracted terms.
"""

from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

def score_topics(topics, raw_text, cleaned_text, min_tags=5, max_tags=20, relevance_threshold=0.2):
    """
    Scores and filters topics based on semantic similarity and frequency.
    - Ensures at least `min_tags` are retained by adding fallback terms from extracted keywords.

    :param topics: Dictionary of topics and their frequencies.
    :param raw_text: Original text to calculate semantic similarity.
    :param cleaned_text: Cleaned text for deriving fallback terms.
    :param min_tags: Minimum number of tags to retain (default is 5).
    :param max_tags: Maximum number of tags to retain (default is 20).
    :param relevance_threshold: Minimum score for a tag to be counted as relevant.
    :return: Dictionary of scored topics sorted by relevance.
    """
    text_embedding = model.encode(raw_text, convert_to_tensor=True)
    scored_topics = {}

    for topic, freq in topics.items():
        topic_embedding = model.encode(topic, convert_to_tensor=True)
        similarity = util.cos_sim(topic_embedding, text_embedding).item()
        score = similarity * freq

        if score >= relevance_threshold:
            scored_topics[topic] = score

    # Sort topics by score, up to max_tags
    sorted_topics = dict(sorted(scored_topics.items(), key=lambda x: x[1], reverse=True)[:max_tags])

    # Ensure at least min_tags by deriving fallback terms from extracted terms
    if len(sorted_topics) < min_tags:
        fallback_terms = derive_fallback_terms(cleaned_text, min_tags - len(sorted_topics))
        for term in fallback_terms:
            sorted_topics[term] = 0.1  # Assign a low default score to fallback terms

    return sorted_topics

def derive_fallback_terms(cleaned_text, num_terms):
    """
    Derives fallback terms from the cleaned text.
    :param cleaned_text: The cleaned text to process.
    :param num_terms: Number of fallback terms to generate.
    :return: List of fallback terms.
    """
    from collections import Counter

    # Use frequent terms from the text as fallback
    words = [word.lower() for word in cleaned_text.split() if len(word) > 2]
    most_common_words = [word for word, _ in Counter(words).most_common(num_terms)]

    return most_common_words
