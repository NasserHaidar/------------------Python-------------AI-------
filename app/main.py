from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
import os

# Load environment first
load_dotenv()
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")

# Debug print (remove after testing)
print(f"API Key Loaded: {DEEPAI_API_KEY is not None}") 

app = FastAPI()

DEEPAI_API_URL = "https://api.deepai.org/api/nsfw-detector"

@app.post("/moderate")
async def moderate_image(file: UploadFile):
    
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Only JPG/PNG images are allowed")
    
    try:
        
        files = {'image': (file.filename, await file.read(), file.content_type)}
        headers = {'Api-Key': DEEPAI_API_KEY}  
        
        response = requests.post(DEEPAI_API_URL, files=files, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        nsfw_score = result.get('output', {}).get('nsfw_score', 0)
        
        if nsfw_score > 0.7:
            return JSONResponse(
                status_code=200,
                content={"status": "REJECTED", "reason": "NSFW content"}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"status": "OK"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")