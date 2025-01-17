"""
Filters out frequent but irrelevant topics based on a frequency threshold.
"""


def dynamic_stopwords(topics, threshold=0.05):
    """
    Identifies and removes dynamically frequent but irrelevant topics. Topics with a frequency
    ratio greater than or equal to the threshold (relative to the total term frequency) are
    filtered out.

    :param topics: Dictionary with topic terms as keys and their frequencies as values.
    :param threshold: Frequency ratio threshold above which topics are considered irrelevant (default = 0.05).
    :return: Filtered dictionary of topics.
    """

    total_terms = sum(topics.values())

    # Retain only those topics with frequency ratio below the threshold
    return {term: freq for term, freq in topics.items() if freq / total_terms < threshold}
