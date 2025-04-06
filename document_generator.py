from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

class DocumentGenerator:
    def generate_documents(self, requirements, tech_specs, project_plan, cost_estimate):
        doc = Document()
        self._add_title_page(doc)
        self._add_executive_summary(doc, requirements, cost_estimate)
        self._add_requirements_section(doc, requirements)
        self._add_technical_specs_section(doc, tech_specs)
        self._add_project_plan_section(doc, project_plan)
        self._add_cost_section(doc, cost_estimate)
        
        # Save to byte stream for Streamlit download
        import io
        doc_stream = io.BytesIO()
        doc.save(doc_stream)
        doc_stream.seek(0)
        return doc_stream.getvalue()
    
    def _add_title_page(self, doc):
        title = doc.add_heading('Project Analysis Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add date and other metadata
        doc.add_paragraph().add_run().add_break()
        date_paragraph = doc.add_paragraph()
        date_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_paragraph.add_run('Generated: ' + self._get_current_date())
        
        doc.add_page_break()
    
    def _add_executive_summary(self, doc, requirements, cost_estimate):
        doc.add_heading('Executive Summary', level=1)
        summary = doc.add_paragraph()
        summary.add_run('This document presents a comprehensive analysis of the project requirements, ')
        summary.add_run('technical specifications, implementation plan, and associated costs.')
        doc.add_page_break()
    
    def _add_requirements_section(self, doc, requirements):
        doc.add_heading('Requirements Analysis', level=1)
        if isinstance(requirements, str):
            doc.add_paragraph(requirements)
        elif isinstance(requirements, dict):
            for key, value in requirements.items():
                doc.add_heading(key.title(), level=2)
                if isinstance(value, list):
                    for item in value:
                        doc.add_paragraph(item, style='List Bullet')
                else:
                    doc.add_paragraph(str(value))
    
    def _add_technical_specs_section(self, doc, tech_specs):
        doc.add_heading('Technical Specifications', level=1)
        if isinstance(tech_specs, str):
            doc.add_paragraph(tech_specs)
        else:
            doc.add_paragraph(str(tech_specs))
    
    def _add_project_plan_section(self, doc, project_plan):
        doc.add_heading('Project Implementation Plan', level=1)
        if isinstance(project_plan, dict):
            for section, content in project_plan.items():
                doc.add_heading(section.replace('_', ' ').title(), level=2)
                if isinstance(content, str):
                    doc.add_paragraph(content)
                else:
                    doc.add_paragraph(str(content))
    
    def _add_cost_section(self, doc, cost_estimate):
        doc.add_heading('Cost Estimation', level=1)
        if isinstance(cost_estimate, dict):
            for category, costs in cost_estimate.items():
                doc.add_heading(category.replace('_', ' ').title(), level=2)
                if isinstance(costs, dict):
                    for item, amount in costs.items():
                        p = doc.add_paragraph(style='List Bullet')
                        p.add_run(f"{item.replace('_', ' ').title()}: ${amount:,.2f}")
                else:
                    doc.add_paragraph(f"${costs:,.2f}")
    
    def _get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")