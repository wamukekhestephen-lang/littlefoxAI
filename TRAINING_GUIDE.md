# Littlefox AI - Training System Guide

## Overview

Littlefox AI now includes a comprehensive training system with 5 major components:

1. **Knowledge Base** - Upload and search your documents
2. **Fine-tuning Data** - Collect training examples for OpenAI fine-tuning
3. **Custom Rules** - Create domain-specific instructions
4. **RAG Integration** - Retrieve relevant information from your knowledge base
5. **Feedback System** - Learn from corrections and improve

## Getting Started

### Start the Training CLI

```bash
python train.py
```

This opens an interactive menu to manage all training components.

---

## Component 1: Knowledge Base

### What it does
Ingests documents (PDF, DOCX, TXT), creates embeddings, and allows semantic search.

### How to use

**From CLI (train.py):**
1. Choose `1a) Ingest Document`
2. Enter the file path
3. Give it a name (optional)
4. The system creates embeddings automatically

**From Python code:**
```python
from knowledge_base import kb

# Ingest a document
kb.ingest_document("path/to/document.pdf", "my_doc")

# Search the knowledge base
results = kb.search("What is machine learning?", top_k=3)
for result in results:
    print(f"Score: {result['score']}")
    print(f"Content: {result['text']}")

# List all documents
docs = kb.list_documents()
```

### In Chat

Use the `kb:` prefix in your question:
```
User: kb: What does the document say about AI?
Littlefox AI: [searches knowledge base and responds with relevant sections]
```

---

## Component 2: Fine-tuning Data

### What it does
Collects good examples and corrections to fine-tune the OpenAI model.

### How to use

**From CLI (train.py):**
1. Choose `2a) Add Good Example` to save correct responses
2. Choose `2b) Add Bad Example` to record mistakes and fixes
3. Choose `2c) View Training Stats` to see progress
4. Choose `2d) Export for Fine-tuning` when ready

**From Python code:**
```python
from fine_tuning import collector

# Add a good example
collector.add_example(
    user_input="What is quantum computing?",
    correct_output="Quantum computing uses quantum bits...",
    feedback="Accurate and comprehensive explanation",
    rating=5
)

# Record a bad example and correction
collector.add_bad_example(
    user_input="Explain AI",
    bad_output="AI is basically robots",
    correction="Artificial Intelligence is...",
    reason="Original was too simplistic"
)

# View statistics
stats = collector.get_stats()
print(f"Total examples: {stats['total_examples']}")
print(f"Average rating: {stats['average_rating']}")

# Export for fine-tuning
collector.export_for_finetuning(min_rating=4)
```

### Uploading to OpenAI

Once you have collected examples:

```bash
# Export the data
python -c "from fine_tuning import collector; collector.export_for_finetuning()"

# Then upload to OpenAI using their CLI
openai api fine_tunes.create -t training_data/finetuning_ready.jsonl
```

---

## Component 3: Custom Rules & Domains

### What it does
Create domain-specific instructions and terminology for specialized tasks.

### How to use

**From CLI (train.py):**
1. Choose `3a) Setup Example Domains` (medical, legal, programming)
2. Choose `3b) Add Domain Rules` to customize
3. Choose `3c) View Domain Context` to see all settings
4. Choose `3d) List All Domains` to see configured domains

**From Python code:**
```python
from custom_rules import rules_engine

# Add domain-specific rules
rules_engine.add_domain_rules("medical", {
    "accuracy": "Only provide medically accurate information",
    "disclaimer": "Always include medical disclaimer",
    "citations": "Cite credible medical sources"
})

# Add specialized terminology
rules_engine.add_terminology("medical", {
    "MRI": "Magnetic Resonance Imaging",
    "CT": "Computed Tomography",
    "ECG": "Electrocardiogram"
})

# Add examples
rules_engine.add_examples("medical", [
    "Always ask about patient history",
    "Never provide definitive diagnosis",
    "Recommend consulting a healthcare provider"
])

# Get context for a domain
context = rules_engine.get_domain_context("medical")
print(context["prompt"])  # Full system prompt for that domain
```

