# Littlefox AI - Complete Training System

## 🎯 What You Just Got

A **complete end-to-end training system** with 5 integrated components:

### 1. **Knowledge Base (RAG)**
- Upload documents: PDF, DOCX, TXT
- Automatic embedding creation (OpenAI text-embedding-3-small)
- Semantic search across your knowledge
- Use with `kb:` prefix in chat

**Files:**
- `knowledge_base.py` - Core knowledge base system
- `knowledge_base/` - Stores embeddings & documents

### 2. **Fine-tuning Data Collection**
- Collect good examples with ratings
- Record corrections and mistakes
- Export in OpenAI JSONL format
- Ready for OpenAI fine-tuning API

**Files:**
- `fine_tuning.py` - Fine-tuning data manager
- `training_data/finetune_data.jsonl` - Your training examples

### 3. **Custom Rules & Domains**
- Create domain-specific instructions (medical, legal, programming, etc.)
- Add specialized terminology
- Store domain examples
- Use with domain prefix in chat

**Files:**
- `custom_rules.py` - Custom rules engine
- `training_data/custom_rules.json` - Your domain configurations

### 4. **RAG Integration**
- Automatically search knowledge base when needed
- Combine web search + knowledge base + domain rules
- Seamless integration into chat responses

### 5. **Feedback System**
- Learn from corrections
- Rate examples for quality
- Improve over time

---

## 🚀 Quick Start

### Option 1: Interactive Training CLI
```bash
python train.py
```

Menu-driven interface for all training operations.

### Option 2: Demo
```bash
python demo_training.py
```

See all features in action.

### Option 3: Python Code
```python
from knowledge_base import kb
from fine_tuning import collector
from custom_rules import rules_engine

# Ingest documents
kb.ingest_document("my_document.pdf")

# Collect training data
collector.add_example("Q", "A", rating=5)

# Setup domains
rules_engine.add_domain_rules("medical", {...})
```

---

## 💬 Using in Chat

### Knowledge Base Search
```
User: kb: What does the handbook say about vacation?
Littlefox AI: [searches knowledge base and responds]
```

### Domain-Specific Responses
```
User: medical: What are symptoms of diabetes?
Littlefox AI: [responds using medical domain rules]

User: legal: What's in a non-disclosure agreement?
Littlefox AI: [responds using legal domain rules]

User: programming: How do I optimize this loop?
Littlefox AI: [responds using programming best practices]
```

### Web Search (explicit)
```
User: search: latest developments in AI 2026
Littlefox AI: [searches web and responds with current info]
```

### Combined Search
```
User: legal: kb: What are the termination clauses?
Littlefox AI: [uses legal domain + knowledge base]
```

---

## 📊 Training Workflow

### 1. Setup Domains
```bash
python train.py → 3a) Setup Example Domains
```

### 2. Ingest Documents
```bash
python train.py → 1a) Ingest Document
```

### 3. Collect Training Data
```bash
python train.py → 2a) Add Good Example
python train.py → 2b) Add Bad Example (corrections)
```

### 4. Monitor Progress
```bash
python train.py → 2c) View Training Stats
python train.py → 4) View All Training Data
```

### 5. Export & Fine-tune
```bash
python train.py → 2d) Export for Fine-tuning
# Then upload to OpenAI
```

---

## 📁 File Structure

```
my_ai_assistant/
├── knowledge_base.py           # Knowledge base system
├── fine_tuning.py              # Training data collection
├── custom_rules.py             # Domain rules engine
├── train.py                    # Training CLI tool
├── demo_training.py            # Demo/example
│
├── training_data/              # Training data directory
│   ├── finetune_data.jsonl     # Collected training examples
│   ├── finetuning_ready.jsonl  # Exported for OpenAI
│   └── custom_rules.json       # Domain configurations
│
├── knowledge_base/             # Knowledge base directory
│   ├── embeddings.json         # Document embeddings
│   ├── documents.json          # Document text chunks
│   └── metadata.json           # Document metadata
│
└── TRAINING_GUIDE.md           # Full documentation
```

---

## 🎓 Example: Complete Training Scenario

### Setup a Medical Domain
```python
from custom_rules import rules_engine

rules_engine.add_domain_rules("medical", {
    "accuracy": "Only provide medically accurate information",
    "disclaimer": "Always include disclaimer about consulting doctors",
    "citations": "Reference credible medical sources when possible",
    "safety": "Never provide diagnosis or treatment plans"
})

rules_engine.add_terminology("medical", {
    "MRI": "Magnetic Resonance Imaging",
    "ECG": "Electrocardiogram",
    "BMI": "Body Mass Index"
})
```

### Ingest Medical Documents
```python
from knowledge_base import kb

kb.ingest_document("medical_handbook.pdf", "handbook")
kb.ingest_document("patient_guidelines.docx", "guidelines")
```

### Collect Training Examples
```python
from fine_tuning import collector

collector.add_example(
    user_input="What are common symptoms of hypertension?",
    correct_output="Common symptoms include headaches, chest pain, shortness of breath...",
    rating=5
)
```

### Use in Chat
```
User: medical: kb: What should I do about high blood pressure?
Littlefox AI: [responds using medical domain rules + knowledge base]
```

---

## ⚡ Performance Tips

1. **Start small** - Use 5-10 documents initially
2. **Quality training data** - Rate examples, focus on high-quality ones
3. **Batch operations** - Ingest multiple documents at once
4. **Regular exports** - Export training data weekly
5. **Domain focus** - Start with 1-2 domains, expand gradually

---

## 🔒 Data Privacy

- **Local storage**: All training data stored locally
- **Embeddings**: Created via OpenAI API (configure via .env)
- **Fine-tuning**: You control what gets sent to OpenAI
- **Knowledge base**: Your documents never sent unless explicitly searched

---

## 📚 Next Steps

1. **Run demo**: `python demo_training.py`
2. **Open CLI**: `python train.py`
3. **Ingest documents**: Add your own knowledge
4. **Create domains**: Setup specialized behavior
5. **Collect examples**: Build training data
6. **Export & fine-tune**: Upload to OpenAI when ready
7. **Monitor**: Check stats and improve continuously

---

## 📖 Full Documentation

See `TRAINING_GUIDE.md` for comprehensive documentation.

---

**You now have a complete AI training system! 🚀**

Start with: `python train.py`
