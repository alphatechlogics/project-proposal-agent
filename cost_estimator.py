from loguru import logger
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class CostEstimator:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        self._setup_chain()
        
    def _setup_chain(self):
        cost_template = """Based on the provided project plan and resources, generate a detailed cost estimate.

        Project Plan and Resources:
        {project_plan}
        
        Cost Parameters:
        - Average hourly rates: {hourly_rates}
        - Infrastructure base cost: {infrastructure_cost}
        - License base cost: {license_cost}
        - Project complexity: {complexity}
        - Risk factor: {risk_factor}
        - Cloud services: {cloud_services}
        - Additional licenses: {additional_licenses}

        Provide a detailed cost analysis that includes:
        1. Labor Costs:
           - Break down by role and phase
           - Consider complexity and expertise levels
           - Account for different hourly rates
           
        2. Infrastructure Costs:
           - Cloud services and hosting
           - Development environments
           - Testing and staging setups
           - Monitoring and security
           
        3. License and Tool Costs:
           - Development tools
           - Third-party services
           - Testing tools
           - Security and compliance tools
           
        4. Risk Buffer and Contingency:
           - Risk-based adjustments
           - Contingency calculations
           - Buffer recommendations
           
        Format the response in a clear, structured way with detailed breakdowns and explanations."""
        
        self.cost_chain = self.groq_client.create_chain(cost_template)
    
    def calculate_costs(self, project_plan, cost_params):
        """Generate cost estimate using LLM analysis."""
        try:
            # Format the input for the LLM
            chain_input = {
                "project_plan": project_plan,
                "hourly_rates": cost_params.get("hourly_rates", "Standard industry rates"),
                "infrastructure_cost": cost_params.get("infrastructure_cost", "$500 base"),
                "license_cost": cost_params.get("license_cost", "$300 base"),
                "complexity": cost_params.get("complexity_multiplier", "1.0"),
                "risk_factor": cost_params.get("risk_factor", "1.0"),
                "cloud_services": ", ".join(cost_params.get("cloud_services", ["Basic cloud setup"])),
                "additional_licenses": ", ".join(cost_params.get("additional_licenses", ["Standard tools"]))
            }
            
            # Get cost analysis from LLM
            cost_analysis = self.cost_chain.run(**chain_input)
            return cost_analysis
            
        except Exception as e:
            logger.error(f"Error generating cost estimate: {str(e)}")
            return "Error generating cost estimate. Please check the inputs and try again."