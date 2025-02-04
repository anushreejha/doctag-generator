from fastapi import FastAPI, UploadFile, File, HTTPException
from tagging import generate_tags, load_model

app = FastAPI()
model, tokenizer, device = load_model()

@app.post("/generate-tags/")
async def generate_tags_from_file(file: UploadFile = File(..., description="Upload a processed text file")):
    try:
        content = await file.read()
        text = content.decode("utf-8").strip()

        if not text:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        tags = generate_tags(text, tokenizer, model, device)
        
        if not tags:
            raise HTTPException(status_code=400, detail="Failed to generate tags.")

        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/status/")
def status():
    return {"status": "running"}