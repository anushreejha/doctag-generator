# from fastapi import FastAPI, UploadFile, File, HTTPException
# from tagging import generate_tags, load_model
# import logging
# import motor.motor_asyncio
# import os
# from dotenv import load_dotenv 

# load_dotenv()

# app = FastAPI()
# model, tokenizer, device = load_model()

# logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger(__name__)

# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise ValueError("MONGO_URI is not set in the environment!")

# DB_NAME = "tagging_db"
# COLLECTION_NAME = "pdf_tags"

# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
# db = client[DB_NAME]
# collection = db[COLLECTION_NAME]

# class TagGenerator:
#     def __init__(self, text: str):
#         self.text = text
#         self.tags = []
    
#     def generate(self):
#         self.tags = generate_tags(self.text, tokenizer, model, device)

# @app.post("/generate-tags/")
# async def generate_tags_from_file(file: UploadFile = File(..., description="Upload a processed text file")):
#     try:
#         content = await file.read()
#         text = content.decode("utf-8")

#         if text == "":              # check for completely empty files
#             raise HTTPException(status_code=400, detail="Uploaded file is empty.")
#         if not text.strip():        # treat whitespace-only files as invalid input
#             raise HTTPException(status_code=400, detail="Failed to generate tags.")

#         try:
#             tag_object = TagGenerator(text)
#             tag_object.generate()
#             print(tag_object.__dict__["tags"])  
#         except Exception as gen_error:
#             logger.error(f"Tag generation failed: {gen_error}")
#             raise HTTPException(status_code=400, detail="Failed to generate tags.")

#         if not tag_object.tags:
#             raise HTTPException(status_code=400, detail="Failed to generate tags.")

#         file_path = os.path.abspath(file.filename)
        
#         # Save to collection (unique id = absolute file path)
#         await collection.update_one(
#             {"_id": file_path},
#             {"$set": {"tags": tag_object.tags}},
#             upsert=True
#         )

#         return {"tags": tag_object.tags}
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @app.get("/status/")
# def status():
#     return {"status": "running"}


from fastapi import FastAPI, UploadFile, File, HTTPException
import logging
import motor.motor_asyncio
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv 

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment!")

DB_NAME = "tagging_db"
COLLECTION_NAME = "pdf_tags"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_model():
    """Load the model and tokenizer."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2-1.5B-Instruct",
        torch_dtype="auto",
        device_map="auto",  
        trust_remote_code=True
    )

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")

    return model, tokenizer, device  

model, tokenizer, device = load_model()

def generate_tags(text, tokenizer, model, device, max_new_tokens=150, num_tags=10):
    """Generate tags from the input text."""

    prompt = (
    "Extract the most relevant and technical tags from the following text, "
    "ensuring they are specific to the domain of the content.\n\n"
    "The tags must meet the following conditions:\n"
    "- All tags should be in lowercase.\n"
    "- If a tag consists of multiple words, replace spaces with hyphens between words.\n"
    "- Tags should not contain any symbols or special characters apart from hyphens.\n"
    "- Generate exactly {num_tags} tags, ordered from most relevant to least relevant.\n\n"
    f"{text}\n\n"
    "Output the tags as a JSON list without additional explanation."
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text_input], return_tensors="pt").to(device)

    with torch.no_grad():  
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=max_new_tokens
        )

    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    try:
        start = output.find("[")
        end = output.find("]") + 1
        raw_tags = json.loads(output[start:end])  
        final_tags = [tag.replace("_", "-").lower() for tag in raw_tags]
        return final_tags
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}\nOutput: {output}")
        return []

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
        
        # save to collection (unique id = absolute file path)
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
