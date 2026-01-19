"""
Training Management CLI Tool
Easy interface to manage all training components
"""

import os
from knowledge_base import kb
from fine_tuning import collector
from custom_rules import rules_engine, setup_example_domains

def print_menu():
    print("\n" + "="*60)
    print("LITTLEFOX AI - TRAINING MANAGEMENT SYSTEM")
    print("="*60)
    print("\n1. KNOWLEDGE BASE")
    print("   1a) Ingest Document (PDF, DOCX, TXT)")
    print("   1b) Search Knowledge Base")
    print("   1c) List Documents")
    print("\n2. FINE-TUNING DATA")
    print("   2a) Add Good Example")
    print("   2b) Add Bad Example (Correction)")
    print("   2c) View Training Stats")
    print("   2d) Export for Fine-tuning")
    print("\n3. CUSTOM RULES & DOMAINS")
    print("   3a) Setup Example Domains")
    print("   3b) Add Domain Rules")
    print("   3c) View Domain Context")
    print("   3d) List All Domains")
    print("\n4. VIEW ALL TRAINING DATA")
    print("\n5. EXIT")
    print("\n" + "="*60)

def ingest_document():
    filepath = input("\nEnter document path (or relative path): ").strip()
    if not os.path.exists(filepath):
        print("❌ File not found!")
        return
    
    doc_name = input("Enter document name (or press Enter for filename): ").strip()
    if not doc_name:
        doc_name = None
    
    print("\n⏳ Ingesting document...")
    kb.ingest_document(filepath, doc_name)

def search_kb():
    query = input("\nEnter search query: ").strip()
    results = kb.search(query, top_k=3)
    
    if not results:
        print("❌ No results found")
        return
    
    print(f"\n✓ Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i} (Score: {result['score']:.3f}):")
        print(f"{result['text'][:200]}...\n")

def list_documents():
    docs = kb.list_documents()
    if not docs:
        print("❌ No documents ingested")
        return
    
    print(f"\n✓ {len(docs)} documents in knowledge base:\n")
    for doc_name, meta in docs.items():
        if doc_name != "custom_knowledge":
            print(f"  • {doc_name} ({meta.get('chunks', 0)} chunks)")

def add_good_example():
    user_input = input("\nUser question: ").strip()
    output = input("Correct output: ").strip()
    feedback = input("Why this is correct (optional): ").strip() or None
    rating_str = input("Rating 1-5 (optional): ").strip()
    rating = int(rating_str) if rating_str.isdigit() and 1 <= int(rating_str) <= 5 else None
    
    collector.add_example(user_input, output, feedback, rating)

def add_bad_example():
    user_input = input("\nUser question: ").strip()
    bad_output = input("Bad/incorrect output: ").strip()
    correction = input("Correct output: ").strip()
    reason = input("Why it was wrong: ").strip()
    
    collector.add_bad_example(user_input, bad_output, correction, reason)

def view_stats():
    stats = collector.get_stats()
    print("\n" + "="*40)
    print("TRAINING DATA STATISTICS")
    print("="*40)
    print(f"Total examples: {stats['total_examples']}")
    print(f"Rated examples: {stats['rated_examples']}")
    print(f"Correction examples: {stats['correction_examples']}")
    print(f"Average rating: {stats['average_rating']:.2f}/5")
    print("="*40)

def export_for_finetuning():
    min_rating = input("\nMinimum rating to export (1-5, or press Enter for all): ").strip()
    min_rating = int(min_rating) if min_rating.isdigit() else None
    
    collector.export_for_finetuning(min_rating)

def setup_domains():
    setup_example_domains()

def add_domain_rules():
    domain = input("\nDomain name (e.g., 'medical', 'legal', 'programming'): ").strip()
    
    print(f"\nAdding rules for domain: {domain}")
    print("Enter rule_name: rule_content pairs (press Enter with empty name to finish)")
    
    rules = {}
    while True:
        rule_name = input("\nRule name: ").strip()
        if not rule_name:
            break
        
        rule_content = input(f"Rule content for '{rule_name}': ").strip()
        rules[rule_name] = rule_content
    
    if rules:
        rules_engine.add_domain_rules(domain, rules)

def view_domain_context():
    domain = input("\nDomain name: ").strip()
    context = rules_engine.get_domain_context(domain)
    
    if not context:
        print("❌ Domain not found")
        return
    
    print(f"\n{'='*60}")
    print(f"DOMAIN CONTEXT: {domain.upper()}")
    print(f"{'='*60}")
    
    print("\nSYSTEM PROMPT:")
    print(context['prompt'])
    
    if context['terminology']:
        print("\nTERMINOLOGY:")
        for term, definition in context['terminology'].items():
            print(f"  • {term}: {definition}")
    
    if context['examples']:
        print("\nEXAMPLES:")
        for i, example in enumerate(context['examples'], 1):
            print(f"  {i}. {example}")

def list_domains():
    domains = rules_engine.list_domains()
    if not domains:
        print("❌ No domains configured")
        return
    
    print(f"\n✓ {len(domains)} domains configured:\n")
    for domain, info in domains.items():
        rule_count = len(info.get('rules', {}))
        print(f"  • {domain} ({rule_count} rules)")

def view_all_training():
    print("\n" + "="*60)
    print("ALL TRAINING DATA")
    print("="*60)
    
    print("\n📚 KNOWLEDGE BASE:")
    docs = kb.list_documents()
    print(f"  Documents: {len([d for d in docs if d != 'custom_knowledge'])}")
    print(f"  Total chunks: {sum(d.get('chunks', 0) for d in docs.values() if d != 'custom_knowledge')}")
    
    print("\n🎓 FINE-TUNING DATA:")
    stats = collector.get_stats()
    print(f"  Total examples: {stats['total_examples']}")
    print(f"  Average rating: {stats['average_rating']:.2f}/5")
    
    print("\n⚙️ CUSTOM RULES:")
    domains = rules_engine.list_domains()
    print(f"  Domains: {len(domains)}")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1a":
            ingest_document()
        elif choice == "1b":
            search_kb()
        elif choice == "1c":
            list_documents()
        elif choice == "2a":
            add_good_example()
        elif choice == "2b":
            add_bad_example()
        elif choice == "2c":
            view_stats()
        elif choice == "2d":
            export_for_finetuning()
        elif choice == "3a":
            setup_domains()
        elif choice == "3b":
            add_domain_rules()
        elif choice == "3c":
            view_domain_context()
        elif choice == "3d":
            list_domains()
        elif choice == "4":
            view_all_training()
        elif choice == "5":
            print("\n✓ Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
