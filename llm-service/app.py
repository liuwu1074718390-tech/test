from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from llm_client import QwenClient
import uvicorn
import os

app = FastAPI(title="LLM Service - Qwen3-235B")
client = QwenClient()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

@app.get("/")
async def health_check():
    return {"status": "ok", "model": client.model_name}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    对话接口
    """
    # 转换为 client 需要的格式
    msgs = [{"role": m.role, "content": m.content} for m in request.messages]
    
    result = client.chat(msgs, temperature=request.temperature, max_tokens=request.max_tokens)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    print(f"🚀 LLM 服务启动中，监听端口: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
