"""
FastAPI Backend for Chatbot - Integrates OpenAI with images and text data
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
from data_loader import DataLoader
from config import SELECTED_MODEL

# Load environment variables (try cle.env first, then .env)
load_dotenv("cle.env")
load_dotenv()  # Fallback to .env if it exists

# Initialize FastAPI app
app = FastAPI(title="Chatbot API")

# Enable CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (works with OpenRouter too!)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Groq configuration (free, fast, reliable!)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    timeout=60.0  # Increase timeout to 60 seconds
)

# Initialize data loader
data_loader = DataLoader()

# Request/Response Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    use_images: Optional[bool] = True
    max_images: Optional[int] = 2

class ChatResponse(BaseModel):
    content: str
    images_used: Optional[List[str]] = []
    source: str = "openai"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Chatbot API is running",
        "data_loaded": {
            "text_size": len(data_loader.text_content),
            "image_folders": list(data_loader.images_data.keys()),
            "total_images": sum(len(imgs) for imgs in data_loader.images_data.values())
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - answers questions based on loaded data
    """
    try:
        # Get the last user message
        user_message = request.messages[-1].content if request.messages else ""
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No message provided")
        
        # Get relevant context from text only (simple and fast)
        text_context = data_loader.get_context_for_query(user_message, max_chars=2000)  # Reduced for faster processing
        
        # Build the system message with context
        system_message = f"""You are a helpful assistant that answers questions based on the L-mobile developer documentation.

Context from documentation:
{text_context}

Answer the user's question based on this context. Be concise and accurate."""

        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add conversation history (limit to last 5 messages to save tokens)
        for msg in request.messages[-5:]:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Use text-only model (Groq - fast and free!)
        response = client.chat.completions.create(
            model=SELECTED_MODEL,  # Model from config.py
            messages=messages,
            max_tokens=500,  # Reduced for faster response
            temperature=0.3
        )
        
        answer = response.choices[0].message.content.strip()
        
        return ChatResponse(
            content=answer,
            images_used=[],  # No images for now
            source="groq"
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/images/summary")
async def get_images_summary():
    """Get summary of available images"""
    return data_loader.get_all_images_summary()

@app.get("/data/stats")
async def get_data_stats():
    """Get statistics about loaded data"""
    return {
        "text_length": len(data_loader.text_content),
        "text_lines": len(data_loader.text_content.split('\n')),
        "images_by_folder": {
            folder: len(images) 
            for folder, images in data_loader.images_data.items()
        },
        "total_images": sum(len(imgs) for imgs in data_loader.images_data.values())
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  L-mobile Chatbot API Server")
    print("=" * 50)
    print(f"[INFO] Loaded {sum(len(imgs) for imgs in data_loader.images_data.values())} images")
    print(f"[INFO] Loaded {len(data_loader.text_content)} characters of text")
    print("[INFO] Starting server on http://localhost:8000")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
