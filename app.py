import streamlit as st
from document_processor import DocumentProcessor
from ai_analysis import AIAnalysisPipeline
from project_planner import ProjectPlanner
from cost_estimator import CostEstimator
from document_generator import DocumentGenerator
from groq_client import GroqClient
from loguru import logger

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

def main():
    st.title("AI Document Generation System")
    
    # Initialize Groq client
    groq_client = initialize_groq_client()
    if not groq_client:
        st.warning("Please check your GROQ_API_KEY in the .env file")
        return
    
    # Main content area
    uploaded_file = st.file_uploader("Upload Business Requirements Document", type=['docx', 'pdf', 'txt'])
    
    if uploaded_file:
        # Initialize components
        doc_processor = DocumentProcessor()
        ai_pipeline = AIAnalysisPipeline(groq_client)
        project_planner = ProjectPlanner(groq_client)
        cost_estimator = CostEstimator()
        doc_generator = DocumentGenerator()
        
        try:
            # Process document
            with st.spinner("Processing document..."):
                extracted_content = doc_processor.process_document(uploaded_file)
                
                # AI Analysis
                requirements, tech_specs, architecture = run_ai_analysis(ai_pipeline, extracted_content)
                
                # Project Planning
                project_plan = project_planner.generate_plan(tech_specs)
                
                # Cost Estimation
                cost_estimate = cost_estimator.calculate_costs(project_plan)
                
                # Generate Final Documents
                final_documents = doc_generator.generate_documents(
                    requirements=requirements,
                    tech_specs=tech_specs,
                    project_plan=project_plan,
                    cost_estimate=cost_estimate
                )
                
                # Display Results
                st.success("Document processing complete!")
                
                # Display tabs for different sections
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["Requirements", "Technical Specs", "Architecture", "Project Plan", "Cost Estimate"])
                
                with tab1:
                    st.header("Analyzed Requirements")
                    st.write(requirements)
                    
                with tab2:
                    st.header("Technical Specifications")
                    st.write(tech_specs)
                    
                with tab3:
                    st.header("Suggested Architecture")
                    st.write(architecture)
                    
                with tab4:
                    st.header("Project Plan")
                    st.write(project_plan)
                    
                with tab5:
                    st.header("Cost Estimate")
                    st.write(cost_estimate)
                
                # Download button for final documents
                st.download_button(
                    label="Download Complete Report",
                    data=final_documents,
                    file_name="project_analysis_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()