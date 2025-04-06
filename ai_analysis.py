class AIAnalysisPipeline:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        
    def analyze_requirements(self, content):
        prompt = f"""Analyze the following business requirements and categorize them into:
        1. Functional Requirements
        2. Non-functional Requirements
        3. Technical Constraints
        4. Business Objectives
        
        Content:
        {content}
        
        Provide a structured analysis with clear categorization."""
        
        return self.groq_client.generate_completion(prompt)
    
    def generate_technical_specs(self, requirements):
        prompt = f"""Transform these business requirements into detailed technical specifications:
        1. System Architecture
        2. Data Models
        3. API Specifications
        4. Integration Requirements
        5. Performance Requirements
        
        Requirements:
        {requirements}
        
        Provide specific, implementable technical specifications."""
        
        return self.groq_client.generate_completion(prompt)
        
    def suggest_architecture(self, tech_specs):
        prompt = f"""Based on these technical specifications, recommend an optimal system architecture including:
        1. Technology Stack
        2. System Components
        3. Integration Patterns
        4. Deployment Model
        
        Specifications:
        {tech_specs}
        
        Provide a detailed architecture recommendation with justifications."""
        
        return self.groq_client.generate_completion(prompt)