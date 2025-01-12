# Doctag Generator

**Doctag Generator** is a Python-based tool that processes raw text documents and automatically generates relevant tags based on the content. The tags are extracted using Named Entity Recognition (NER), filtered for relevance, and semantically scored to ensure they are meaningful to the document.

## Features

- **Text Cleaning**: Removes irrelevant content, noise, and formatting issues.
- **Topic Extraction**: Uses NER to extract domain-specific entities and fallback frequent words.
- **Dynamic Stopword Filtering**: Filters out frequently appearing but irrelevant terms.
- **Semantic Scoring**: Ranks tags based on their semantic relevance to the text.
- **Tag Cleaning**: Processes and cleans extracted tags to ensure quality.
- **JSON Output**: Final tags are stored in JSON format for easy integration.

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/anushreejha/doctag-generator
cd doctag-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the spacy English model:
```bash
python -m spacy download en_core_web_sm
```

4. Run:
```bash
python main.py
```
