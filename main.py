from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from model import predict_url
from nlp_model import predict_text
from image_model import predict_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)
class URLRequest(BaseModel):
    url: str

class TextRequest(BaseModel):
    text: str


@app.post("/scan-url")
def scan_url(req: URLRequest):
    score = predict_url(req.url)

    if score > 70:
        verdict = "High Risk"
    elif score > 40:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    return {"risk_score": score, "verdict": verdict}


@app.post("/scan-text")
def scan_text(req: TextRequest):
    score = predict_text(req.text)

    if score > 70:
        verdict = "High Risk"
    elif score > 40:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    return {"risk_score": score, "verdict": verdict}


@app.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    score = await predict_image(file)

    if score > 70:
        verdict = "High Risk"
    elif score > 40:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    return {"risk_score": score, "verdict": verdict}