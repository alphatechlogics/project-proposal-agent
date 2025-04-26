import streamlit as st
from document_processor import DocumentProcessor
from ai_analysis import AIAnalysisPipeline
from project_planner import ProjectPlanner
from cost_estimator import CostEstimator
from document_generator import DocumentGenerator
from groq_client import GroqClient
from loguru import logger

def format_project_plan_markdown(project_plan):
    md = """
# 📅 Project Plan Details

## 🎯 Work Breakdown Structure
"""
    if "work_breakdown" in project_plan:
        wb = project_plan["work_breakdown"]
        if isinstance(wb, dict) and "phases" in wb:
            # Create a summary table
            md += "\n### Phase Summary\n"
            md += "| Phase | Hours | Complexity | Main Roles |\n"
            md += "|-------|--------|------------|------------|\n"
            
            total_hours = 0
            for phase in wb["phases"]:
                hours = phase.get("estimated_hours", 0)
                total_hours += hours
                complexity = phase.get("complexity_factor", 1.0)
                
                # Get top 2 roles by distribution
                roles = phase.get("role_distribution", {})
                top_roles = sorted(roles.items(), key=lambda x: x[1], reverse=True)[:2]
                role_text = ", ".join([role for role, _ in top_roles])
                
                md += f"| {phase['name']} | {hours} | {complexity}x | {role_text} |\n"
            
            md += f"\n**Total Estimated Hours:** {total_hours}\n\n"
            
            # Detailed phase breakdown
            md += "\n### Detailed Phase Breakdown\n"
            for phase in wb["phases"]:
                md += f"\n#### {phase['name']}\n"
                md += f"**Hours:** {phase.get('estimated_hours', 0)}  "
                md += f"**Complexity:** {phase.get('complexity_factor', 1.0)}x\n\n"
                
                # Role distribution
                md += "**Team Allocation:**\n"
                for role, percentage in phase.get("role_distribution", {}).items():
                    md += f"- {role}: {percentage * 100:.0f}%\n"
                md += "\n"
                
                # Tasks
                if "tasks" in phase and phase["tasks"]:
                    md += "**Tasks:**\n"
                    for task in phase["tasks"]:
                        md += f"- {task}\n"
                md += "\n"
                
                # Deliverables
                if "deliverables" in phase and phase["deliverables"]:
                    md += "**Deliverables:**\n"
                    for deliverable in phase["deliverables"]:
                        md += f"- {deliverable}\n"
                md += "\n"
                
                # Dependencies
                if "dependencies" in phase and phase["dependencies"]:
                    md += "**Dependencies:**\n"
                    for dep in phase["dependencies"]:
                        md += f"- {dep}\n"
                md += "\n"
        else:
            md += str(wb)
    
    md += "\n## ⏱️ Timeline\n"
    if "timeline" in project_plan:
        timeline_text = project_plan['timeline']
        # Split timeline into phases
        phases = timeline_text.split('\n\n')
        for phase in phases:
            if not phase.strip():
                continue
            # Add bullet points for better readability
            phase_lines = phase.split('\n')
            if phase_lines:
                md += f"\n### {phase_lines[0]}\n"  # Phase name and duration
                for line in phase_lines[1:]:
                    if line.strip():
                        md += f"{line}\n"
        md += "\n"
    
    md += "\n## 👥 Required Resources\n"
    if "resources" in project_plan:
        resources_text = project_plan['resources']
        sections = resources_text.split('\n\n')
        for section in sections:
            if not section.strip():
                continue
            lines = section.split('\n')
            if lines and ':' in lines[0]:
                section_name = lines[0].replace(':', '')
                md += f"\n### {section_name}\n"
                for line in lines[1:]:
                    if line.strip():
                        md += f"{line}\n"
            else:
                md += section + "\n\n"
    
    md += "\n## ⚠️ Risk Assessment\n"
    if "risks" in project_plan:
        risks_text = project_plan['risks']
        # Format risks with severity indicators
        risk_levels = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }
        
        # Process risks by category
        current_category = ""
        for line in risks_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a category header
            if line.endswith("Risks:"):
                current_category = f"\n### {line}\n"
                md += current_category
                continue
            
            # Add risk level indicators
            risk_level = "medium"  # default
            for level in risk_levels:
                if f"({level})" in line.lower():
                    risk_level = level
                    break
            
            if line.startswith('- ') or line.startswith('* '):
                md += f"{risk_levels[risk_level]} {line[2:]}\n"
            else:
                md += f"{risk_levels[risk_level]} {line}\n"
    
    return md

