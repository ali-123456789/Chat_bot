chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg?.type === "CHAT_REQUEST") {
      fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "openai/gpt-oss-20b:free",
          messages: msg.messages,
          top_k: 4
        })
      })
        .then((r) => r.json())
        .then((data) => sendResponse({ ok: true, content: data.content }))
        .catch((err) => sendResponse({ ok: false, error: String(err) }));
  
      return true; // réponse async
    }
  });
  