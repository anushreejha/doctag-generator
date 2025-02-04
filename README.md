# Doctag Generator

Generates domain-specific tags for text files using the Qwen-1.5B-Instruct model. 

## Setup

1. Clone the repository:
```bash
git clone https://github.com/anushreejha/doctag-generator
cd doctag-generator
```

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Start FastAPI server:
```bash
uvicorn main:app --reload
```

## Usage

1. Check server status:
```bash
curl -X 'GET' 'http://localhost:8000/status/' -H 'accept: application/json'
```

2. Generate tags:
```bash
curl -X 'POST' 'http://localhost:8000/generate-tags/' -F "file=@<path-to-file>"
```
