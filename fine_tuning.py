"""
Fine-tuning Data Collection & Management
Collects user feedback and good/bad examples for training
"""

import json
import os
from datetime import datetime

class FineTuningCollector:
    def __init__(self, data_file="training_data/finetune_data.jsonl"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        
        self.examples = []
        self.load()
    
    def load(self):
        """Load existing training data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                for line in f:
                    self.examples.append(json.loads(line))
    
    def save(self):
        """Save training data in JSONL format for OpenAI"""
        with open(self.data_file, 'w') as f:
            for example in self.examples:
                f.write(json.dumps(example) + '\n')
    
    def add_example(self, user_input, correct_output, feedback=None, rating=None):
        """
        Add a training example
        
        Args:
            user_input: The user's question/prompt
            correct_output: The desired/correct output
            feedback: Optional feedback about why this is correct
            rating: Optional rating 1-5
        """
        example = {
            "messages": [
                {"role": "system", "content": "You are Littlefox AI, a professional intelligent assistant."},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": correct_output}
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "feedback": feedback,
                "rating": rating
            }
        }
        
        self.examples.append(example)
        self.save()
        print(f"✓ Added training example ({len(self.examples)} total)")
        return example
    
    def add_bad_example(self, user_input, bad_output, correction, reason):
        """Add a bad example with correction for learning"""
        example = {
            "messages": [
                {"role": "system", "content": "You are Littlefox AI, a professional intelligent assistant."},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": correction}
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "bad_output": bad_output,
                "reason": reason,
                "type": "correction"
            }
        }
        
        self.examples.append(example)
        self.save()
        print(f"✓ Added correction example: {reason}")
        return example
    
    def get_stats(self):
        """Get training data statistics"""
        total = len(self.examples)
        rated = sum(1 for ex in self.examples if ex.get("metadata", {}).get("rating"))
        corrections = sum(1 for ex in self.examples if ex.get("metadata", {}).get("type") == "correction")
        
        ratings = [ex.get("metadata", {}).get("rating") for ex in self.examples if ex.get("metadata", {}).get("rating")]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            "total_examples": total,
            "rated_examples": rated,
            "correction_examples": corrections,
            "average_rating": avg_rating
        }
    
    def export_for_finetuning(self, min_rating=None):
        """Export training data for OpenAI fine-tuning"""
        filtered = self.examples
        
        if min_rating:
            filtered = [
                ex for ex in self.examples 
                if ex.get("metadata", {}).get("rating", 0) >= min_rating
            ]
        
        output_file = "training_data/finetuning_ready.jsonl"
        with open(output_file, 'w') as f:
            for example in filtered:
                f.write(json.dumps(example) + '\n')
        
        print(f"✓ Exported {len(filtered)} examples to {output_file}")
        print(f"  Ready to upload to OpenAI for fine-tuning")
        return output_file


# Create global instance
collector = FineTuningCollector()
