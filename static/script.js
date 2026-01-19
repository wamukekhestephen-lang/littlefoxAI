const chatBox = document.getElementById("chatBox");
const input = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const emptyState = document.querySelector(".empty-state");
const modeBtn = document.getElementById("modeBtn");
let currentChat = null;
let currentMode = "online";
let searchActive = false;

/* =====================
   INITIALIZE
===================== */
document.addEventListener("DOMContentLoaded", () => {
  loadChats();
  loadMode();
  setupModeToggle();
  setupNavigationButtons();
  setupClearHistoryButton();
});

function setupModeToggle() {
  if (modeBtn) {
    modeBtn.addEventListener("click", toggleMode);
  }
}

async function loadMode() {
  try {
    const res = await fetch("/mode");
    const data = await res.json();
    currentMode = data.mode;
    updateModeButton();
  } catch (e) {
    console.error("Failed to load mode:", e);
  }
}

async function toggleMode() {
  currentMode = currentMode === "online" ? "offline" : "online";
  
  try {
    const res = await fetch("/mode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: currentMode })
    });
    
    if (res.ok) {
      updateModeButton();
    }
  } catch (e) {
    console.error("Failed to toggle mode:", e);
  }
}

function updateModeButton() {
  if (currentMode === "online") {
    modeBtn.textContent = "🔵 Online";
    modeBtn.classList.remove("offline");
    modeBtn.classList.add("online");
  } else {
    modeBtn.textContent = "🔴 Offline";
    modeBtn.classList.remove("online");
    modeBtn.classList.add("offline");
  }
}

/* =====================
   SETUP NAVIGATION BUTTONS
===================== */
function setupNavigationButtons() {
  const navItems = document.querySelectorAll(".nav-item[data-action]");
  
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const action = item.getAttribute("data-action");
      handleNavAction(action);
    });
  });
}

function handleNavAction(action) {
  switch(action) {
    case "new-chat":
      createNewChat();
      break;
    case "search":
      toggleSearchChats();
      break;
    case "images":
      showFeature("Images");
      break;
    case "apps":
      showFeature("Apps");
      break;
    case "projects":
      showFeature("Projects");
      break;
    default:
      console.log("Unknown action:", action);
  }
}

function createNewChat() {
  currentChat = crypto.randomUUID();
  chatBox.innerHTML = "";
  input.value = "";
  emptyState.style.display = "flex";
  chatBox.classList.remove("active");
  searchActive = false;
  input.focus();
}

function toggleSearchChats() {
  searchActive = !searchActive;
  
  if (searchActive) {
    input.placeholder = "🔍 Search chats...";
    input.focus();
  } else {
    input.placeholder = "+ Ask anything";
    input.value = "";
    loadChats();
  }
}

function showFeature(feature) {
  const featureMsg = `<strong>${feature} feature</strong> is coming soon! 🚀`;
  emptyState.style.display = "none";
  chatBox.innerHTML = "";
  
  const msg = document.createElement("div");
  msg.className = "message assistant";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = featureMsg;
  msg.appendChild(bubble);
  chatBox.appendChild(msg);
  chatBox.classList.add("active");
}

function setupClearHistoryButton() {
  const clearBtn = document.getElementById("clearHistoryBtn");
  if (clearBtn) {
    clearBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      if (confirm("Are you sure you want to delete all chats? This cannot be undone.")) {
        try {
          // Delete all chats from database
          const res = await fetch("/chats");
          const chats = await res.json();
          
          for (const [id] of chats) {
            await fetch(`/delete/${id}`, { method: "DELETE" });
          }
          
          loadChats();
          createNewChat();
        } catch (e) {
          console.error("Error clearing history:", e);
        }
      }
    });
  }
}

/* =====================
   LOAD CHAT LIST
===================== */
async function loadChats() {
  const res = await fetch("/chats");
  const chats = await res.json();

  const list = document.getElementById("chatList");
  list.innerHTML = "";

  if (chats.length === 0) {
    list.innerHTML = '<div class="empty-history">No chats yet</div>';
    return;
  }

  chats.forEach(([id, title]) => {
    const item = document.createElement("div");
    item.className = "chat-item";
    
    // Truncate long titles for better display
    const displayTitle = title.length > 40 ? title.substring(0, 40) + "..." : title;
    
    const textSpan = document.createElement("span");
    textSpan.className = "chat-item-text";
    textSpan.innerText = displayTitle;
    textSpan.title = title;
    textSpan.addEventListener("click", () => loadChat(id));
    
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "chat-item-delete";
    deleteBtn.innerText = "✕";
    deleteBtn.title = "Delete chat";
    deleteBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      deleteChat(id, title);
    });
    
    item.appendChild(textSpan);
    item.appendChild(deleteBtn);
    list.appendChild(item);
  });
}

