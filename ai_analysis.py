from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain


class AIAnalysisPipeline:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        self._setup_chains()
        
    def _setup_chains(self):
        # Requirements analysis chain
        requirements_template = """Analyze the following business requirements and categorize them into:
        1. Functional Requirements
        2. Non-functional Requirements
        3. Technical Constraints
        4. Business Objectives
        
        Content: {input_text}
        
        Provide a structured analysis with clear categorization."""
        
        self.requirements_chain = LLMChain(
            llm=self.groq_client.llm,
            prompt=PromptTemplate.from_template(requirements_template),
            output_key="requirements"
        )
        
        # Technical specs chain
        specs_template = """Transform these business requirements into detailed technical specifications:
        1. System Architecture
        2. Data Models
        3. API Specifications
        4. Integration Requirements
        5. Performance Requirements
        
        Requirements: {requirements}
        
        Provide specific, implementable technical specifications."""
        
        self.specs_chain = LLMChain(
            llm=self.groq_client.llm,
            prompt=PromptTemplate.from_template(specs_template),
            output_key="tech_specs"
        )
        
        # Architecture chain
        architecture_template = """Based on these technical specifications, recommend an optimal system architecture including:
        1. Technology Stack
        2. System Components
        3. Integration Patterns
        4. Deployment Model
        
        Specifications: {tech_specs}
        
        Provide a detailed architecture recommendation with justifications."""
        
        self.architecture_chain = LLMChain(
            llm=self.groq_client.llm,
            prompt=PromptTemplate.from_template(architecture_template),
            output_key="architecture"
        )

        # Combined sequential chain
        self.full_analysis_chain = SequentialChain(
            chains=[self.requirements_chain, self.specs_chain, self.architecture_chain],
            input_variables=["input_text"],
            output_variables=["requirements", "tech_specs", "architecture"],
            verbose=True
        )
        
    def analyze_requirements(self, content):
        return self.requirements_chain.run({"input_text": content})
    
    def generate_technical_specs(self, requirements):
        return self.specs_chain.run(requirements=requirements)
        
    def suggest_architecture(self, tech_specs):
        return self.architecture_chain.run(tech_specs=tech_specs)
        
    def run_full_analysis(self, content):
        return self.full_analysis_chain({"input_text": content})