def format_cost_estimate_markdown(cost_estimate, cost_params):
    if not isinstance(cost_estimate, dict) or "cost_breakdown" not in cost_estimate:
        return "Error: Invalid cost estimate data"
    
    costs = cost_estimate["cost_breakdown"]
    metadata = cost_estimate.get("metadata", {})
    
    md = """
# 💰 Project Cost Analysis

## 📊 Summary
"""
    # Total cost with risk buffer
    total_cost = costs["total_cost"]["amount"]
    risk_buffer = costs.get("risk_buffer", 0)
    
    # Create summary metrics
    md += f"""
| Metric | Amount |
|--------|---------|
| **Total Project Cost** | ${total_cost:,.2f} |
| **Risk Buffer** | ${risk_buffer:,.2f} |
| **Base Cost** | ${(total_cost - risk_buffer):,.2f} |
"""
    
    # Labor costs breakdown with percentage
    md += "\n## 👥 Labor Cost Distribution\n"
    labor_costs = costs["labor_costs"]
    total_labor = labor_costs["amount"]
    
    md += f"\n**Total Labor Cost:** ${total_labor:,.2f}\n\n"
    
    if "breakdown" in labor_costs:
        md += "| Role | Cost | % of Labor Cost |\n"
        md += "|------|------|----------------|\n"
        for role, cost in labor_costs["breakdown"].items():
            percentage = (cost / total_labor * 100) if total_labor > 0 else 0
            md += f"| {role} | ${cost:,.2f} | {percentage:.1f}% |\n"
    md += "\n"
    
    # Infrastructure costs with cloud services
    md += "## 🖥️ Infrastructure Details\n"
    infra_cost = costs["infrastructure_costs"]["amount"]
    md += f"\n**Total Infrastructure Cost:** ${infra_cost:,.2f}\n"
    
    if "cloud_services" in cost_params:
        md += "\n### Selected Cloud Services\n"
        for service in cost_params["cloud_services"]:
            md += f"- {service}\n"
    md += "\n"
    
    # License costs with breakdown
    md += "## 📄 License Details\n"
    license_cost = costs["license_costs"]["amount"]
    md += f"\n**Total License Cost:** ${license_cost:,.2f}\n"
    
    if "additional_licenses" in cost_params:
        md += "\n### Required Licenses\n"
        for license in cost_params["additional_licenses"]:
            md += f"- {license}\n"
    md += "\n"
    
    # Project factors and metrics
    md += "## 📈 Project Factors & Metrics\n\n"
    md += "| Factor | Value |\n"
    md += "|--------|--------|\n"
    md += f"| Complexity Multiplier | {cost_params['complexity_multiplier']}x |\n"
    md += f"| Risk Factor | {cost_params['risk_factor']}x |\n"
    
    # Cost Distribution Chart (ASCII)
    md += "\n## 📊 Cost Distribution\n"
    total = total_cost if total_cost > 0 else 1  # Avoid division by zero
    labor_percent = (total_labor / total) * 100
    infra_percent = (infra_cost / total) * 100
    license_percent = (license_cost / total) * 100
    
    md += "\n```\n"
    md += "Cost Breakdown:\n"
    md += f"Labor       {'█' * int(labor_percent/2)}{' ' * (50 - int(labor_percent/2))} {labor_percent:.1f}%\n"
    md += f"Infra      {'█' * int(infra_percent/2)}{' ' * (50 - int(infra_percent/2))} {infra_percent:.1f}%\n"
    md += f"Licenses   {'█' * int(license_percent/2)}{' ' * (50 - int(license_percent/2))} {license_percent:.1f}%\n"
    md += "```\n\n"
    
    # Additional Notes
    if metadata:
        md += "## ℹ️ Additional Information\n"
        md += f"- **Currency:** {metadata.get('currency', 'USD')}\n"
        md += f"- **Timestamp:** {metadata.get('timestamp', 'N/A')}\n"
        
    return md