/* =====================
   DELETE CHAT
===================== */
async function deleteChat(id, title) {
  if (confirm(`Delete chat "${title}"?`)) {
    try {
      const res = await fetch(`/delete/${id}`, { method: "DELETE" });
      if (res.ok) {
        loadChats();
        if (currentChat === id) {
          createNewChat();
        }
      }
    } catch (e) {
      console.error("Error deleting chat:", e);
    }
  }
}

/* =====================
   LOAD SPECIFIC CHAT
===================== */
async function loadChat(id) {
  if (searchActive) {
    searchActive = false;
    input.placeholder = "+ Ask anything";
    input.value = "";
  }
  
  currentChat = id;
  chatBox.innerHTML = "";

  const res = await fetch(`/history/${id}`);
  const messages = await res.json();

  messages.forEach(([role, text]) => {
    addMessage(role, text);
  });
}

/* =====================
   ADD MESSAGE FUNCTION
===================== */
function addMessage(role, text, stream = false) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  
  // For assistant messages, render formatted HTML; for user, plain text
  if (role === "assistant") {
    bubble.innerHTML = markdownToHtml(text);
  } else {
    bubble.innerText = text;
  }

  if (stream) bubble.id = "streaming";

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.classList.add("active");
  emptyState.style.display = "none";
  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble;
}

