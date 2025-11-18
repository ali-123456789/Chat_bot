/**
 * Background service worker for Chatbot Extension
 * Handles communication between content script and backend API
 */

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === "CHAT_REQUEST") {
    // Send request to FastAPI backend
    fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        messages: msg.messages,
        use_images: msg.use_images !== false,  // Default true
        max_images: msg.max_images || 2
      })
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        sendResponse({ 
          ok: true, 
          content: data.content,
          images_used: data.images_used || [],
          source: data.source
        });
      })
      .catch((err) => {
        console.error("Chat request error:", err);
        sendResponse({ 
          ok: false, 
          error: String(err),
          message: "Failed to connect to chatbot server. Make sure the backend is running on http://localhost:8000"
        });
      });

    return true; // Keep message channel open for async response
  }
  
  if (msg?.type === "HEALTH_CHECK") {
    // Check if backend is running
    fetch("http://localhost:8000/")
      .then((r) => r.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: String(err) }));
    
    return true;
  }
});

// Log when extension is loaded
console.log("🤖 Chatbot extension background service worker loaded");
