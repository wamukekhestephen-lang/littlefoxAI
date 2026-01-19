class RequestClassifier:
    def __init__(self):
        self.request_types = {
            'code': self.detect_code_request,
            'math': self.detect_math_request,
            'essay': self.detect_essay_request,
            'greeting': self.detect_greeting,
            'capabilities': self.detect_capabilities,
            'design': self.detect_design_request,
            'translation': self.detect_translation_request,
            'howto': self.detect_howto_request,
            'creative': self.detect_creative_request,
            'analysis': self.detect_analysis_request,
            'general': None  # fallback
        }
    
    def detect_code_request(self, text):
        """Detect code generation, debugging, or explanation requests"""
        keywords = [
            'code', 'write a', 'create', 'function', 'program', 'script',
            'html', 'css', 'javascript', 'python', 'java', 'cpp', 'c#',
            'react', 'vue', 'node', 'flask', 'django', 'api', 'database',
            'debug', 'fix', 'error', 'bug', 'issue', 'problem with',
            'refactor', 'optimize', 'improve', 'snippet', 'example',
            'implementation', 'how to code', 'build', 'develop',
            'class', 'method', 'function', 'variable', 'loop', 'condition',
            'sql', 'query', 'endpoint', 'route', 'middleware', 'component',
            'game', 'application', 'software', 'system'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_math_request(self, text):
        """Detect mathematics problems"""
        keywords = [
            'solve', 'equation', 'derivative', 'integral', 'calculate',
            'compute', 'limit', 'simplify', 'factor', 'expand',
            'calculus', 'algebra', 'geometry', 'matrix', 'determinant',
            'eigenvalue', 'polynomial', 'root', 'quadratic', 'linear',
            'differential', 'inequality', 'sin', 'cos', 'tan', 'log',
            'sqrt', 'math', 'dx', 'dy', '∫', '∑', 'mathematical'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_essay_request(self, text):
        """Detect essay or academic writing requests"""
        essay_keywords = [
            'essay', 'academic', 'paper', 'research paper',
            'research', 'article', 'compose', 'scholarly',
            'formal write', 'term paper', 'report on'
        ]
        
        # Check if it's specifically asking for an essay
        for keyword in essay_keywords:
            if keyword in text.lower():
                return True
        
        # Also check for "write about X topic" combined with academic-sounding topics
        if 'write about' in text.lower() or 'write an' in text.lower():
            academic_topics = [
                'climate change', 'technology', 'education', 'health',
                'economy', 'society', 'politics', 'philosophy',
                'science', 'history', 'literature', 'culture'
            ]
            return any(topic in text.lower() for topic in academic_topics)
        
        return False
    
    def detect_greeting(self, text):
        """Detect greetings"""
        # Detect greetings that start with greeting words
        text = text.strip()
        
        # Simple greetings
        simple_greetings = ['hello', 'hi', 'hey', 'greetings', 'howdy', 'welcome', 
                           'bye', 'goodbye', 'farewell', 'thanks', 'thank you']
        
        for greeting in simple_greetings:
            if text.lower() == greeting or text.lower().startswith(greeting + ' '):
                return True
        
        # Complex greetings
        if any(text.lower().startswith(phrase) for phrase in 
               ['good morning', 'good afternoon', 'good evening', 'how are you', 
                "what's up", 'sup', 'see you', 'appreciate']):
            return True
        
        return False
    
    def detect_capabilities(self, text):
        """Detect capability/feature inquiries"""
        keywords = [
            'what can you do', 'capabilities', 'features', 'abilities',
            'tell me about yourself', 'what can i', 'help with',
            'how can you help', 'what do you', 'can you'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_design_request(self, text):
        """Detect design, UI/UX, or visual requests"""
        keywords = [
            'design', 'ui', 'ux', 'layout', 'template', 'wireframe',
            'mockup', 'color', 'font', 'style', 'visual', 'aesthetic',
            'icon', 'logo', 'interface', 'theme', 'responsive'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_translation_request(self, text):
        """Detect translation requests"""
        keywords = [
            'translate', 'translation', 'convert to', 'in english',
            'in spanish', 'in french', 'in german', 'in chinese',
            'in russian', 'in arabic', 'in portuguese', 'in italian',
            'what is', 'what does', 'means', 'language'
        ]
        # Check if it's more specific than just "what is"
        if 'what is' in text.lower() or 'what does' in text.lower():
            # Only consider it translation if combined with language keywords
            lang_keywords = ['english', 'spanish', 'french', 'german', 'chinese', 'russian', 'arabic', 'portuguese', 'italian', 'japanese']
            return any(lang in text.lower() for lang in lang_keywords)
        
        return any(kw in text.lower() for kw in keywords)
    
    def detect_howto_request(self, text):
        """Detect how-to and tutorial requests"""
        keywords = [
            'how to', 'how do i', 'how can i', 'teach me',
            'explain', 'show me', 'tutorial', 'guide', 'step by step',
            'instructions', 'help me learn', 'what is', 'what are',
            'tell me how', 'walk me through'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_creative_request(self, text):
        """Detect creative writing requests"""
        keywords = [
            'story', 'poem', 'fiction', 'create a', 'write a',
            'character', 'plot', 'dialogue', 'creative', 'imagine',
            'generate', 'make up', 'invent', 'brainstorm', 'idea',
            'description', 'scenario', 'narrative'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def detect_analysis_request(self, text):
        """Detect analysis and evaluation requests"""
        keywords = [
            'analyze', 'analysis', 'evaluate', 'evaluation', 'compare',
            'comparison', 'pros and cons', 'advantage', 'disadvantage',
            'pros', 'cons', 'pros vs', 'which is better', 'difference',
            'summary', 'summarize', 'review', 'critique', 'assess'
        ]
        return any(kw in text.lower() for kw in keywords)
    
    def classify(self, user_input):
        """Classify the user request and return the category"""
        text = user_input.lower().strip()
        
        # Check in order of specificity (most specific first)
        # 1. Greetings (very specific)
        if self.detect_greeting(text):
            return 'greeting'
        
        # 2. Capabilities (very specific)
        if self.detect_capabilities(text):
            return 'capabilities'
        
        # 3. Essay (check before code since code detection is broad)
        if self.detect_essay_request(text):
            return 'essay'
        
        # 4. Math (very specific)
        if self.detect_math_request(text):
            return 'math'
        
        # 5. Design (specific)
        if self.detect_design_request(text):
            return 'design'
        
        # 6. Translation (specific)
        if self.detect_translation_request(text):
            return 'translation'
        
        # 7. Analysis (specific)
        if self.detect_analysis_request(text):
            return 'analysis'
        
        # 8. How-to (specific)
        if self.detect_howto_request(text):
            return 'howto'
        
        # 9. Creative (check before code)
        if self.detect_creative_request(text):
            return 'creative'
        
        # 10. Code (broad, check last of specific types)
        if self.detect_code_request(text):
            return 'code'
        
        # Default to general if nothing matches
        return 'general'
    
    def get_context_hint(self, request_type):
        """Get a hint about what type of request was detected"""
        hints = {
            'code': 'Programming/Code',
            'math': 'Mathematics',
            'essay': 'Academic Writing',
            'greeting': 'Greeting',
            'capabilities': 'Capabilities',
            'design': 'Design/UI',
            'translation': 'Translation',
            'howto': 'How-To/Tutorial',
            'creative': 'Creative Writing',
            'analysis': 'Analysis/Comparison',
            'general': 'General Question'
        }
        return hints.get(request_type, 'Unknown')

# Initialize classifier
classifier = RequestClassifier()
