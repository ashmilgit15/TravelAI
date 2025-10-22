from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(title="Travel Planner AI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

# In-memory conversation storage (use database in production)
conversations = {}

# Pydantic models
class Message(BaseModel):
    content: str
    conversation_id: str

class ConversationHistory(BaseModel):
    conversation_id: str

class TravelPlannerSystem:
    """System prompt for the travel planner AI"""
    
    SYSTEM_PROMPT = """You are an expert travel planning AI assistant with deep knowledge of:
- Destination recommendations based on preferences
- Budget optimization and travel cost management
- Itinerary planning and activity suggestions
- Flight and accommodation recommendations
- Travel tips, safety, and cultural etiquette
- Weather patterns and best seasons to visit
- Visa requirements and travel documentation
- Local transportation options
- Restaurant and dining recommendations
- Off-the-beaten-path attractions

**RESPONSE FORMAT GUIDELINES:**
Always format your responses using markdown for clarity and visual appeal:

1. **Use Headers** for main sections (# for titles, ## for subsections)
2. **Use Bullet Points** for lists and options
3. **Use Bold** for important information and highlights
4. **Use Tables** for comparisons, budgets, and schedules
5. **Use Code Blocks** for itineraries, contact info, or structured data
6. **Use Lists** (numbered for steps, bullet points for options)
7. **Use Blockquotes** for tips and warnings
8. **Use Horizontal Rules** to separate major sections

**CONTENT GUIDELINES:**
When helping users plan trips:
1. Ask clarifying questions about preferences, budget, dates, and interests
2. Provide specific, actionable, detailed recommendations
3. Consider budget constraints and suggest cost-saving tips
4. Create detailed day-by-day itineraries with times and costs when requested
5. Include real-time information context (use your knowledge)
6. Suggest backup plans and alternatives
7. Include practical tips about local customs and language

**TONE:**
Be conversational, friendly, enthusiastic, and genuinely helpful. Remember context from earlier in the conversation. Use emojis sparingly but strategically (🌍 ✈️ 🏨 🍽️ 💰 📍 ⏰) to enhance readability."""

    @staticmethod
    def get_system_message():
        return TravelPlannerSystem.SYSTEM_PROMPT

def get_or_create_conversation(conversation_id: str):
    """Get or create a conversation history"""
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    return conversations[conversation_id]

def format_conversation_history(history: list) -> str:
    """Format conversation history for the model"""
    formatted = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")
    return "\n".join(formatted)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Travel Planner AI</h1><p>Static files not found. Check your setup.</p>"

@app.post("/api/chat")
async def chat(message: Message):
    """Handle chat messages with streaming response"""
    try:
        conversation_id = message.conversation_id
        user_message = message.content
        
        if not user_message or not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get or create conversation history
        history = get_or_create_conversation(conversation_id)
        
        # Create the model with system instruction
        system_prompt = TravelPlannerSystem.get_system_message()
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=system_prompt
        )
        
        # Stream the response
        async def generate():
            full_response = ""
            try:
                # Convert conversation history to Gemini format
                chat_history = []
                for msg in history:
                    chat_history.append({
                        "role": msg["role"] if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}]
                    })
                
                # Start a chat session with history
                chat = model.start_chat(history=chat_history)
                
                # Send the new message and stream response
                response = await asyncio.to_thread(
                    lambda: chat.send_message(
                        user_message,
                        stream=True
                    )
                )
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        yield chunk.text
                
                # Ensure we have a response
                if not full_response:
                    full_response = "I encountered an issue generating a response. Please try again."
                
                # Add messages to history
                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"Streaming error: {error_msg}")
                if not full_response:
                    yield error_msg
                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": full_response or error_msg})
        
        return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    history = conversations.get(conversation_id, [])
    return {"conversation_id": conversation_id, "messages": history}

@app.post("/api/conversations/{conversation_id}/clear")
async def clear_conversation(conversation_id: str):
    """Clear conversation history"""
    if conversation_id in conversations:
        del conversations[conversation_id]
    return {"status": "cleared", "conversation_id": conversation_id}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": "gemini-2.5-flash"
    }

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)