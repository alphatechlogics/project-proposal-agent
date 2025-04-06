class ProjectPlanner:
    def __init__(self, groq_client):
        self.groq_client = groq_client
        
    def generate_plan(self, tech_specs):
        return {
            "work_breakdown": self._create_work_breakdown(tech_specs),
            "timeline": self._estimate_timeline(tech_specs),
            "resources": self._allocate_resources(tech_specs),
            "risks": self._analyze_risks(tech_specs)
        }
    
    def _create_work_breakdown(self, tech_specs):
        prompt = f"""Create a detailed work breakdown structure for:
        {tech_specs}
        
        Include:
        1. Major phases
        2. Key deliverables
        3. Tasks and subtasks
        4. Dependencies
        
        Format as a structured list with estimated complexity levels."""
        
        return self.groq_client.generate_completion(prompt)
    
    def _estimate_timeline(self, tech_specs):
        prompt = f"""Generate a realistic timeline estimation for:
        {tech_specs}
        
        Consider:
        1. Task dependencies
        2. Resource availability
        3. Complexity factors
        4. Buffer periods
        
        Provide estimates in weeks/months with confidence levels."""
        
        return self.groq_client.generate_completion(prompt)
    
    def _allocate_resources(self, tech_specs):
        prompt = f"""Determine required resources for:
        {tech_specs}
        
        Include:
        1. Development team composition
        2. Technical infrastructure
        3. Tools and licenses
        4. External dependencies
        
        Provide specific roles and quantities needed."""
        
        return self.groq_client.generate_completion(prompt)
    
    def _analyze_risks(self, tech_specs):
        prompt = f"""Identify potential project risks for:
        {tech_specs}
        
        Include:
        1. Technical risks
        2. Resource risks
        3. Timeline risks
        4. External dependencies
        
        Provide risk levels and mitigation strategies."""
        
        return self.groq_client.generate_completion(prompt)