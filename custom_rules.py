import json
import os
from datetime import datetime

class CustomRulesEngine:
    def __init__(self, rules_file="training_data/custom_rules.json"):
        self.rules_file = rules_file
        os.makedirs(os.path.dirname(rules_file), exist_ok=True)
        
        self.rules = {}
        self.load()
    
    def load(self):
        """Load custom rules"""
        if os.path.exists(self.rules_file):
            with open(self.rules_file, 'r') as f:
                self.rules = json.load(f)
    
    def save(self):
        """Save custom rules"""
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
    
    def add_domain_rules(self, domain_name, rules_dict):
        """
        Add domain-specific rules
        
        Args:
            domain_name: Name of domain (e.g., "medical", "legal", "programming")
            rules_dict: Dictionary with rule configurations
        """
        self.rules[domain_name] = {
            "name": domain_name,
            "created_at": datetime.now().isoformat(),
            "rules": rules_dict
        }
        self.save()
        print(f"✓ Added domain rules for '{domain_name}'")
    
    def add_rule(self, domain, rule_name, rule_content):
        """Add a specific rule to a domain"""
        if domain not in self.rules:
            self.rules[domain] = {
                "name": domain,
                "created_at": datetime.now().isoformat(),
                "rules": {}
            }
        
        self.rules[domain]["rules"][rule_name] = rule_content
        self.save()
        print(f"✓ Added rule '{rule_name}' to domain '{domain}'")
    
    def get_system_prompt_for_domain(self, domain):
        """Get enhanced system prompt for a specific domain"""
        if domain not in self.rules:
            return None
        
        domain_rules = self.rules[domain]["rules"]
        
        prompt = f"""You are Littlefox AI, a professional intelligent assistant specializing in {domain}.

DOMAIN-SPECIFIC INSTRUCTIONS FOR {domain.upper()}:

"""
        
        for rule_name, rule_content in domain_rules.items():
            prompt += f"• {rule_name}: {rule_content}\n"
        
        return prompt
    
    def add_terminology(self, domain, terms_dict):
        """
        Add specialized terminology for a domain
        
        Args:
            domain: Domain name
            terms_dict: Dict of {term: definition}
        """
        if "terminology" not in self.rules:
            self.rules["terminology"] = {}
        
        self.rules["terminology"][domain] = terms_dict
        self.save()
        print(f"✓ Added {len(terms_dict)} terms for '{domain}'")
    
    def add_examples(self, domain, examples_list):
        """
        Add domain-specific examples
        
        Args:
            domain: Domain name
            examples_list: List of good examples for that domain
        """
        if "examples" not in self.rules:
            self.rules["examples"] = {}
        
        self.rules["examples"][domain] = examples_list
        self.save()
        print(f"✓ Added {len(examples_list)} examples for '{domain}'")
    
    def get_domain_context(self, domain):
        """Get complete context for a domain"""
        if domain not in self.rules:
            return None
        
        return {
            "prompt": self.get_system_prompt_for_domain(domain),
            "terminology": self.rules.get("terminology", {}).get(domain, {}),
            "examples": self.rules.get("examples", {}).get(domain, [])
        }
    
    def list_domains(self):
        """List all configured domains"""
        domains = {k: v for k, v in self.rules.items() 
                   if isinstance(v, dict) and "created_at" in v}
        return domains
    
    def get_all_rules(self):
        """Get all rules"""
        return self.rules


# Create global instance
rules_engine = CustomRulesEngine()


# Example usage:
def setup_example_domains():
    """Setup some example domains"""
    
    # Medical Domain
    rules_engine.add_domain_rules("medical", {
        "accuracy": "Only provide medically accurate information",
        "disclaimer": "Always include medical disclaimer",
        "citations": "Cite credible medical sources",
        "safety": "Never provide diagnosis or treatment plans"
    })
    
    # Legal Domain
    rules_engine.add_domain_rules("legal", {
        "accuracy": "Ensure legal accuracy and compliance",
        "disclaimer": "Include legal disclaimer for non-lawyers",
        "jurisdiction": "Always ask about jurisdiction when relevant",
        "ethics": "Maintain legal and ethical standards"
    })
    
    # Programming Domain
    rules_engine.add_domain_rules("programming", {
        "code_quality": "Write clean, production-ready code",
        "best_practices": "Follow language best practices",
        "performance": "Consider performance implications",
        "security": "Include security considerations"
    })
    
    print("✓ Example domains configured")
