from fastapi import FastAPI, UploadFile, File, HTTPException
from tagging import generate_tags, load_model
import logging

app = FastAPI()
model, tokenizer, device = load_model()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

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
            tags = generate_tags(text, tokenizer, model, device)
        except Exception as gen_error:
            logger.error(f"Tag generation failed: {gen_error}")
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        if not tags:
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        return {"tags": tags}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/status/")
def status():
    return {"status": "running"}
