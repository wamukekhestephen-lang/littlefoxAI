"""
Test script to demonstrate new Math Solver and Essay Writer features
Run this to see the capabilities in action
"""

from math_solver import math_solver
from essay_writer import essay_writer

def test_math_solver():
    print("=" * 70)
    print("MATH SOLVER TESTS")
    print("=" * 70)
    
    test_cases = [
        ("Solve x^2 - 5x + 6 = 0", "Quadratic equation"),
        ("Solve x + 2 = 10", "Linear equation"),
        ("Find derivative of x^3 + 2x^2", "Derivative"),
        ("Integrate 3x^2 + 2x", "Integral"),
        ("Factor x^2 - 9", "Factoring"),
        ("Expand (x + 2)(x - 3)", "Expansion"),
        ("Simplify 4x/2x", "Simplification"),
        ("Calculate limit of sin(x)/x", "Limit"),
    ]
    
    for test_input, description in test_cases:
        print(f"\n\nTest: {description}")
        print(f"Input: {test_input}")
        print("-" * 70)
        
        # Check if it's detected as math problem
        is_math = math_solver.detect_math_problem(test_input)
        print(f"Detected as math problem: {is_math}")
        
        # Process it
        if is_math:
            result = math_solver.process_math_problem(test_input)
            print(result)
        else:
            print("Not detected as math problem")

def test_essay_writer():
    print("\n\n" + "=" * 70)
    print("ESSAY WRITER TESTS")
    print("=" * 70)
    
    test_cases = [
        ("Write an essay about climate change", "Climate change essay"),
        ("Academic paper on artificial intelligence", "AI paper"),
        ("Essay on renewable energy", "Renewable energy essay"),
    ]
    
    for test_input, description in test_cases:
        print(f"\n\nTest: {description}")
        print(f"Input: {test_input}")
        print("-" * 70)
        
        # Check if it's detected as essay request
        is_essay = essay_writer.detect_essay_request(test_input)
        print(f"Detected as essay request: {is_essay}")
        
        # Extract topic
        if is_essay:
            topic = test_input.replace("essay", "").replace("write", "").replace("academic paper", "") \
                              .replace("about", "").replace("on", "").replace("paper", "").strip()
            print(f"Extracted topic: {topic}")
            
            # Generate essay
            thesis = f"This paper explores significant and multifaceted aspects of {topic}."
            main_points = f"Historical context of {topic}; Current state and implications; Future prospects"
            implications = f"understanding and strategic implementation of {topic}"
            
            result = essay_writer.format_essay(topic, thesis, main_points, implications)
            print(result)

def demonstrate_integration():
    print("\n\n" + "=" * 70)
    print("INTEGRATION DEMONSTRATION")
    print("=" * 70)
    
    print("\nThe new features integrate seamlessly with the existing AI assistant:")
    print("\n1. Math Solver detects mathematical queries and solves them directly")
    print("2. Essay Writer detects essay requests and generates academic content")
    print("3. For other queries, the normal AI chain is used")
    print("\nIn main.py, the comprehensive_response() function now:")
    print("  - Checks for math problems first")
    print("  - Checks for essay requests")
    print("  - Falls back to normal AI response for general queries")

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AI ASSISTANT - NEW FEATURES TEST" + " " * 21 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Run tests
    test_math_solver()
    test_essay_writer()
    demonstrate_integration()
    
    print("\n\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
    print("\nTo use in your application:")
    print("1. Math problems are automatically detected and solved")
    print("2. Essay requests are automatically detected and processed")
    print("3. Other queries go through normal AI processing")
    print("\nStart using your AI assistant with these new capabilities!")
