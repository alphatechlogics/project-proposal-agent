from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain


class AIAnalysisPipeline:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        self._setup_chains()
        
    def _setup_chains(self):
        # Requirements analysis chain with improved structure
        requirements_template = """Analyze the following business requirements and provide a detailed breakdown.
        
        Content: {input_text}
        
        Please provide a structured analysis in the following format:

        1. Functional Requirements:
           - Core features and capabilities
           - User interactions and workflows
           - System behaviors and responses
           - Data processing requirements
           
        2. Non-functional Requirements:
           - Performance criteria
           - Scalability needs
           - Security requirements
           - Reliability standards
           - Usability requirements
           
        3. Technical Constraints:
           - System limitations
           - Integration requirements
           - Technology stack constraints
           - Infrastructure requirements
           
        4. Business Objectives:
           - Primary goals
           - Success metrics
           - Business outcomes
           - Strategic alignment
        
        For each requirement, include:
        - Priority level (High/Medium/Low)
        - Implementation complexity
        - Dependencies
        - Success criteria

        Format the output in a clear, hierarchical structure."""
        
        self.requirements_chain = LLMChain(
            llm=self.groq_client.llm,
            prompt=PromptTemplate.from_template(requirements_template),
            output_key="requirements"
        )
        
        # Technical specs chain with detailed structure
        specs_template = """Based on these analyzed requirements, create comprehensive technical specifications.

        Requirements Analysis: {requirements}
        
        Provide detailed specifications in the following format:

        1. System Architecture:
           - Architecture pattern (e.g., microservices, monolithic)
           - Component breakdown
           - System interactions
           - Data flow patterns
           
        2. Data Models:
           - Core entities
           - Relationships
           - Data validation rules
           - Storage requirements
           
        3. API Specifications:
           - Endpoints structure
           - Request/Response formats
           - Authentication/Authorization
           - Rate limiting and security
           
        4. Integration Requirements:
           - External systems
           - APIs and protocols
           - Data synchronization
           - Error handling
           
        5. Performance Requirements:
           - Response time targets
           - Throughput requirements
           - Scalability metrics
           - Resource utilization
           
        For each specification:
        - Implementation priority
        - Technical complexity
        - Dependencies
        - Validation criteria

        Focus on specifics that can be directly implemented by the development team."""
        
        self.specs_chain = LLMChain(
            llm=self.groq_client.llm,
            prompt=PromptTemplate.from_template(specs_template),
            output_key="tech_specs"
        )
        
        # Architecture chain with implementation focus
        architecture_template = """Based on the technical specifications, recommend a detailed system architecture.

        Technical Specifications: {tech_specs}
        
        Provide a comprehensive architecture recommendation in the following format:

        1. Technology Stack:
           - Frontend technologies
           - Backend technologies
           - Database solutions
           - Infrastructure components
           
        2. System Components:
           - Core services
           - Supporting services
           - External integrations
           - Development tools
           
        3. Integration Patterns:
           - Communication protocols
           - Data exchange formats
           - Security measures
           - Monitoring solutions
           
        4. Deployment Model:
           - Infrastructure requirements
           - Scaling strategy
           - High availability setup
           - Disaster recovery plan
           
        For each architectural decision:
        - Technical justification
        - Implementation considerations
        - Scalability impact
        - Maintenance implications

        Focus on practical, implementable solutions that align with modern best practices."""
        
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
        """Analyze and structure the requirements from the input content."""
        try:
            return self.requirements_chain.run({"input_text": content})
        except Exception as e:
            logger.error(f"Error analyzing requirements: {str(e)}")
            # Return a structured error message that won't break the chain
            return """
            Error analyzing requirements. Using default structure:
            
            1. Functional Requirements:
               - Core system functionality required
               - Basic user interactions
               
            2. Non-functional Requirements:
               - Standard performance metrics
               - Basic security requirements
               
            3. Technical Constraints:
               - Standard system limitations
               - Basic integration needs
               
            4. Business Objectives:
               - Primary system goals
               - Basic success metrics
            """
    
    def generate_technical_specs(self, requirements):
        """Generate technical specifications based on the requirements."""
        try:
            return self.specs_chain.run(requirements=requirements)
        except Exception as e:
            logger.error(f"Error generating technical specs: {str(e)}")
            # Return a structured error message that won't break the chain
            return """
            Error generating specifications. Using default structure:
            
            1. System Architecture:
               - Basic system components
               - Standard interactions
               
            2. Data Models:
               - Core data entities
               - Basic relationships
               
            3. API Specifications:
               - Essential endpoints
               - Standard security
               
            4. Integration Requirements:
               - Basic external systems
               - Standard protocols
               
            5. Performance Requirements:
               - Baseline metrics
               - Standard scalability
            """
        
    def suggest_architecture(self, tech_specs):
        """Suggest system architecture based on technical specifications."""
        try:
            return self.architecture_chain.run(tech_specs=tech_specs)
        except Exception as e:
            logger.error(f"Error suggesting architecture: {str(e)}")
            # Return a structured error message that won't break the chain
            return """
            Error suggesting architecture. Using default structure:
            
            1. Technology Stack:
               - Standard web technologies
               - Basic database solution
               
            2. System Components:
               - Core service components
               - Essential integrations
               
            3. Integration Patterns:
               - REST APIs
               - Standard security
               
            4. Deployment Model:
               - Basic cloud infrastructure
               - Standard scaling approach
            """
        
    def run_full_analysis(self, content):
        """Run the complete analysis pipeline with error handling."""
        try:
            return self.full_analysis_chain({"input_text": content})
        except Exception as e:
            logger.error(f"Error in full analysis: {str(e)}")
            # Return a structured response with all required keys
            return {
                "requirements": self.analyze_requirements(content),
                "tech_specs": self.generate_technical_specs("Basic requirements"),
                "architecture": self.suggest_architecture("Standard specifications")
            }