/* =====================
   MARKDOWN TO HTML CONVERTER
===================== */
function markdownToHtml(text) {
  let html = text;

  // Escape HTML but preserve markdown syntax temporarily
  html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Code blocks (```language\ncode\n```)
  html = html.replace(/```(\w+)?\n([\s\S]*?)\n```/g, (match, lang, code) => {
    const trimmed = code.trim();
    // Escape code content
    let escaped = trimmed
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    return `<pre><code class="language-${lang || 'plain'}">${escaped}</code></pre>`;
  });

  // Inline code (`code`)
  html = html.replace(/`([^`]+)`/g, (match, code) => {
    const escaped = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return `<code>${escaped}</code>`;
  });

  // Headings (# to ######)
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");
  html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
  html = html.replace(/^##### (.+)$/gm, "<h5>$1</h5>");
  html = html.replace(/^###### (.+)$/gm, "<h6>$1</h6>");

  // Bold (**text** or __text__)
  html = html.replace(/\*\*([^\*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/__([^_]+)__/g, "<strong>$1</strong>");

  // Italic (*text* or _text_)
  html = html.replace(/\*([^\*]+)\*/g, "<em>$1</em>");
  html = html.replace(/_([^_]+)_/g, "<em>$1</em>");

  // Numbered lists (1. item -> <ol>)
  html = html.replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>[\s\S]*<\/li>)/s, (match) => {
    if (!match.includes("<ol>") && !match.includes("<ul>")) {
      return `<ol>${match}</ol>`;
    }
    return match;
  });

  // Bullet lists (- or * item)
  html = html.replace(/^[\-\*]\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>[\s\S]*?<\/li>)/s, (match) => {
    if (!match.includes("<ol>") && !match.includes("<ul>")) {
      return `<ul>${match}</ul>`;
    }
    return match;
  });

  // Blockquotes (> text)
  html = html.replace(/^&gt;\s(.+)$/gm, "<blockquote>$1</blockquote>");

  // Line breaks
  html = html.split("\n").map(line => {
    const trimmed = line.trim();
    if (!trimmed) return "";
    if (trimmed.match(/^<[h1-6p]|^<pre|^<blockquote|^<[ou]l|^<li/)) {
      return line;
    }
    return `<p>${line}</p>`;
  }).filter(Boolean).join("\n");

  return html;
}

/* =====================
   QUICK ACTION BUTTONS
===================== */
document.addEventListener("DOMContentLoaded", () => {
  const quickBtns = document.querySelectorAll(".quick-btn");
  
  quickBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.getAttribute("data-action");
      handleQuickAction(action);
    });
  });
});

function handleQuickAction(action) {
  const prompts = {
    "code": "Generate a simple Python script that prints a greeting",
    "explain": "Explain the concept of machine learning in simple terms",
    "creative": "Write a short creative story about an AI discovering consciousness",
    "analyze": "Analyze the pros and cons of remote work"
  };
  
  if (prompts[action]) {
    input.value = prompts[action];
    input.focus();
    input.dispatchEvent(new Event("input"));
  }
}

/* =====================
   UPDATE SEND MESSAGE
===================== */
async function sendMessage() {
  const text = input.value.trim();
  
  // Handle search mode
  if (searchActive) {
    const searchTerm = text.toLowerCase();
    const res = await fetch("/chats");
    const chats = await res.json();
    
    const list = document.getElementById("chatList");
    list.innerHTML = "";
    
    const filtered = chats.filter(([_, title]) => title.toLowerCase().includes(searchTerm));
    
    if (filtered.length === 0) {
      list.innerHTML = '<div class="empty-history">No matching chats</div>';
      return;
    }
    
    filtered.forEach(([id, title]) => {
      const item = document.createElement("div");
      item.className = "chat-item";
      
      const displayTitle = title.length > 40 ? title.substring(0, 40) + "..." : title;
      
      const textSpan = document.createElement("span");
      textSpan.className = "chat-item-text";
      textSpan.innerText = displayTitle;
      textSpan.title = title;
      textSpan.addEventListener("click", () => loadChat(id));
      
      const deleteBtn = document.createElement("button");
      deleteBtn.className = "chat-item-delete";
      deleteBtn.innerText = "✕";
      deleteBtn.title = "Delete chat";
      deleteBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteChat(id, title);
      });
      
      item.appendChild(textSpan);
      item.appendChild(deleteBtn);
      list.appendChild(item);
    });
    return;
  }
  
  if (!text) return;

  if (!currentChat) {
    currentChat = crypto.randomUUID();
  }

  input.value = "";
  emptyState.style.display = "none";
  
  addMessage("user", text);
  const assistantBubble = addMessage("assistant", "", true);

  // Show thinking indicator
  const thinkingIndicator = document.getElementById("thinkingIndicator");
  if (thinkingIndicator) {
    thinkingIndicator.classList.add("show");
  }

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, chat_id: currentChat })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    // Handle Server-Sent Events stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      
      // Process complete lines
      for (let i = 0; i < lines.length - 1; i++) {
        const line = lines[i].trim();
        
        if (line.startsWith("data: ")) {
          const data = line.substring(6);
          
          try {
            const event = JSON.parse(data);
            
            if (event.type === "text") {
              // Add text chunk
              fullText += event.text;
              assistantBubble.innerHTML = markdownToHtml(fullText);
              
              // Apply syntax highlighting
              assistantBubble.querySelectorAll("pre code").forEach((block) => {
                hljs.highlightElement(block);
              });
              
              chatBox.scrollTop = chatBox.scrollHeight;
            } else if (event.type === "status") {
              // Show status message (like "searching web") - optional logging
              console.log("Status:", event.text);
            } else if (event.type === "done") {
              // Stream complete
              break;
            }
          } catch (e) {
            console.error("Parse error:", e);
          }
        }
      }
      
      // Keep incomplete line in buffer
      buffer = lines[lines.length - 1];
    }

    // Hide thinking indicator
    if (thinkingIndicator) {
      thinkingIndicator.classList.remove("show");
    }

    assistantBubble.removeAttribute("id");
    loadChats();
  } catch (error) {
    console.error("Error:", error);
    assistantBubble.innerHTML = "<strong>Sorry, an error occurred. Please try again.</strong>";
    
    // Hide thinking indicator
    if (thinkingIndicator) {
      thinkingIndicator.classList.remove("show");
    }
  }
}

/* =====================
   INPUT ICON BUTTONS
===================== */
document.addEventListener("DOMContentLoaded", () => {
  const inputIcons = document.querySelectorAll(".input-icons .icon-btn[data-action]");
  
  inputIcons.forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.getAttribute("data-action");
      
      if (action === "voice") {
        console.log("Voice input - coming soon");
      } else if (action === "attach") {
        console.log("File attachment - coming soon");
      }
    });
  });
});

/* =====================
   EVENTS
===================== */
if (sendBtn) {
  sendBtn.addEventListener("click", sendMessage);
}

if (input) {
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

/* =====================
   LOAD CHAT
===================== */
async function loadChat(id) {
  currentChat = id;
  chatBox.innerHTML = "";

  const res = await fetch(`/history/${id}`);
  const messages = await res.json();

  messages.forEach(([role, text]) => {
    addMessage(role, text);
  });
}
/* =====================
   ADD MESSAGE FUNCTION
===================== */
function addMessage(role, text, stream = false) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  
  // For assistant messages, render formatted HTML; for user, plain text
  if (role === "assistant") {
    bubble.innerHTML = markdownToHtml(text);
  } else {
    bubble.innerText = text;
  }

  if (stream) bubble.id = "streaming";

  msg.appendChild(bubble);
  chatBox.appendChild(msg);

  chatBox.classList.add("active");
  chatBox.scrollTop = chatBox.scrollHeight;

  return bubble;
}

/* =====================
   MARKDOWN TO HTML CONVERTER
===================== */
function markdownToHtml(text) {
  let html = text;

  // Escape HTML but preserve markdown syntax temporarily
  html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Code blocks (```language\ncode\n```)
  html = html.replace(/```(\w+)?\n([\s\S]*?)\n```/g, (match, lang, code) => {
    const trimmed = code.trim();
    // Escape code content
    let escaped = trimmed
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    return `<pre><code class="language-${lang || 'plain'}">${escaped}</code></pre>`;
  });

  // Inline code (`code`)
  html = html.replace(/`([^`]+)`/g, (match, code) => {
    const escaped = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return `<code>${escaped}</code>`;
  });

  // Headings (# to ######)
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");
  html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
  html = html.replace(/^##### (.+)$/gm, "<h5>$1</h5>");
  html = html.replace(/^###### (.+)$/gm, "<h6>$1</h6>");

  // Bold (**text** or __text__)
  html = html.replace(/\*\*([^\*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/__([^_]+)__/g, "<strong>$1</strong>");

  // Italic (*text* or _text_)
  html = html.replace(/\*([^\*]+)\*/g, "<em>$1</em>");
  html = html.replace(/_([^_]+)_/g, "<em>$1</em>");

  // Numbered lists (1. item -> <ol>)
  html = html.replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>[\s\S]*<\/li>)/s, (match) => {
    if (!match.includes("<ol>") && !match.includes("<ul>")) {
      return `<ol>${match}</ol>`;
    }
    return match;
  });

  // Bullet lists (- or * item)
  html = html.replace(/^[\-\*]\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>[\s\S]*?<\/li>)/s, (match) => {
    if (!match.includes("<ol>") && !match.includes("<ul>")) {
      return `<ul>${match}</ul>`;
    }
    return match;
  });

  // Blockquotes (> text)
  html = html.replace(/^&gt;\s(.+)$/gm, "<blockquote>$1</blockquote>");

  // Line breaks
  html = html.split("\n").map(line => {
    const trimmed = line.trim();
    if (!trimmed) return "";
    if (trimmed.match(/^<[h1-6p]|^<pre|^<blockquote|^<[ou]l|^<li/)) {
      return line;
    }
    return `<p>${line}</p>`;
  }).filter(Boolean).join("\n");

  return html;
}
/* =====================
   UPDATE SEND MESSAGE
===================== */
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  if (!currentChat) {
    currentChat = crypto.randomUUID();
  }

  input.value = "";
  emptyState.style.display = "none";
  
  addMessage("user", text);
  const assistantBubble = addMessage("assistant", "", true);

  // Show thinking indicator
  const thinkingIndicator = document.getElementById("thinkingIndicator");
  if (thinkingIndicator) {
    thinkingIndicator.classList.add("show");
  }

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, chat_id: currentChat })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    // Handle Server-Sent Events stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      
      // Process complete lines
      for (let i = 0; i < lines.length - 1; i++) {
        const line = lines[i].trim();
        
        if (line.startsWith("data: ")) {
          const data = line.substring(6);
          
          try {
            const event = JSON.parse(data);
            
            if (event.type === "text") {
              // Add text chunk
              fullText += event.text;
              assistantBubble.innerHTML = markdownToHtml(fullText);
              
              // Apply syntax highlighting
              assistantBubble.querySelectorAll("pre code").forEach((block) => {
                hljs.highlightElement(block);
              });
              
              chatBox.scrollTop = chatBox.scrollHeight;
            } else if (event.type === "status") {
              // Show status message (like "searching web") - optional logging
              console.log("Status:", event.text);
            } else if (event.type === "done") {
              // Stream complete
              break;
            }
          } catch (e) {
            console.error("Parse error:", e);
          }
        }
      }
      
      // Keep incomplete line in buffer
      buffer = lines[lines.length - 1];
    }

    // Hide thinking indicator
    if (thinkingIndicator) {
      thinkingIndicator.classList.remove("show");
    }

    assistantBubble.removeAttribute("id");
    loadChats();
  } catch (error) {
    console.error("Error:", error);
    assistantBubble.innerHTML = "<strong>Sorry, an error occurred. Please try again.</strong>";
    
    // Hide thinking indicator
    if (thinkingIndicator) {
      thinkingIndicator.classList.remove("show");
    }
  }
}

/* =====================
   EVENTS
===================== */
if (sendBtn) {
  sendBtn.addEventListener("click", sendMessage);
}

if (input) {
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}
