#!/usr/bin/env python3
"""
Quick Start Training Examples
Run this to see how all training components work together
"""

from knowledge_base import kb
from fine_tuning import collector
from custom_rules import rules_engine, setup_example_domains

def demo():
    print("="*60)
    print("LITTLEFOX AI - TRAINING SYSTEM DEMO")
    print("="*60)
    
    # 1. Setup example domains
    print("\n1. Setting up example domains (medical, legal, programming)...")
    setup_example_domains()
    
    # 2. Add some training examples
    print("\n2. Adding training examples...")
    collector.add_example(
        user_input="What is machine learning?",
        correct_output="Machine learning is a subset of artificial intelligence that enables systems to learn from data without explicit programming.",
        feedback="Clear and accurate definition",
        rating=5
    )
    
    collector.add_example(
        user_input="How do I write clean code?",
        correct_output="Write clean code by: 1) Using meaningful names, 2) Keeping functions small, 3) Following DRY principle, 4) Writing tests, 5) Refactoring regularly.",
        feedback="Practical and actionable",
        rating=5
    )
    
    # 3. Show training stats
    print("\n3. Training statistics:")
    stats = collector.get_stats()
    print(f"   Total examples: {stats['total_examples']}")
    print(f"   Average rating: {stats['average_rating']:.2f}/5")
    
    # 4. Show configured domains
    print("\n4. Configured domains:")
    domains = rules_engine.list_domains()
    for domain in domains:
        print(f"   ✓ {domain}")
    
    # 5. Add custom terminology
    print("\n5. Adding custom terminology to medical domain...")
    rules_engine.add_terminology("medical", {
        "MRI": "Magnetic Resonance Imaging - non-invasive medical imaging",
        "EHR": "Electronic Health Record - patient data system",
        "ICU": "Intensive Care Unit - critical care facility"
    })
    
    # 6. Get domain context
    print("\n6. Medical domain system prompt:")
    context = rules_engine.get_domain_context("medical")
    if context:
        print("   " + context["prompt"][:200] + "...")
    
    print("\n" + "="*60)
    print("✓ Demo complete! You can now:")
    print("  - Use 'kb: your question' to search knowledge base")
    print("  - Use 'medical: your question' for medical domain")
    print("  - Use 'programming: your question' for coding help")
    print("  - Run 'python train.py' for full training interface")
    print("="*60)

if __name__ == "__main__":
    demo()
