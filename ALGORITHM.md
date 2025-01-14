# Doctag Generator Algorithm

### 1. Preprocessing Raw Files (`process_file.py`)

- **Purpose**: Prepares raw text files for tag generation by removing noise and focusing on relevant sections.
- **Actions**:
  - Removes lines with only numbers, single characters, or dots (`.` or `...`).
  - Stops processing once the "Introduction" section is encountered.
  - Saves the cleaned text to a new directory.

### 2. Text Cleaning (`text_cleaning.py`)

- **Purpose**: Cleans the content of the text by removing noise and irrelevant content.
- **Actions**:
  - Removes URLs, citations, and inline references.
  - Eliminates non-alphabet characters.
  - Removes hyphen line breaks and extra spaces.

### 3. Topic Extraction (`topic_extraction.py`)

- **Purpose**: Identifies key terms or topics from the cleaned text.
- **Actions**:
  - Uses Named Entity Recognition (NER) via spaCy to extract entities and combines it with frequent terms from document.
  - If fewer than the minimum required tags (`min_tags`), generates fallback tags which are derived frequent words in text which can be used as tags.
  - Returns a dictionary of topics with their frequencies.

### 4. Dynamic Stopword Filtering (`dynamic_stopwords.py`)

- **Purpose**: Removes irrelevant frequent terms dynamically based on a frequency threshold.
- **Actions**:
  - Filters out topics with a frequency ratio above a specified threshold.

### 5. Semantic Scoring (`semantic_scoring.py`)

- **Purpose**: Scores and ranks topics based on their semantic relevance to the raw text and based on frequency relevance.
- **Actions**:
  - Uses SentenceTransformer to calculate cosine similarity between topics and the raw text.
  - Combines frequency and semantic similarity to score topics.
  - Fallback tags used to ensure minimum 5 tags generated per document.

### 6. Tag Cleaning (`tag_cleaning.py`)

- **Purpose**: Finalizes the extracted tags by removing noise and ensuring quality.
- **Actions**:
  - Removes single-character words and non-English words.
  - Filters out noise words.
  - Saves the cleaned tags back to JSON files.

## Order of Processing

1. **Raw File Preprocessing**: `process_files_in_directory()` in `process_file.py` processes all files in the `raw_inputs` directory and saves cleaned versions in the `processed_inputs` directory.
2. **Text Cleaning**: `clean_text()` in `text_cleaning.py` cleans the raw text.
3. **Topic Extraction**: `extract_topics()` in `topic_extraction.py` identifies relevant terms using NER and frequent words as fallbacks.
4. **Dynamic Stopword Filtering**: `dynamic_stopwords()` in `dynamic_stopwords.py` removes frequent but irrelevant topics.
5. **Semantic Scoring**: `score_topics()` in `semantic_scoring.py` ranks topics by combining frequency and semantic similarity.
6. **Final Tag Cleaning**: `process_tags()` in `tag_cleaning.py` finalizes tags by removing noise and non-English words.
7. **Output**: Final tags are saved as JSON files in the `tags` directory.