### In Chat

Use domain prefix to trigger specialized behavior:
```
User: medical: What are the symptoms of diabetes?
Littlefox AI: [responds using medical domain rules and terminology]

User: programming: How do I optimize this function?
Littlefox AI: [responds using programming best practices]
```

---

## Component 4: RAG Integration

### How it works

The system automatically searches your knowledge base when you:
- Use the `kb:` prefix
- Ask questions related to ingested documents
- Request specific information

### Example workflow

```python
# Ingest your company documentation
kb.ingest_document("company_handbook.pdf", "handbook")
kb.ingest_document("project_guidelines.docx", "guidelines")

# Now questions can use this knowledge
# User: kb: What's our vacation policy?
# → System searches documents and answers based on handbook
```

---

## Component 5: Complete Training Workflow

### Step-by-step example

```python
from knowledge_base import kb
from fine_tuning import collector
from custom_rules import rules_engine

# 1. Setup a legal domain
rules_engine.add_domain_rules("legal", {
    "accuracy": "Ensure legal accuracy",
    "jurisdiction": "Ask about jurisdiction",
    "disclaimer": "Include legal disclaimer"
})

# 2. Ingest legal documents
kb.ingest_document("contracts.pdf", "contracts")
kb.ingest_document("terms.docx", "terms")

# 3. Collect training examples
collector.add_example(
    user_input="What are common contract terms?",
    correct_output="Common contract terms include...",
    rating=5
)

# 4. Use in chat
# User: legal: kb: What are termination clauses?
# → Uses legal domain rules + knowledge base + generates response
```

---

## Training Data Files

All training data is saved in the `training_data/` directory:

```
training_data/
├── finetune_data.jsonl          # Training examples for OpenAI
├── finetuning_ready.jsonl       # Exported, ready-to-upload data
└── custom_rules.json            # Domain rules and terminology

knowledge_base/
├── embeddings.json              # Document embeddings
├── documents.json               # Document chunks
└── metadata.json                # Document metadata & custom knowledge
```

---

## Advanced Usage

### Adding feedback to improve the model

```python
# After an AI response, if it was helpful
collector.add_example(
    user_input="User's question",
    correct_output="AI's response",
    feedback="Great answer because...",
    rating=5
)

# If AI made a mistake
collector.add_bad_example(
    user_input="User's question",
    bad_output="AI's wrong response",
    correction="Correct response",
    reason="AI missed the key point"
)
```

### Viewing all training progress

```bash
python train.py
# Select option 4: VIEW ALL TRAINING DATA
```

This shows:
- Number of ingested documents and total chunks
- Training data statistics (examples, ratings)
- Configured domains

---

## Best Practices

1. **Start with domain rules** - Define what you want before collecting data
2. **Quality over quantity** - 10 excellent examples beat 100 mediocre ones
3. **Rate examples** - Use ratings to identify your best training data
4. **Ingest gradually** - Add documents as you go
5. **Export regularly** - Keep backups of your training data
6. **Test domain behavior** - Verify domains work as expected before heavy use

---

## FAQ

**Q: How often should I fine-tune?**
A: Once you have 50+ high-quality examples (rating 4+)

**Q: Can I delete training data?**
A: Yes, remove files from `training_data/` or `knowledge_base/`

**Q: How large can my knowledge base be?**
A: Tested with 100+ documents, limited mainly by available memory

**Q: Do I need OpenAI API for knowledge base?**
A: Yes, for creating embeddings. Alternatively, use local models (Ollama)

---

## Next Steps

1. Start with `python train.py`
2. Try all 5 components with test data
3. Set up your first domain
4. Ingest your key documents
5. Collect training examples
6. Export and fine-tune when ready

Happy training! 🚀
