from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from matcher import extract_text_from_pdf, match_score, get_missing_keywords
import tempfile
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.post("/match")
async def match(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await resume.read())
        tmp_path = tmp.name
    
    resume_text = extract_text_from_pdf(tmp_path)
    os.unlink(tmp_path)
    
    score = match_score(job_description, resume_text)
    missing = get_missing_keywords(job_description, resume_text)
    
    return {
        "match_score": score,
        "missing_keywords": missing
    }