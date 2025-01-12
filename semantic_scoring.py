"""
Scores topics based on their semantic relevance to the raw text
using the pre-trained SentenceTransformer model.
"""

from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

def score_topics(topics, raw_text, max_tags=20, relevance_threshold=0.2):
    """
    Scores and filters topics based on semantic similarity and frequency.

    - Topics with a score below the `relevance_threshold` are excluded.
    - Ensures at least 5 tags are retained by adding fallback tags.

    :param topics: Dictionary of topics and their frequencies.
    :param raw_text: Original text to calculate the semantic similarity.
    :param max_tags: Maximum number of tags to retain (default is 20).
    :param relevance_threshold: Minimum score for a tag to be counted as relevant (default is 0.2).
    :return: Dictionary of scored topics sorted by relevance.
    """

    # Encode raw text into a semantic embedding
    text_embedding = model.encode(raw_text, convert_to_tensor=True)
    scored_topics = {}

    for topic, freq in topics.items():
        # Encode the topic into a semantic embedding
        topic_embedding = model.encode(topic, convert_to_tensor=True)

        # Calculate cosine similariy between topic and raw text
        similarity = util.cos_sim(topic_embedding, text_embedding).item()

        # Calculate the score by combining similarity and frequency
        score = similarity * freq

        # Retain topics above threshold
        if score >= relevance_threshold:
            scored_topics[topic] = score

    # Sort topics by score with limit (default 20)
    sorted_topics = dict(sorted(scored_topics.items(), key=lambda x: x[1], reverse=True)[:max_tags])

    # Ensure at least 5 tags are included
    while len(sorted_topics) < 5:
        sorted_topics[f"fallback_tag_{len(sorted_topics) + 1}"] = 0.1

    return sorted_topics