st.set_page_config(page_title="AI Document Generation System", layout="wide")

def initialize_groq_client():
    try:
        client = GroqClient()
        client.initialize()
        return client
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        return None

def run_ai_analysis(ai_pipeline, content):
    progress_bar = st.progress(0)
    col1, col2, col3 = st.columns(3)
    
    try:
        with col1:
            with st.spinner("Analyzing requirements..."):
                requirements = ai_pipeline.analyze_requirements(content)
                progress_bar.progress(33)

        with col2:
            with st.spinner("Generating technical specs..."):
                tech_specs = ai_pipeline.generate_technical_specs(requirements)
                progress_bar.progress(66)

        with col3:
            with st.spinner("Suggesting architecture..."):
                architecture = ai_pipeline.suggest_architecture(tech_specs)
                progress_bar.progress(100)

        return requirements, tech_specs, architecture
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        st.error("An error occurred during AI analysis. Please try again.")
        return None, None, None

def get_cost_inputs():
    st.sidebar.title("Cost Configuration")
    
    # Labor Costs Section
    st.sidebar.subheader("💼 Labor Costs")
    with st.sidebar.expander("Configure Labor Costs", expanded=True):
        hourly_rates = {
            "Junior Developer": st.number_input("Junior Developer Rate (USD/hr)", min_value=0.0, value=50.0, step=5.0),
            "Senior Developer": st.number_input("Senior Developer Rate (USD/hr)", min_value=0.0, value=150.0, step=10.0),
            "Project Manager": st.number_input("Project Manager Rate (USD/hr)", min_value=0.0, value=175.0, step=10.0),
            "Designer": st.number_input("Designer Rate (USD/hr)", min_value=0.0, value=125.0, step=10.0)
        }
        avg_hourly_rate = sum(hourly_rates.values()) / len(hourly_rates)
    
    # Infrastructure Costs Section
    st.sidebar.subheader("🖥️ Infrastructure Costs")
    with st.sidebar.expander("Configure Infrastructure Costs", expanded=True):
        infrastructure_cost = st.number_input("Base Infrastructure Cost (USD)", min_value=0.0, value=500.0, step=100.0)
        cloud_services = st.multiselect(
            "Select Cloud Services",
            ["AWS", "Azure", "Google Cloud", "Other"],
            default=["AWS"]
        )
        if "Other" in cloud_services:
            other_infra_cost = st.number_input("Additional Infrastructure Cost (USD)", min_value=0.0, value=0.0, step=100.0)
            infrastructure_cost += other_infra_cost
    
    # License Costs Section
    st.sidebar.subheader("📄 License Costs")
    with st.sidebar.expander("Configure License Costs", expanded=True):
        license_cost = st.number_input("Base License Cost (USD)", min_value=0.0, value=300.0, step=100.0)
        additional_licenses = st.multiselect(
            "Additional Licenses Required",
            ["Development Tools", "Monitoring Tools", "Security Tools", "Other"],
            default=[]
        )
        if "Other" in additional_licenses:
            other_license_cost = st.number_input("Additional License Cost (USD)", min_value=0.0, value=0.0, step=100.0)
            license_cost += other_license_cost
    
    # Project Complexity and Risk Section
    st.sidebar.subheader("📊 Project Factors")
    with st.sidebar.expander("Configure Project Factors", expanded=True):
        complexity_multiplier = st.slider(
            "Project Complexity Factor",
            min_value=1.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Affects overall cost based on project complexity"
        )
        risk_factor = st.slider(
            "Risk Factor",
            min_value=1.0,
            max_value=1.5,
            value=1.0,
            step=0.1,
            help="Additional cost buffer for risk mitigation"
        )
    
    return {
        "hourly_rate": avg_hourly_rate,
        "hourly_rates": hourly_rates,
        "infrastructure_cost": infrastructure_cost,
        "license_cost": license_cost,
        "complexity_multiplier": complexity_multiplier,
        "risk_factor": risk_factor,
        "cloud_services": cloud_services,
        "additional_licenses": additional_licenses
    }

