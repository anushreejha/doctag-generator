"""
Scores extracted topics based on their semantic relevance to the input text.
"""

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def score_topics(topics, raw_text):
    """
    Scores topics based on their semantic relevance to the raw text.

    - Uses SentenceTransformer to compute embeddings for both - text and topics.
    - Combine semantic similarity with topic frequency to assign scores.

    :param topics: Dictionary of topics and their frequencies.
    :param raw_text: Original input text for semantic comparison.
    :return: Dictionary of topics with their relevance scores.
    """

    # Load model
    model = SentenceTransformer('all-MiniLM-L6-v2')  

    # Calculate text embedding
    text_embedding = model.encode(raw_text)  

    scored_topics = {}
    for term, freq in topics.items():
        topic_embedding = model.encode(term)  # Calculate topic embedding
        similarity = cosine_similarity([text_embedding], [topic_embedding])[0][0]  # Calculate similarity
        scored_topics[term] = similarity * freq  # Combine similarity and frequency

    # Return topics sorted by order of descending score 
    return dict(sorted(scored_topics.items(), key=lambda item: item[1], reverse=True))
