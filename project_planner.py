from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from loguru import logger

class ProjectPlanner:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        self._setup_chain()
        
    def _setup_chain(self):
        plan_template = """Based on the technical specifications provided, create a detailed project plan that includes clear phases, tasks, and resource allocation.

        Technical Specifications:
        {tech_specs}
        
        Generate a comprehensive project plan with the following structure:
        
        1. Project Phases:
           - Break down into logical phases
           - Include duration estimates for each phase
           - Specify key milestones and deliverables
           - Note dependencies between phases
           
        2. Resource Requirements:
           - Required team roles and expertise levels
           - Development tools and licenses needed
           - Infrastructure and cloud services required
           - Testing and deployment resources
           
        3. Implementation Timeline:
           - Start and end dates for each phase
           - Major milestones and deadlines
           - Critical path activities
           - Buffer periods for risks
           
        4. Risk Assessment:
           - Potential technical challenges
           - Resource availability risks
           - Timeline impact factors
           - Mitigation strategies
           
        Include sufficient detail for accurate cost estimation, such as:
        - Time estimates for each phase and major task
        - Specific expertise levels required
        - Infrastructure components needed
        - Third-party tools and services
        - Complex integration points
        - Performance requirements
        - Security considerations"""
        
        self.plan_chain = self.groq_client.create_chain(plan_template)
    
    def generate_plan(self, tech_specs):
        """Generate a detailed project plan from technical specifications."""
        try:
            return self.plan_chain.run(tech_specs=tech_specs)
        except Exception as e:
            logger.error(f"Error generating project plan: {str(e)}")
            return "Error generating project plan. Please check the inputs and try again."