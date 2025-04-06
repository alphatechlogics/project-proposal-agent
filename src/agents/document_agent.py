from typing import Dict, Any, List
from pathlib import Path
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json

from ..config.settings import settings
from ..utils.logger import logger

class ProjectPlan(BaseModel):
    timeline: List[Dict[str, str]] = Field(description="List of timeline entries with dates and descriptions")
    milestones: List[Dict[str, str]] = Field(description="List of project milestones")
    deliverables: List[Dict[str, str]] = Field(description="List of project deliverables")
    resources: List[Dict[str, str]] = Field(description="List of required resources")

class CostEstimate(BaseModel):
    labor_costs: List[Dict[str, float]] = Field(description="List of labor costs with roles and amounts")
    material_costs: List[Dict[str, float]] = Field(description="List of material costs with items and amounts")
    timeline_expenses: List[Dict[str, float]] = Field(description="List of timeline-based expenses")
    contingency: float = Field(description="Contingency amount as a percentage")

class DocumentAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=settings.AGENT_SETTINGS["temperature"],
            max_tokens=settings.AGENT_SETTINGS["max_tokens"]
        )
        
        # Initialize output parsers
        self.project_plan_parser = PydanticOutputParser(pydantic_object=ProjectPlan)
        self.cost_estimate_parser = PydanticOutputParser(pydantic_object=CostEstimate)
        
        # Initialize prompt templates
        self.project_plan_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert project manager. Create a detailed project plan based on the given requirements.
            {format_instructions}"""),
            ("human", "{requirements}")
        ])
        
        self.cost_estimate_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert cost estimator. Create detailed cost estimates based on the given requirements.
            {format_instructions}"""),
            ("human", "{requirements}")
        ])
    
    def generate_project_plan(self, requirements: str) -> Dict[str, Any]:
        """Generate a project plan from requirements."""
        try:
            prompt = self.project_plan_template.format_messages(
                requirements=requirements,
                format_instructions=self.project_plan_parser.get_format_instructions()
            )
            
            response = self.llm.invoke(prompt)
            parsed_response = self.project_plan_parser.parse(response.content)
            
            logger.info("Successfully generated project plan")
            return {"content": parsed_response.model_dump_json(indent=2)}
        except Exception as e:
            logger.error(f"Error generating project plan: {str(e)}")
            raise
    
    def generate_estimates(self, requirements: str) -> Dict[str, Any]:
        """Generate cost estimates from requirements."""
        try:
            prompt = self.cost_estimate_template.format_messages(
                requirements=requirements,
                format_instructions=self.cost_estimate_parser.get_format_instructions()
            )
            
            response = self.llm.invoke(prompt)
            parsed_response = self.cost_estimate_parser.parse(response.content)
            
            logger.info("Successfully generated cost estimates")
            return {"content": parsed_response.model_dump_json(indent=2)}
        except Exception as e:
            logger.error(f"Error generating cost estimates: {str(e)}")
            raise