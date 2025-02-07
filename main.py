from fastapi import FastAPI, UploadFile, File, HTTPException
from tagging import generate_tags, load_model
import logging
import motor.motor_asyncio
import os
from dotenv import load_dotenv  # ✅ Load environment variables

# Load environment variables from .env
load_dotenv()

app = FastAPI()
model, tokenizer, device = load_model()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ✅ Get MongoDB URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment!")

DB_NAME = "tagging_db"
COLLECTION_NAME = "pdf_tags"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class TagGenerator:
    def __init__(self, text: str):
        self.text = text
        self.tags = []
    
    def generate(self):
        self.tags = generate_tags(self.text, tokenizer, model, device)

@app.post("/generate-tags/")
async def generate_tags_from_file(file: UploadFile = File(..., description="Upload a processed text file")):
    try:
        content = await file.read()
        text = content.decode("utf-8")

        if text == "":              # check for completely empty files
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        if not text.strip():        # treat whitespace-only files as invalid input
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        try:
            tag_object = TagGenerator(text)
            tag_object.generate()
            print(tag_object.__dict__["tags"])  
        except Exception as gen_error:
            logger.error(f"Tag generation failed: {gen_error}")
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        if not tag_object.tags:
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        file_path = os.path.abspath(file.filename)
        
        # Save to collection (unique id = absolute file path)
        await collection.update_one(
            {"_id": file_path},
            {"$set": {"tags": tag_object.tags}},
            upsert=True
        )

        return {"tags": tag_object.tags}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/status/")
def status():
    return {"status": "running"}
