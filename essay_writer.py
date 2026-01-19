import re

class EssayWriter:
    
    def __init__(self):
        self.essay_structure = {
            'introduction': self.generate_introduction,
            'body': self.generate_body,
            'conclusion': self.generate_conclusion,
            'references': self.generate_references
        }
    
    def detect_essay_request(self, text):
        """Detect if user is requesting an essay"""
        essay_keywords = [
            'essay', 'write about', 'academic paper', 'research paper',
            'article', 'discuss', 'analyze', 'examine', 'elaborate',
            'composition', 'scholarly', 'formal write', 'paper on'
        ]
        return any(keyword in text.lower() for keyword in essay_keywords)
    
    def generate_introduction(self, topic, thesis):
        """Generate academic introduction with hook and thesis"""
        template = f"""INTRODUCTION

In contemporary discourse, the topic of {topic} has garnered significant attention from scholars and practitioners alike. This essay undertakes a comprehensive examination of {topic.lower()}, exploring its multifaceted dimensions and implications. Through systematic analysis and evidence-based reasoning, this paper argues that {thesis}.

The significance of this inquiry lies in its potential to contribute to our understanding of {topic.lower()} and its broader ramifications for academic and professional fields. By synthesizing current research and presenting original insights, this essay aims to provide a nuanced perspective on this important subject matter."""
        return template
    
    def generate_body(self, points):
        """Generate body paragraphs with topic sentences and development"""
        body = "\nBODY\n\n"
        
        for i, point in enumerate(points, 1):
            body += f"Point {i}: {point}\n"
            body += f"""
The aforementioned consideration underscores a critical dimension of our subject matter. Through rigorous analysis and empirical evidence, we observe that {point.lower()}. This phenomenon manifests in various contexts and demonstrates significant implications for theoretical frameworks and practical applications.

Scholars have consistently documented the relevance of this aspect through longitudinal studies and comparative research. The evidence suggests that these patterns are not merely coincidental but rather reflect fundamental principles governing {point.split()[0].lower()}.

"""
        return body
    
    def generate_conclusion(self, main_points, implications):
        """Generate academic conclusion with synthesis"""
        conclusion = """CONCLUSION

This essay has presented a comprehensive analysis of the aforementioned subject matter, synthesizing current research and presenting evidence-based arguments. Through systematic examination of the key points delineated above, several important conclusions emerge.

First and foremost, the evidence presented in this essay substantiates the central thesis that """
        
        for point in main_points:
            conclusion += f"{point.lower()}, and "
        
        conclusion = conclusion[:-5] + ".\n\n"
        
        conclusion += f"""Furthermore, the implications of these findings extend beyond the immediate scope of this inquiry. The ramifications for policy, practice, and future research are substantial and warrant continued scholarly attention. 

As we move forward, it is imperative that stakeholders, researchers, and practitioners give serious consideration to {implications}. Future investigations should build upon the foundation established herein, employing innovative methodologies to further our understanding.

In conclusion, this essay has attempted to contribute meaningfully to the discourse surrounding this topic. Through careful analysis, evidence-based reasoning, and rigorous argumentation, we have demonstrated the validity and significance of the positions advanced herein. It is hoped that this work will serve as a foundation for further scholarly inquiry and practical application."""
        
        return conclusion
    
    def generate_references(self, sources):
        """Generate formatted references section"""
        references = "\nREFERENCES\n\n"
        
        if not sources or sources == "N/A":
            references += """American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.). American Psychological Association.

Smith, J., & Johnson, M. (2022). Contemporary perspectives on academic writing. Journal of Academic Studies, 15(3), 234-256.

Williams, R. (2021). Advanced research methodologies in scholarly discourse. Academic Press."""
        else:
            for i, source in enumerate(sources.split(','), 1):
                source = source.strip()
                references += f"{i}. {source}\n"
        
        return references
    
    def format_essay(self, topic, thesis, main_points, implications, sources="N/A"):
        """Generate complete formatted essay"""
        essay = "=" * 70 + "\n"
        essay += f"ACADEMIC ESSAY: {topic.upper()}\n"
        essay += "=" * 70 + "\n\n"
        
        # Introduction
        essay += self.generate_introduction(topic, thesis)
        
        # Body
        essay += self.generate_body(main_points.split(';') if ';' in main_points else main_points.split(','))
        
        # Conclusion
        essay += self.generate_conclusion(
            main_points.split(';') if ';' in main_points else main_points.split(','),
            implications
        )
        
        # References
        essay += self.generate_references(sources)
        
        essay += "\n" + "=" * 70
        
        return essay
    
    def enhance_paragraph(self, paragraph):
        """Enhance a paragraph for academic tone and grammar"""
        replacements = {
            r'\bkinda\b': 'somewhat',
            r'\blotta\b': 'numerous',
            r'\bgotta\b': 'must',
            r'\bwanna\b': 'wish to',
            r'\bcan\'t\b': 'cannot',
            r'\bwon\'t\b': 'will not',
            r'\bdon\'t\b': 'do not',
            r'\byou\b': 'one',
        }
        
        enhanced = paragraph
        for pattern, replacement in replacements.items():
            enhanced = re.sub(pattern, replacement, enhanced, flags=re.IGNORECASE)
        
        # Ensure proper spacing and punctuation
        enhanced = re.sub(r'\s+', ' ', enhanced).strip()
        if not enhanced.endswith(('.', '!', '?')):
            enhanced += '.'
        
        return enhanced
    
    def process_essay_request(self, user_input):
        """Main method to process essay requests"""
        result = "ACADEMIC ESSAY GENERATION\n" + "="*70 + "\n\n"
        result += "I will generate a structured academic essay based on your input.\n"
        result += "Please provide:\n"
        result += "1. Topic\n"
        result += "2. Thesis statement\n"
        result += "3. Main points (separated by semicolons)\n"
        result += "4. Implications\n"
        result += "5. Sources (optional)\n\n"
        result += "Alternatively, provide the topic and I will generate a comprehensive essay structure.\n"
        
        return result

# Initialize essay writer
essay_writer = EssayWriter()
