/**
 * Content script for Chatbot Extension
 * Creates floating chat bubble and panel interface
 */

console.log("✅ Chatbot content script loaded");

// Conversation history
let conversationHistory = [];

// === Create Chat Bubble ===
const bubble = document.createElement("div");
bubble.id = "chatbot-bubble";
bubble.textContent = "💬";
bubble.title = "Click to open chatbot";
document.body.appendChild(bubble);

// === Create Chat Panel ===
const panel = document.createElement("div");
panel.id = "chatbot-panel";
panel.innerHTML = `
  <div id="chatbot-header" style="background:#4CAF50; color:white; padding:10px; font-weight:bold; text-align:center; cursor:move;">
    🤖 L-mobile Documentation Assistant
    <button id="chatbot-close" style="float:right; background:transparent; border:none; color:white; cursor:pointer; font-size:18px;">×</button>
  </div>
  <div id="chatbot-status" style="padding:5px; background:#e8f5e9; font-size:11px; text-align:center; display:none;">
    Connecting...
  </div>
  <div id="chatbot-body" style="flex:1; padding:10px; overflow-y:auto; background:#f5f5f5; min-height:200px;">
    <div class="chatbot-message bot-message">
      👋 Hello! I'm your L-mobile documentation assistant. Ask me anything about the documentation!
    </div>
  </div>
  <div id="chatbot-input-container" style="display:flex !important; border-top:1px solid #ccc; background:white; flex-shrink:0;">
    <input 
      id="chatbot-input" 
      placeholder="Ask about the documentation..." 
      style="flex:1; border:none; padding:12px 15px; font-size:14px; outline:none; min-width:200px;" 
    />
    <button id="chatbot-send" style="background:#4CAF50; color:white; border:none; padding:12px 20px; cursor:pointer; font-weight:bold; flex-shrink:0;">
      Send
    </button>
  </div>
`;
document.body.appendChild(panel);

// === Helper Functions ===

function appendMessage(content, isUser = false, metadata = {}) {
  const body = panel.querySelector("#chatbot-body");
  const msgDiv = document.createElement("div");
  msgDiv.className = isUser ? "chatbot-message user-message" : "chatbot-message bot-message";
  
  // Main content
  const textDiv = document.createElement("div");
  textDiv.textContent = content;
  msgDiv.appendChild(textDiv);
  
  // Add metadata (images used, etc.)
  if (metadata.images_used && metadata.images_used.length > 0) {
    const metaDiv = document.createElement("div");
    metaDiv.style.cssText = "font-size:10px; color:#666; margin-top:5px; font-style:italic;";
    metaDiv.textContent = `📷 Referenced ${metadata.images_used.length} image(s)`;
    msgDiv.appendChild(metaDiv);
  }
  
  body.appendChild(msgDiv);
  body.scrollTop = body.scrollHeight;
}

function showStatus(message, isError = false) {
  const status = panel.querySelector("#chatbot-status");
  status.textContent = message;
  status.style.display = "block";
  status.style.background = isError ? "#ffebee" : "#e8f5e9";
  status.style.color = isError ? "#c62828" : "#2e7d32";
  
  // Auto-hide after 3 seconds
  setTimeout(() => {
    status.style.display = "none";
  }, 3000);
}

function setLoading(isLoading) {
  const input = panel.querySelector("#chatbot-input");
  const sendBtn = panel.querySelector("#chatbot-send");
  
  input.disabled = isLoading;
  sendBtn.disabled = isLoading;
  sendBtn.textContent = isLoading ? "⏳" : "Send";
  
  if (isLoading) {
    showStatus("Thinking...");
  }
}

async function sendMessage(userMessage) {
  if (!userMessage.trim()) return;
  
  // Add user message to UI
  appendMessage(userMessage, true);
  
  // Add to conversation history
  conversationHistory.push({
    role: "user",
    content: userMessage
  });
  
  // Clear input
  panel.querySelector("#chatbot-input").value = "";
  
  // Set loading state
  setLoading(true);
  
  try {
    // Send to background script
    const response = await new Promise((resolve) => {
      chrome.runtime.sendMessage(
        {
          type: "CHAT_REQUEST",
          messages: conversationHistory,
          use_images: true,
          max_images: 2
        },
        (res) => resolve(res)
      );
    });
    
    setLoading(false);
    
    if (response.ok) {
      // Add assistant response
      const botMessage = response.content;
      appendMessage(botMessage, false, {
        images_used: response.images_used
      });
      
      // Add to conversation history
      conversationHistory.push({
        role: "assistant",
        content: botMessage
      });
      
      // Keep only last 10 messages to avoid context overflow
      if (conversationHistory.length > 10) {
        conversationHistory = conversationHistory.slice(-10);
      }
    } else {
      showStatus(response.message || "Error: " + response.error, true);
      appendMessage(
        "⚠️ " + (response.message || "Sorry, I couldn't connect to the server. Please make sure the backend is running."), 
        false
      );
    }
  } catch (error) {
    setLoading(false);
    showStatus("Connection error", true);
    appendMessage("⚠️ Connection error. Please check if the backend server is running.", false);
  }
}

