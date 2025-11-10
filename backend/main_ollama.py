"""
FastAPI Backend for Chatbot - Uses Ollama (100% Free, Local)
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from data_loader import DataLoader

# Initialize FastAPI app
app = FastAPI(title="Chatbot API")

# Enable CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # or "llama3.2:1b" for faster, smaller model

# Initialize data loader
data_loader = DataLoader()

# Request/Response Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    use_images: Optional[bool] = False
    max_images: Optional[int] = 0

class ChatResponse(BaseModel):
    content: str
    images_used: Optional[List[str]] = []
    source: str = "ollama"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Chatbot API is running (Ollama)",
        "model": OLLAMA_MODEL,
        "data_loaded": {
            "text_size": len(data_loader.text_content),
            "total_images": 0
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - answers questions based on loaded data using Ollama
    """
    try:
        # Get the last user message
        user_message = request.messages[-1].content if request.messages else ""
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No message provided")
        
        # Get relevant context from text
        text_context = data_loader.get_context_for_query(user_message, max_chars=2000)
        
        # Build the prompt
        prompt = f"""You are a helpful assistant that answers questions based on the L-mobile developer documentation.

Context from documentation:
{text_context}

User question: {user_message}

Answer based on the context above. Be concise and accurate."""

        # Call Ollama API
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 500
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
        
        answer = response.json().get("response", "").strip()
        
        if not answer:
            raise HTTPException(status_code=500, detail="No response from Ollama")
        
        return ChatResponse(
            content=answer,
            images_used=[],
            source="ollama-local"
        )
    
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Cannot connect to Ollama. Make sure Ollama is running (run 'ollama serve' in terminal)"
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/stats")
async def get_data_stats():
    """Get statistics about loaded data"""
    return {
        "text_length": len(data_loader.text_content),
        "text_lines": len(data_loader.text_content.split('\n')),
        "model": OLLAMA_MODEL,
        "backend": "Ollama (Local)"
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  L-mobile Chatbot API Server (Ollama)")
    print("=" * 50)
    print(f"[INFO] Using Ollama model: {OLLAMA_MODEL}")
    print(f"[INFO] Loaded {len(data_loader.text_content)} characters of text")
    print("[INFO] Starting server on http://localhost:8000")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)

