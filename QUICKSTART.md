# 🚀 Quick Start Guide

## What You Have

A complete AI chatbot system that:
- ✅ Answers questions about L-mobile developer documentation
- ✅ Processes both text (307,851 characters) and images (126 images)
- ✅ Works as a browser extension on any webpage
- ✅ Uses OpenAI GPT-4 Vision API

## Test Results

```
[PASS] - File Structure
[PASS] - Python Imports  
[PASS] - Environment
[PASS] - Data Loader

Total Images: 126
- images_extraites: 36
- images_nommees: 31
- images_simples: 31
- images_titre_associe: 28
```

## Step 1: Start the Backend Server

### Option A: Using Startup Script (Recommended)
```bash
# Windows
cd backend
start_server.bat

# Linux/Mac
cd backend
chmod +x start_server.sh
./start_server.sh
```

### Option B: Manual Start
```bash
cd backend
python main.py
```

You should see:
```
==================================================
  L-mobile Chatbot API Server
==================================================
[INFO] Loaded 126 images
[INFO] Loaded 307851 characters of text
[INFO] Starting server on http://localhost:8000
==================================================
```

**Keep this terminal window open!** The server needs to run while you use the chatbot.

## Step 2: Install Chrome Extension

1. Open Chrome browser
2. Go to `chrome://extensions/`
3. Enable **"Developer mode"** (toggle in top right)
4. Click **"Load unpacked"**
5. Select the `chatbot-extension` folder from this project
6. You should see "Chatbot Extension" installed

## Step 3: Use the Chatbot!

1. **Navigate to any webpage** (e.g., Google, GitHub, etc.)
2. **Look for the green chat bubble** (💬) at the bottom right
3. **Click the bubble** to open the chat panel
4. **Ask questions!**

### Example Questions:

**Text-based queries:**
```
"What is the development environment setup?"
"How do I use HG/Mercurial?"
"What are the branching strategies?"
"Tell me about release targets"
```

**Image-related queries:**
```
"Show me database diagrams"
"What do the parameters look like?"
"Explain the architecture"
```

## How It Works

### Backend (FastAPI + OpenAI)
1. Loads all documentation text and images on startup
2. When you ask a question:
   - Finds relevant text sections using keyword matching
   - Finds relevant images based on filenames
   - Sends both to OpenAI GPT-4 Vision
   - Returns the AI's response

### Frontend (Chrome Extension)
1. Adds a draggable chat bubble to every webpage
2. Sends your questions to the backend
3. Displays AI responses in a chat interface
4. Shows which images were used in the response

## API Endpoints

The backend provides these endpoints:

- `GET /` - Health check and statistics
- `POST /chat` - Main chatbot endpoint
- `GET /images/summary` - Summary of available images
- `GET /data/stats` - Data loading statistics

### Test the API directly:

```bash
# Health check
curl http://localhost:8000/

# Get stats
curl http://localhost:8000/data/stats

# Chat (example)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is this documentation about?"}]}'
```

## Troubleshooting

### "Failed to connect to chatbot server"
**Problem:** Extension can't reach the backend
**Solution:** 
- Make sure backend is running on http://localhost:8000
- Check the terminal for errors
- Try restarting the backend

### "API Error" or "Rate Limit"
**Problem:** OpenAI API issues
**Solution:**
- Check your API key in `backend/cle.env`
- Verify you have credits at https://platform.openai.com/usage
- The model used is `gpt-4o-mini` (cheaper option)

### Extension not appearing
**Problem:** Extension not loaded properly
**Solution:**
- Check `chrome://extensions/` for errors
- Click "Reload" on the extension
- Try removing and re-adding the extension

### No images in responses
**Problem:** Images not being found
**Solution:**
- Images are selected based on filename matching
- Try more specific questions that match image names
- Check backend logs to see which images were found

## Features

### Chat Bubble
- 🔹 **Draggable** - Click and drag to reposition
- 🔹 **Persistent** - Stays on all web pages
- 🔹 **Minimizable** - Click to show/hide chat panel

### Chat Panel
- 🔹 **Draggable** - Drag by header to reposition
- 🔹 **Conversation History** - Keeps last 10 messages
- 🔹 **Image Context** - Shows when images are used
- 🔹 **Modern UI** - Clean, professional design

### AI Capabilities
- 🔹 **Text Understanding** - Searches through 300K+ characters
- 🔹 **Image Analysis** - GPT-4 Vision processes diagrams/screenshots
- 🔹 **Context-Aware** - Maintains conversation history
- 🔹 **Smart Matching** - Finds relevant sections automatically

## Data Sources

The chatbot uses:
- ✅ `output_text.txt` - Full documentation text
- ✅ `images_extraites/` - All extracted PDF images
- ✅ `images_nommees/` - Images with descriptive names
- ✅ `images_simples/` - Simple extracted images
- ✅ `images_titre_associe/` - Images with associated titles

## Cost Considerations

This project uses OpenAI's API:
- **Model:** `gpt-4o-mini` (optimized for cost)
- **Image Detail:** Low (to reduce costs)
- **Token Limits:** 500 max tokens per response

**Estimated costs:**
- Text-only queries: ~$0.001 per request
- With images: ~$0.003-0.005 per request

Monitor your usage at: https://platform.openai.com/usage

## Next Steps

1. ✅ **Customize the UI** - Edit `chatbot-extension/style.css`
2. ✅ **Adjust AI behavior** - Modify system prompt in `backend/main.py`
3. ✅ **Add more data** - Update `output_text.txt` or add image folders
4. ✅ **Improve matching** - Enhance keyword matching in `data_loader.py`

## Security Notes

⚠️ **Important:**
- Never commit `cle.env` or `.env` files to Git
- The `.gitignore` file protects these files
- Backend uses CORS `*` for development - tighten for production
- Keep your API key secret!

## Support

If you have issues:
1. Run `python backend/test_setup.py` to diagnose problems
2. Check backend logs for errors
3. Check Chrome console (F12) for frontend errors
4. Verify API key and credits

---

**Enjoy your AI-powered documentation assistant!** 🎉

