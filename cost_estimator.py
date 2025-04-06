class CostEstimator:
    def __init__(self):
        self.hourly_rates = {
            "senior_developer": 150,
            "developer": 100,
            "designer": 90,
            "project_manager": 125,
            "qa_engineer": 85
        }
        
    def calculate_costs(self, project_plan):
        return {
            "labor_costs": self._calculate_labor_costs(project_plan),
            "infrastructure_costs": self._calculate_infrastructure_costs(project_plan),
            "software_costs": self._calculate_software_costs(project_plan),
            "maintenance_costs": self._calculate_maintenance_costs(project_plan),
            "total_cost": self._calculate_total_cost()
        }
    
    def _calculate_labor_costs(self, project_plan):
        labor_costs = {}
        resources = project_plan.get("resources", {})
        timeline_weeks = self._extract_timeline_weeks(project_plan.get("timeline", ""))
        
        for role, rate in self.hourly_rates.items():
            # Assume 40 hours per week
            if role in str(resources):
                labor_costs[role] = rate * 40 * timeline_weeks
                
        return labor_costs
    
    def _calculate_infrastructure_costs(self, project_plan):
        # Estimate infrastructure costs based on project requirements
        # This could include cloud services, servers, etc.
        return {
            "cloud_services": 1000,  # Monthly estimate
            "servers": 2000,         # Monthly estimate
            "networking": 500        # Monthly estimate
        }
    
    def _calculate_software_costs(self, project_plan):
        # Estimate software licensing and tools costs
        return {
            "development_tools": 200,    # Monthly per developer
            "hosting": 300,              # Monthly estimate
            "third_party_services": 500  # Monthly estimate
        }
    
    def _calculate_maintenance_costs(self, project_plan):
        # Estimate ongoing maintenance costs
        # Usually 15-20% of development costs annually
        labor_costs = sum(self._calculate_labor_costs(project_plan).values())
        return labor_costs * 0.20  # 20% of development costs
    
    def _calculate_total_cost(self):
        # Calculate total project cost including contingency
        # Implementation would aggregate all costs and add contingency
        pass
    
    def _extract_timeline_weeks(self, timeline_str):
        # Extract number of weeks from timeline string
        # Simple implementation - would need more robust parsing
        try:
            return float(timeline_str.split()[0])
        except:
            return 12  # Default to 12 weeks if parsing fails