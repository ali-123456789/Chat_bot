console.log("✅ Chatbot loaded");

const bubble = document.createElement("div");
bubble.id = "chatbot-bubble";
bubble.textContent = "💬";
document.body.appendChild(bubble);

// === Panel ===
const panel = document.createElement("div");
panel.id = "chatbot-panel";
panel.innerHTML = `
  <div id="chatbot-header" style="background:#4CAF50; color:white; padding:10px; font-weight:bold; text-align:center; cursor:move;">
    🤖 ChatBot
  </div>
  <div id="chatbot-body" style="flex:1; padding:10px; overflow-y:auto;">
    <div style="background:#f1f1f1; margin-bottom:8px; padding:6px 10px; border-radius:5px;">
      Bonjour ! Comment puis-je vous aider ?
    </div>
  </div>
  <input id="chatbot-input" placeholder="Écrivez ici..." style="border:none; border-top:1px solid #ccc; padding:10px; width:100%; box-sizing:border-box; font-size:14px;" />
`;
document.body.appendChild(panel);

// === Toggle panel on click ===
bubble.addEventListener("click", () => {
  const isVisible = panel.style.display === "flex";
  panel.style.display = isVisible ? "none" : "flex";

  if (!isVisible) {
    const rect = bubble.getBoundingClientRect();
    const spaceRight = window.innerWidth - rect.right;
    const left = spaceRight > 340 ? rect.right + 10 : rect.left - 330;
    const top = Math.min(window.innerHeight - 410, rect.top);

    panel.style.left = `${Math.max(10, left)}px`;
    panel.style.top = `${Math.max(10, top)}px`;
  }
});

// === Drag bubble ===
let isDragging = false;
bubble.addEventListener("mousedown", (e) => {
  let offsetX = e.clientX - bubble.getBoundingClientRect().left;
  let offsetY = e.clientY - bubble.getBoundingClientRect().top;

  function move(ev) {
    isDragging = true;
    bubble.style.left = `${ev.clientX - offsetX}px`;
    bubble.style.top = `${ev.clientY - offsetY}px`;
    bubble.style.right = "auto";
    bubble.style.bottom = "auto";
  }

  function up() {
    document.removeEventListener("mousemove", move);
    document.removeEventListener("mouseup", up);
  }

  document.addEventListener("mousemove", move);
  document.addEventListener("mouseup", up);
});

// === Drag panel by header ===
let draggingPanel = false;
const header = panel.querySelector("#chatbot-header");
header.addEventListener("mousedown", (e) => {
  draggingPanel = true;
  const rect = panel.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;

  function move(ev) {
    if (!draggingPanel) return;
    panel.style.left = ev.clientX - offsetX + "px";
    panel.style.top = ev.clientY - offsetY + "px";
    panel.style.right = "auto";
    panel.style.bottom = "auto";
  }

  function up() {
    draggingPanel = false;
    document.removeEventListener("mousemove", move);
    document.removeEventListener("mouseup", up);
  }
  function askFromFile(userText) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(
        { type: "CHAT_REQUEST", messages: [{ role: "user", content: userText }] },
        (res) => resolve(res)
      );
    });
  }
  
  // Exemple au submit de ton formulaire
  async function onSend(text) {
    appendUserMessage(text);
    const res = await askFromFile(text);
    appendAssistantMessage(res?.ok ? res.content : "Erreur: " + (res?.error || "inconnue"));
  }
  

  document.addEventListener("mousemove", move);
  document.addEventListener("mouseup", up);
});

// === Send message ===
panel.querySelector("#chatbot-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const input = e.target;
    const msg = input.value.trim();
    if (!msg) return;
    const body = panel.querySelector("#chatbot-body");
    const msgDiv = document.createElement("div");
    msgDiv.textContent = msg;
    msgDiv.style.cssText = "background:#f1f1f1; margin-bottom:8px; padding:6px 10px; border-radius:5px;";
    body.appendChild(msgDiv);
    input.value = "";
    body.scrollTop = body.scrollHeight;
  }
});
