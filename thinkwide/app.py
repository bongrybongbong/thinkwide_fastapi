from fastapi import FastAPI, Form, HTTPException
from typing import Annotated
from typing import List
import uvicorn
import httpx
from pydantic import BaseModel
import mindmap_generator
import mindmap
import prompt

app = FastAPI()

class MindMapRequest(BaseModel):
    connected_nodes: list[str]

class DataIn(BaseModel):
    id: int
    Node_text: List[str]

class DataOut(BaseModel):
    id: int
    keyword_suggestions: List[str]

@app.post("/keywordsuggestions/")
async def keyword_suggestions(data: DataIn) -> DataOut:
    connected_nodes = data.Node_text
    aiKeywords = mindmap_generator.get_recommendations(connected_nodes)
    return DataOut(id=data.id, keyword_suggestions=aiKeywords)

class MindMapRequest(BaseModel):
    connected_nodes: list[str]

@app.post("/makemindmap/")
async def make_mindmap(data: MindMapRequest):
    connected_nodes = data.connected_nodes
    results = mindmap.get_mindmap(connected_nodes)
    return results

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    gpt_response, _ = ask_chatgpt(request.messages)
    return {"response": gpt_response}


if __name__ == "__main__":
    # from models import Base
    # Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=5000)
