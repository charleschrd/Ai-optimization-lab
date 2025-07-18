from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_DIR = "training/tiny-gpt2-finetuned"

# ────────────────────────────────────────────────────────────────
# Chargement du modèle
# ────────────────────────────────────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)

# ────────────────────────────────────────────────────────────────
# Schémas Pydantic
# ────────────────────────────────────────────────────────────────
class GenerationParams(BaseModel):
    max_tokens:    int     = Field(80, gt=1, le=512)
    temperature:   float   = Field(1.0, gt=0.0, le=2.0)
    top_p:         float   = Field(0.9, gt=0.0, le=1.0)
    do_sample:     bool    = True

class CompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    generation: Optional[GenerationParams] = GenerationParams()

class Choice(BaseModel):
    text: str

class CompletionResponse(BaseModel):
    id: str
    model: str
    choices: List[Choice]

# ────────────────────────────────────────────────────────────────
# FastAPI app
# ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Tiny‑GPT Completions API",
    version="1.0",
    description="Generate text with a fine‑tuned DistilGPT‑2 model.",
    docs_url="/docs",
    redoc_url=None,
)

@app.get("/", tags=["utility"])
def root():
    return {"status": "Tiny‑GPT API up", "model": MODEL_DIR}

@app.get("/health", tags=["utility"])
def health():
    return {"ok": True}

@app.get("/models", tags=["utility"])
def list_models():
    return {"available_models": [MODEL_DIR]}

@app.post("/v1/completions", response_model=CompletionResponse, tags=["generation"])
def completions(req: CompletionRequest):
    try:
        gen_cfg = req.generation or GenerationParams()
        outputs = generator(
            req.prompt,
            max_new_tokens=gen_cfg.max_tokens,
            temperature=gen_cfg.temperature,
            top_p=gen_cfg.top_p,
            do_sample=gen_cfg.do_sample,
            pad_token_id=tokenizer.eos_token_id,
        )
        result = outputs[0]["generated_text"]
        return CompletionResponse(
            id=str(uuid4()),
            model=MODEL_DIR.split("/")[-1],
            choices=[Choice(text=result)]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
