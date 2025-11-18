# 🤖 L-mobile Documentation Chatbot

An AI-powered chatbot that helps you navigate and query L-mobile developer documentation using OpenAI's GPT-4 Vision model. The chatbot can understand both text and images from the documentation.

## 📋 Features

- 🔍 **Smart Context Search**: Automatically finds relevant sections from documentation
- 🖼️ **Image Processing**: Analyzes images from documentation to provide visual context
- 💬 **Browser Extension**: Accessible from any webpage via a floating chat bubble
- 🎯 **Multi-source Data**: Queries across multiple image folders and text files
- 🔐 **Secure API Key Management**: Uses environment variables for API keys

## 🏗️ Project Structure

```
Chat_bot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── data_loader.py       # Loads images and text data
│   ├── requirements.txt     # Python dependencies
│   ├── cle.env             # API key configuration
│   └── structured_output.txt
├── chatbot-extension/
│   ├── manifest.json        # Chrome extension config
│   ├── background.js        # Service worker for API calls
│   ├── content.js          # UI and chat interface
│   ├── style.css           # Styling
│   ├── output_text.txt     # Documentation text
│   ├── images_extraites/   # Extracted images
│   ├── images_nommees/     # Named images with descriptions
│   ├── images_simples/     # Simple extracted images
│   └── images_titre_associe/ # Images with associated titles
```

## 🚀 Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key

Make sure your OpenAI API key is in `backend/cle.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

### 3. Start the Backend Server

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

You should see:
```
🚀 Starting Chatbot API server...
📊 Loaded X images
📄 Loaded X characters of text
```

### 4. Install Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `chatbot-extension` folder
5. The chatbot icon should appear in your extensions

### 5. Use the Chatbot

1. Navigate to any webpage
2. Look for the green chat bubble (💬) on the bottom right
3. Click it to open the chat panel
4. Ask questions about the L-mobile documentation!

## 💡 Usage Examples

**Text-based questions:**
- "What is the purpose of this documentation?"
- "How do I set up the development environment?"
- "What are the branching strategies?"

**Image-related questions:**
- "Show me the database schema"
- "What do the workflow diagrams look like?"
- "Explain the architecture diagram"

## 🔧 API Endpoints

### `GET /`
Health check and data statistics

### `POST /chat`
Main chat endpoint

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Your question"}
  ],
  "use_images": true,
  "max_images": 2
}
```

**Response:**
```json
{
  "content": "AI response",
  "images_used": ["image1.png"],
  "source": "openai"
}
```

### `GET /images/summary`
Get summary of available images

### `GET /data/stats`
Get statistics about loaded data

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **OpenAI API**: GPT-4 Vision for text + image understanding
- **Python-dotenv**: Environment variable management
- **Pydantic**: Data validation

### Frontend
- **Chrome Extension Manifest V3**: Modern extension API
- **Vanilla JavaScript**: No dependencies
- **Custom CSS**: Modern, responsive design

## 📊 Data Processing

The project includes several Python scripts for PDF processing:

- `extract_text.py`: Extracts text from PDF
- `textestructure.py`: Structures text with markdown
- `imagesextractions.py`: Comprehensive image extraction
- `images.py`: Extracts images with contextual titles

## 🔐 Security Notes

- ⚠️ Never commit your API key to version control
- ⚠️ The `cle.env` file should be added to `.gitignore`
- ⚠️ Backend uses CORS for development (tighten for production)

## 🐛 Troubleshooting

### "Failed to connect to chatbot server"
- Make sure the backend is running on `http://localhost:8000`
- Check that no firewall is blocking the connection
- Verify the API key is correctly set in `cle.env`

### "No images found"
- Ensure image folders are in the correct location
- Check that images were properly extracted from PDF
- Verify folder names match those in `data_loader.py`

### Extension not working
- Check Chrome console for errors (`F12` > Console)
- Reload the extension from `chrome://extensions/`
- Make sure Manifest V3 is supported (Chrome 88+)

## 📝 Future Improvements

- [ ] Add conversation memory/persistence
- [ ] Implement image similarity search
- [ ] Add support for multiple PDF documents
- [ ] Create web UI alternative to extension
- [ ] Add authentication and rate limiting
- [ ] Improve context retrieval with embeddings
- [ ] Support for code snippets highlighting

## 📄 License

This project is for internal use with L-mobile documentation.

## 👥 Author

Created for streamlining developer onboarding and documentation access.

---

**Note**: This chatbot uses OpenAI's API which incurs costs. Monitor your usage at [OpenAI Dashboard](https://platform.openai.com/usage).

