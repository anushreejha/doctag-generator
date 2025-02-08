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
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Docker

1. Build image:
```bash
docker build -t doctag-generator .
```

2. Run container:
```bash
docker run --env-file .env -p 8000:8000 doctag-generator
```

## MongoDB Setup

1. Create a .env file with:
```bash
MONGO_URI=mongodb://<username>:<password>@localhost:27018/tagging_db?authSource=tagging_db
```

2. Run mongoDB in docker:
```bash
docker run -d --name tagging-mongo -p 27018:27017 -e MONGO_INITDB_DATABASE=tagging_db mongo
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

## View Saved Tags 

1. Access the mongoDB shell:
```bash
docker exec -it tagging-mongo mongosh -u <username> -p <password> --authenticationDatabase tagging_db
```

2. Switch to database:
```bash
use tagging_db
```

3. View tags:
```bash
db.pdf_tags.find().pretty()
```
