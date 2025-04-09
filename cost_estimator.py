from loguru import logger
import json
from typing import Dict, Union, Any
from datetime import datetime  # Added this import

class CostEstimator:
    def __init__(self, hourly_rate: float = 150.0):
        self.hourly_rate = hourly_rate

    def calculate_costs(self, project_plan: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        try:
            # Convert string to dictionary if needed
            if isinstance(project_plan, str):
                try:
                    project_plan = json.loads(project_plan)
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "message": "Invalid JSON format in project plan",
                        "timestamp": datetime.now().isoformat()
                    }

            if not isinstance(project_plan, dict):
                return {
                    "status": "error",
                    "message": "Project plan must be a dictionary",
                    "timestamp": datetime.now().isoformat()
                }

            # Calculate costs
            labor_costs = self._calculate_labor_costs(project_plan)
            if isinstance(labor_costs, dict) and "status" in labor_costs and labor_costs["status"] == "error":
                return labor_costs

            # Infrastructure costs (example)
            infrastructure_costs = self._calculate_infrastructure_costs(project_plan)
            
            # Software license costs (example)
            license_costs = self._calculate_license_costs(project_plan)

            # Calculate total cost
            total_cost = labor_costs + infrastructure_costs + license_costs

            # Return formatted response
            return {
                "status": "success",
                
                "cost_breakdown": {
                    "labor_costs": {
                        "amount": round(labor_costs, 2),
                        "currency": "USD"
                    },
                    "infrastructure_costs": {
                        "amount": round(infrastructure_costs, 2),
                        "currency": "USD"
                    },
                    "license_costs": {
                        "amount": round(license_costs, 2),
                        "currency": "USD"
                    },
                    "total_cost": {
                        "amount": round(total_cost, 2),
                        "currency": "USD"
                    }
                },
                "metadata": {
                    "hourly_rate": self.hourly_rate,
                    "currency": "USD"
                }
            }

        except Exception as e:
            logger.error(f"Error calculating costs: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _calculate_labor_costs(self, project_plan: Dict[str, Any]) -> float:
        try:
            labor_cost = 0.0
            for phase, details in project_plan.items():
                if isinstance(details, dict):
                    # Calculate based on estimated hours
                    hours = float(details.get("estimated_hours", 0))
                    complexity_factor = float(details.get("complexity_factor", 1.0))
                    labor_cost += hours * self.hourly_rate * complexity_factor

            return labor_cost

        except Exception as e:
            logger.error(f"Error calculating labor costs: {str(e)}")
            return {
                "status": "error",
                "message": f"Labor cost calculation error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _calculate_infrastructure_costs(self, project_plan: Dict[str, Any]) -> float:
        # Example implementation
        return 500.0  # Placeholder value

    def _calculate_license_costs(self, project_plan: Dict[str, Any]) -> float:
        # Example implementation
        return 300.0  # Placeholder value