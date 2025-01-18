# Doctag Generator

A Python tool that processes text files to generate domain-specific tags using the Qwen-1.5B-Instruct model. It cleans, standardizes, and filters the tags, outputting them as a clean, relevant JSON list.

---

## Pipeline Overview

The pipeline consists of three steps:

1. **Preprocessing Text Files**  
   Crops unnecessary sections and removes insignificant lines from input text files.

2. **Generating Tags**  
   Generates relevant tags from the preprocessed text using the **Qwen-1.5B-Instruct** model.

3. **Cleaning Tags**  
   Cleans the generated tags by formatting tags and filtering noise words.

---

## Usage

1. Clone the repository:
```bash
git clone https://github.com/anushreejha/doctag-generator
cd doctag-generator
```

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Run:
```bash
python main.py
```