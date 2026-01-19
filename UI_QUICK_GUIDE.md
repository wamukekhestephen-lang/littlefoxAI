# 🎯 Frontend UI - Quick Reference Guide

## Navigation Buttons (All Working!)

### Top Sidebar Buttons
```
✏️ New Chat      → Creates new conversation, clears input
🔍 Search Chats  → Filters chat history by search term
🖼️ Images        → Coming soon! (Placeholder ready)
🌐 Apps          → Coming soon! (Placeholder ready)
📁 Projects      → Coming soon! (Placeholder ready)
```

## Mode Toggle
```
🔵 Online        → Uses web search + Ollama (slower, accurate)
🔴 Offline       → Only Ollama local (faster, no internet needed)
```

## Chat History (Bottom Left)

### Header Section
```
💬 Chat History    [✕] Clear all chats
```
- Shows "No chats yet" when empty
- Lists all conversations with timestamps
- Shows most recent chats first

### Chat Item Interaction
```
Click chat     → Load conversation
Hover chat     → Delete button (✕) appears
Click ✕        → Delete with confirmation dialog
```

## Input Area

### Bottom of Screen
```
[Input Box with placeholder "+ Ask anything"]
     [🎤] [📎] [➤ Send Button]
```

- **🎤 Voice** - Coming soon (for voice input)
- **📎 Attach** - Coming soon (for file uploads)
- **➤ Send** - Send message (or press Enter)

### Quick Action Buttons (Below Input)
```
[💻 Code] [📚 Explain] [✨ Creative] [🔍 Analyze]
```
- Click to auto-fill with suggested prompt
- Ready to send or edit

## Features

### Searching Chats
1. Click 🔍 Search Chats
2. Placeholder changes to "🔍 Search chats..."
3. Type to filter conversations
4. Click result to load it

### Deleting Chats
1. **Single Chat**: Hover → Click ✕ → Confirm
2. **All Chats**: Click ✕ in header → Confirm
3. Deleted instantly from UI and database

### Creating Messages
1. Type or click Quick Action button
2. Press Enter or click ➤ Send
3. Message streams in real-time
4. Chat automatically saves to history

## Visual Indicators

### Chat Item States
```
Default:    Light background, text aligned left
Hover:      Slightly brighter background, green left border
Delete:     Red ✕ button visible on hover
```

### Mode Button States
```
Online:     🔵 Blue border and text
Offline:    🔴 Red border and text
```

### Loading States
```
Thinking indicator:  Animated dots "AI is thinking..."
Input disabled:      While waiting for response
Auto-saves:          Chats saved after response
```

## Keyboard Shortcuts

```
Enter                → Send message (Shift+Enter for newline - ready)
Escape               → (Future: Close panels)
Ctrl+K               → (Future: Command palette)
```

## Styling Features

### Dark Theme (Dark Mode)
- Background: Dark gray (#1e1e1e)
- Text: Light gray (#f0f0f0)
- Accents: Green (#10a37f) and Blue (#4a9eff)

### Responsive Layout
- Sidebar: 260px fixed width
- Main chat area: Flexible full width
- Works on desktop (mobile coming soon)

### Smooth Animations
- Button hover effects (0.2s)
- Scroll animations
- Message streaming
- Panel transitions

## Database Operations

### Automatic
- ✅ Message saved on send
- ✅ Chat created on first message
- ✅ Chat title set from first message
- ✅ Timestamps recorded

### Manual (via UI)
- ✅ Delete single chat (instant)
- ✅ Clear all chats (instant)
- ✅ Load chat history (on click)

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Load UI |
| `/ask` | POST | Send message, get response |
| `/chats` | GET | List all chats |
| `/history/<id>` | GET | Load specific chat |
| `/delete/<id>` | DELETE | Remove chat |
| `/mode` | GET/POST | Toggle online/offline |

## Troubleshooting

### Button Not Working?
- Check browser console (F12) for errors
- Reload page (Ctrl+R)
- Ensure Flask server is running

### Chat Not Saving?
- Check Flask logs for errors
- Verify database file exists (chat_history.db)
- Check browser network tab

### Slow Response?
- Normal for first query (30-60s on 4GB RAM)
- Subsequent queries faster (10-30s)
- Check Ollama is running (`ollama list`)

### Delete Doesn't Work?
- Confirm confirmation dialog (may need scrolling)
- Check if chat exists in list
- Reload page to refresh list

## Future Buttons Ready (Just Need Features)

When you're ready to add:
1. **Images** - Backend image generation integration
2. **Apps** - Integrations dashboard
3. **Projects** - Project management interface

The buttons are already wired and styled - just needs backend API!

---

**System Info:**
- Server: Flask (localhost:5000)
- AI Model: Phi (1.6GB, running on Ollama)
- Database: SQLite3
- Frontend: Vanilla JavaScript, no frameworks
- Responsive: Desktop-first design