// === Event Listeners ===

// Toggle panel on bubble click
bubble.addEventListener("click", () => {
  const isVisible = panel.style.display === "flex";
  panel.style.display = isVisible ? "none" : "flex";
  
  if (!isVisible) {
    // Position panel near bubble
    const rect = bubble.getBoundingClientRect();
    const spaceRight = window.innerWidth - rect.right;
    const left = spaceRight > 340 ? rect.right + 10 : rect.left - 330;
    const top = Math.min(window.innerHeight - 450, rect.top);
    
    panel.style.left = `${Math.max(10, left)}px`;
    panel.style.top = `${Math.max(10, top)}px`;
    
    // Focus input
    setTimeout(() => panel.querySelector("#chatbot-input").focus(), 100);
  }
});

// Close button
panel.querySelector("#chatbot-close").addEventListener("click", (e) => {
  e.stopPropagation();
  panel.style.display = "none";
});

// Send message on button click
panel.querySelector("#chatbot-send").addEventListener("click", () => {
  const input = panel.querySelector("#chatbot-input");
  sendMessage(input.value);
});

// Send message on Enter key
panel.querySelector("#chatbot-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage(e.target.value);
  }
});

// === Drag Bubble ===
let isDraggingBubble = false;
bubble.addEventListener("mousedown", (e) => {
  const startX = e.clientX;
  const startY = e.clientY;
  const rect = bubble.getBoundingClientRect();
  const offsetX = startX - rect.left;
  const offsetY = startY - rect.top;
  
  function move(ev) {
    const dx = Math.abs(ev.clientX - startX);
    const dy = Math.abs(ev.clientY - startY);
    
    // Only start dragging if moved more than 5px
    if (dx > 5 || dy > 5) {
      isDraggingBubble = true;
      bubble.style.left = `${ev.clientX - offsetX}px`;
      bubble.style.top = `${ev.clientY - offsetY}px`;
      bubble.style.right = "auto";
      bubble.style.bottom = "auto";
    }
  }
  
  function up() {
    document.removeEventListener("mousemove", move);
    document.removeEventListener("mouseup", up);
    
    // Prevent click event if we were dragging
    if (isDraggingBubble) {
      setTimeout(() => { isDraggingBubble = false; }, 100);
    }
  }
  
  document.addEventListener("mousemove", move);
  document.addEventListener("mouseup", up);
});

// Prevent opening panel when dragging
bubble.addEventListener("click", (e) => {
  if (isDraggingBubble) {
    e.stopPropagation();
  }
});

// === Drag Panel by Header ===
const header = panel.querySelector("#chatbot-header");
let isDraggingPanel = false;

header.addEventListener("mousedown", (e) => {
  if (e.target.id === "chatbot-close") return; // Don't drag when clicking close
  
  isDraggingPanel = true;
  const rect = panel.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;
  
  function move(ev) {
    if (!isDraggingPanel) return;
    panel.style.left = ev.clientX - offsetX + "px";
    panel.style.top = ev.clientY - offsetY + "px";
  }
  
  function up() {
    isDraggingPanel = false;
    document.removeEventListener("mousemove", move);
    document.removeEventListener("mouseup", up);
  }
  
  document.addEventListener("mousemove", move);
  document.addEventListener("mouseup", up);
});

// === Health Check on Load ===
setTimeout(() => {
  chrome.runtime.sendMessage({ type: "HEALTH_CHECK" }, (response) => {
    if (response?.ok) {
      console.log("✅ Backend connected:", response.data);
    } else {
      console.warn("⚠️ Backend not available. Make sure to run: python backend/main.py");
    }
  });
}, 1000);
