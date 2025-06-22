from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from prompter import PromptManager

app = FastAPI(title="Prompter API")
pm = PromptManager()

class PromptCreate(BaseModel):
    text: str

class PromptRate(BaseModel):
    up: bool = True

class Comment(BaseModel):
    text: str

class RegenerateRequest(BaseModel):
    system_prompt: Optional[str] = None

@app.get("/prompts")
def list_prompts():
    return pm.list_prompts()

@app.post("/prompts")
def create_prompt(data: PromptCreate):
    pid = pm.create_prompt(data.text)
    return {"id": pid}

@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    prompts = [p for p in pm.list_prompts() if p["id"] == prompt_id]
    if not prompts:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompts[0]

@app.post("/prompts/{prompt_id}/rate")
def rate_prompt(prompt_id: str, rating: PromptRate):
    if not pm.rate_prompt(prompt_id, rating.up):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"success": True}

@app.post("/prompts/{prompt_id}/comment")
def add_comment(prompt_id: str, comment: Comment):
    if not pm.comment(prompt_id, comment.text):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"success": True}

@app.post("/prompts/{prompt_id}/regenerate")
def regenerate_prompt(prompt_id: str, req: RegenerateRequest):
    try:
        new_text = pm.regenerate(prompt_id, system_prompt=req.system_prompt)
    except KeyError:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"text": new_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
