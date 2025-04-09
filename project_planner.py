from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class ProjectPlanner:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        self._setup_chains()
        
    def _setup_chains(self):
        self.wbs_chain = self.groq_client.create_chain(
            """Create a detailed work breakdown structure for: {tech_specs}
            Include:
            1. Major phases
            2. Key deliverables
            3. Tasks and subtasks
            4. Dependencies
            
            Format as a structured list with estimated complexity levels."""
        )
        
        self.timeline_chain = self.groq_client.create_chain(
            """Generate a realistic timeline estimation for: {tech_specs}
            Consider:
            1. Task dependencies
            2. Resource availability
            3. Complexity factors
            4. Buffer periods
            
            Provide estimates in weeks/months with confidence levels."""
        )
        
        self.resources_chain = self.groq_client.create_chain(
            """Determine required resources for: {tech_specs}
            Include:
            1. Development team composition
            2. Technical infrastructure
            3. Tools and licenses
            4. External dependencies
            
            Provide specific roles and quantities needed."""
        )
        
        self.risks_chain = self.groq_client.create_chain(
            """Identify potential project risks for: {tech_specs}
            Include:
            1. Technical risks
            2. Resource risks
            3. Timeline risks
            4. External dependencies
            
            Provide risk levels and mitigation strategies."""
        )
    
    def generate_plan(self, tech_specs):
        return {
            "work_breakdown": self.wbs_chain.run(tech_specs=tech_specs),
            "timeline": self.timeline_chain.run(tech_specs=tech_specs),
            "resources": self.resources_chain.run(tech_specs=tech_specs),
            "risks": self.risks_chain.run(tech_specs=tech_specs)
        }