def main():
    st.title("AI Document Generation System")
    
    # Initialize Groq client
    groq_client = initialize_groq_client()
    if not groq_client:
        st.warning("Please check your GROQ_API_KEY in the .env file")
        return
    
    # Get cost inputs from sidebar
    cost_params = get_cost_inputs()
    
    # Main content area
    st.subheader("📄 Document Upload")
    uploaded_file = st.file_uploader("Upload Business Requirements Document", type=['docx', 'pdf', 'txt'])
    
    if uploaded_file:
        # Show start button
        start_process = st.button("🚀 Start Document Analysis", type="primary", use_container_width=True)
        
        if start_process:
            # Initialize components
            doc_processor = DocumentProcessor()
            ai_pipeline = AIAnalysisPipeline(groq_client)
            project_planner = ProjectPlanner(groq_client)
            cost_estimator = CostEstimator(groq_client)  # Updated to use groq_client
            doc_generator = DocumentGenerator()
            
            try:
                # Process document
                with st.spinner("Processing document..."):
                    extracted_content = doc_processor.process_document(uploaded_file)
                    
                    # Add cost parameters to the content for LLM context
                    enhanced_content = f"""
                    Document Content:
                    {extracted_content}
                    
                    Cost Parameters:
                    - Average Hourly Rate: ${cost_params['hourly_rate']}
                    - Infrastructure Cost: ${cost_params['infrastructure_cost']}
                    - License Cost: ${cost_params['license_cost']}
                    - Complexity Multiplier: {cost_params['complexity_multiplier']}
                    - Risk Factor: {cost_params['risk_factor']}
                    - Cloud Services: {', '.join(cost_params['cloud_services'])}
                    - Additional Licenses: {', '.join(cost_params['additional_licenses'])}
                    """
                    
                    # AI Analysis with cost context
                    requirements, tech_specs, architecture = run_ai_analysis(ai_pipeline, enhanced_content)
                    
                    # Project Planning with cost awareness
                    project_plan = project_planner.generate_plan(tech_specs)
                    
                    # Cost Estimation using direct LLM analysis
                    cost_estimate = cost_estimator.calculate_costs(project_plan, cost_params)
                    
                    # Generate Final Documents
                    final_documents = doc_generator.generate_documents(
                        requirements=requirements,
                        tech_specs=tech_specs,
                        project_plan=project_plan,
                        cost_estimate=cost_estimate
                    )
                    
                    # Display Results
                    st.success("✅ Document processing complete!")
                    
                    # Display tabs for different sections
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Requirements", "Technical Specs", "Architecture", "Project Plan", "Cost Estimate"])
                    
                    with tab1:
                        st.header("📋 Analyzed Requirements")
                        st.write(requirements)
                        
                    with tab2:
                        st.header("🔧 Technical Specifications")
                        st.write(tech_specs)
                        
                    with tab3:
                        st.header("🏗️ Suggested Architecture")
                        st.write(architecture)
                        
                    with tab4:
                        st.header("📅 Project Plan")
                        st.markdown(project_plan)
                        
                        # Add export buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "📥 Export Project Plan as MD",
                                project_plan,
                                file_name="project_plan.md",
                                mime="text/markdown"
                            )
                        
                    with tab5:
                        st.header("💰 Cost Estimate")
                        st.markdown(cost_estimate)
                        
                        # Add export buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "📥 Export Cost Estimate as MD",
                                cost_estimate,
                                file_name="cost_estimate.md",
                                mime="text/markdown"
                            )
                    
                    # Download complete report
                    st.divider()
                    st.subheader("📊 Complete Report")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download Complete Report (DOCX)",
                            data=final_documents,
                            file_name="project_analysis_report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()