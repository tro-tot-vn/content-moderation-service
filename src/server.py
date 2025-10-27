from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch, time

# ==== cấu hình tối thiểu ====
MODEL_DIR = "lamdx4/phobert-vi-moderation"
MAX_LENGTH = 192
THRESHOLD = 0.5

# ==== load model 1 lần khi khởi động ====
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()
torch.set_grad_enabled(False)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)

app = FastAPI()


class Payload(BaseModel):
    text: str


@app.post("/moderate")
def moderate(p: Payload):
    text = (p.text or "").strip()
    if not text:
        raise HTTPException(status_code=422, detail="Field 'text' must be a non-empty string.")

    t0 = time.time()
    enc = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_LENGTH).to(DEVICE)
    logits = model(**enc).logits
    prob_invalid = torch.softmax(logits, dim=-1)[0, 1].item()
    label = "invalid" if prob_invalid >= THRESHOLD else "valid"
    latency_ms = (time.time() - t0) * 1000.0

    return {
        "label": label,
        "prob_invalid": prob_invalid,
        "threshold": THRESHOLD,
        "latency_ms": round(latency_ms, 2),
    }
