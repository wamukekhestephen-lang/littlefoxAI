#!/usr/bin/env python3
"""
Setup script for Littlefox AI Training System
Creates necessary directories and initializes the system
"""

import os
import json

def setup():
    print("="*60)
    print("LITTLEFOX AI - TRAINING SYSTEM SETUP")
    print("="*60)
    
    # Create directories
    dirs = [
        "training_data",
        "knowledge_base",
        "data"
    ]
    
    print("\n📁 Creating directories...")
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"   ✓ {dir_name}/")
    
    # Initialize empty files if they don't exist
    print("\n📋 Initializing data files...")
    
    files_to_create = {
        "training_data/finetune_data.jsonl": "",
        "training_data/custom_rules.json": "{}",
        "knowledge_base/embeddings.json": "{}",
        "knowledge_base/documents.json": "{}",
        "knowledge_base/metadata.json": "{}"
    }
    
    for filepath, content in files_to_create.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"   ✓ {filepath}")
        else:
            print(f"   - {filepath} (exists)")
    
    # Initialize domains
    print("\n⚙️ Initializing example domains...")
    try:
        from custom_rules import setup_example_domains
        setup_example_domains()
    except Exception as e:
        print(f"   Note: Domain setup can be done via train.py later")
    
    print("\n" + "="*60)
    print("✓ SETUP COMPLETE!")
    print("="*60)
    
    print("\n📖 Next steps:")
    print("   1. Run: python train.py")
    print("   2. Choose option 1a to ingest your first document")
    print("   3. Add training examples with option 2a")
    print("   4. View stats with option 2c")
    
    print("\n💡 Or try the demo:")
    print("   python demo_training.py")
    
    print("\n📚 Full documentation:")
    print("   TRAINING_GUIDE.md")
    print("   TRAINING_SYSTEM_OVERVIEW.md")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    setup()
